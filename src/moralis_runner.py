import requests
import os
from typing import Dict, List, Optional
from datetime import datetime
import json

class MoralisRunner:
    def __init__(self):
        self.api_key = os.getenv('MORALIS_API_KEY')
        self.base_url = 'https://deep-index.moralis.io/api/v2.2'
        self.headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def run_query(self, query: Dict) -> Dict:
        """Execute Moralis API query"""
        endpoint = query['endpoint']
        params = query['params']
        
        try:
            if endpoint == 'wallet_balance':
                return self._get_wallet_balance(params)
            elif endpoint == 'wallet_history':
                return self._get_wallet_history(params)
            elif endpoint == 'contract_logs':
                return self._get_contract_logs(params)
            elif endpoint == 'token_transfers':
                return self._get_token_transfers(params)
            else:
                return {'error': f'Unknown endpoint: {endpoint}'}
                
        except Exception as e:
            return {'error': str(e)}

    def _get_wallet_balance(self, params: Dict) -> Dict:
        """Get wallet balance including native and ERC-20 tokens"""
        address = params['address']
        chain = params.get('chain', 'eth')
        
        # Get native balance
        url = f"{self.base_url}/{address}/balance"
        response = requests.get(url, headers=self.headers, params={'chain': chain})
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'formatted': self._format_balance_response(data)
            }
        else:
            return {'error': f'API Error: {response.status_code}', 'message': response.text}

    def _get_wallet_history(self, params: Dict) -> Dict:
        """Get wallet transaction history"""
        address = params['address']
        chain = params.get('chain', 'eth')
        limit = params.get('limit', 10)
        
        url = f"{self.base_url}/{address}"
        response = requests.get(url, headers=self.headers, params={
            'chain': chain,
            'limit': limit
        })
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'formatted': self._format_transaction_response(data)
            }
        else:
            return {'error': f'API Error: {response.status_code}', 'message': response.text}

    def _get_contract_logs(self, params: Dict) -> Dict:
        """Get contract interaction logs"""
        address = params['address']
        chain = params.get('chain', 'eth')
        
        url = f"{self.base_url}/{address}/logs"
        response = requests.get(url, headers=self.headers, params={'chain': chain})
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'formatted': self._format_logs_response(data)
            }
        else:
            return {'error': f'API Error: {response.status_code}', 'message': response.text}

    def _get_token_transfers(self, params: Dict) -> Dict:
        """Get token transfer data for volume analysis"""
        contract_address = params['contract_address']
        chain = params.get('chain', 'eth')
        
        url = f"{self.base_url}/erc20/{contract_address}/transfers"
        response = requests.get(url, headers=self.headers, params={'chain': chain})
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'formatted': self._format_transfers_response(data)
            }
        else:
            return {'error': f'API Error: {response.status_code}', 'message': response.text}

    def _format_balance_response(self, data: Dict) -> str:
        """Format balance data for display with enhanced interpretation"""
        balance_wei = int(data.get('balance', 0))
        balance_eth = balance_wei / 1e18
        
        # Add USD estimate (rough calculation)
        estimated_usd = balance_eth * 2000  # Rough ETH price estimate
        
        formatted = f"ETH Balance: {balance_eth:.6f} ETH"
        if estimated_usd > 0:
            formatted += f" (~${estimated_usd:,.2f} USD)"
        
        # Add interpretation
        if balance_eth > 10:
            formatted += "\n💰 High balance wallet"
        elif balance_eth > 1:
            formatted += "\n💼 Active wallet"
        elif balance_eth > 0.1:
            formatted += "\n🔸 Regular wallet"
        else:
            formatted += "\n🔹 Low balance wallet"
            
        return formatted

    def _format_transaction_response(self, data: Dict) -> str:
        """Format transaction data for display with enhanced interpretation"""
        if 'result' not in data:
            return "No transactions found"
            
        transactions = data['result'][:10]  # Limit to 10
        formatted = "Recent Transactions:\n"
        
        total_value = 0
        for tx in transactions:
            hash_short = tx.get('hash', '')[:10] + '...'
            value_wei = int(tx.get('value', 0))
            value_eth = value_wei / 1e18
            total_value += value_eth
            
            # Calculate gas fee if available
            gas_info = ""
            if tx.get('gas_used') and tx.get('gas_price'):
                gas_fee_wei = int(tx.get('gas_used', 0)) * int(tx.get('gas_price', 0))
                gas_fee_eth = gas_fee_wei / 1e18
                gas_info = f" (Gas: {gas_fee_eth:.6f} ETH)"
            
            # Add timestamp interpretation
            timestamp = tx.get('block_timestamp', '')
            time_info = ""
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_info = f" - {dt.strftime('%Y-%m-%d %H:%M')}"
                except:
                    pass
            
            formatted += f"- {hash_short}: {value_eth:.6f} ETH{gas_info}{time_info}\n"
        
        # Add summary
        formatted += f"\nSummary: {len(transactions)} transactions, Total value: {total_value:.6f} ETH"
        
        return formatted

    def _format_logs_response(self, data: Dict) -> str:
        """Format contract logs for display"""
        if 'result' not in data:
            return "No interactions found"
            
        logs = data['result']
        unique_addresses = set()
        for log in logs:
            unique_addresses.add(log.get('address', ''))
        
        return f"Unique addresses that interacted: {len(unique_addresses)}\n" + \
               "\n".join([f"- {addr}" for addr in list(unique_addresses)[:10]])

    def _format_transfers_response(self, data: Dict) -> str:
        """Format token transfers for volume calculation"""
        if 'result' not in data:
            return "No transfers found"
            
        transfers = data['result']
        total_volume = sum(float(t.get('value', 0)) for t in transfers)
        return f"24h Transfer Volume: {total_volume:.2f} tokens\n" + \
               f"Number of transfers: {len(transfers)}"
