# 🚀 Blockchain AI Assistant - Execution Guide

This document provides step-by-step instructions to implement the Blockchain AI Assistant using Moralis Web3 API as outlined in the PRD.

## 📋 Prerequisites

1. **Moralis Account Setup**
   - Sign up at [moralis.io](https://moralis.io)
   - Create a new project
   - Get your API key from the dashboard
   - Note your API key for later use

2. **Development Environment**
   - Python 3.8+ installed
   - Node.js 16+ (for MCP server)
   - Git initialized (already done)
   - Code editor (VS Code recommended)

## 🏗️ Implementation Steps

### Step 1: Project Structure Setup

Create the project structure:

```bash
mkdir src
mkdir config
mkdir tests
touch src/__init__.py
touch src/app.py
touch src/query_builder.py
touch src/moralis_runner.py
touch config/mcp-config.json
touch demo.md
touch requirements.txt
```

### Step 2: Dependencies Installation

Create `requirements.txt`:

```txt
openai>=1.0.0
requests>=2.31.0
streamlit>=1.28.0
python-dotenv>=1.0.0
moralis>=0.1.0
click>=8.1.0
tabulate>=0.9.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration

Create `.env` file:
```bash
touch .env
```

Add to `.env`:
```
MORALIS_API_KEY=your_moralis_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: MCP Server Configuration

Create `config/mcp-config.json`:

```json
{
  "mcpServers": {
    "moralis": {
      "command": "node",
      "args": ["moralis-mcp-server.js"],
      "env": {
        "MORALIS_API_KEY": "${MORALIS_API_KEY}"
      }
    }
  },
  "endpoints": {
    "wallet_balance": "https://deep-index.moralis.io/api/v2.2/{address}/balance",
    "wallet_history": "https://deep-index.moralis.io/api/v2.2/{address}",
    "contract_logs": "https://deep-index.moralis.io/api/v2.2/{address}/logs",
    "token_transfers": "https://deep-index.moralis.io/api/v2.2/erc20/{address}/transfers",
    "nft_transfers": "https://deep-index.moralis.io/api/v2.2/nft/transfers"
  }
}
```

### Step 5: Query Builder Implementation

Create `src/query_builder.py`:

```python
import re
from typing import Dict, Optional, Tuple

class QueryBuilder:
    def __init__(self):
        self.patterns = {
            'balance': r'balance.*wallet.*0x[a-fA-F0-9]{40}',
            'transactions': r'transactions.*address.*0x[a-fA-F0-9]{40}',
            'contract_interactions': r'interact.*contract.*0x[a-fA-F0-9]{40}',
            'token_volume': r'volume.*token.*(\w+)',
            'nft_transfers': r'NFT.*0x[a-fA-F0-9]{40}'
        }
        
        self.templates = {
            'balance': {
                'endpoint': 'wallet_balance',
                'method': 'GET',
                'params': ['chain', 'address']
            },
            'transactions': {
                'endpoint': 'wallet_history', 
                'method': 'GET',
                'params': ['chain', 'address', 'limit']
            },
            'contract_interactions': {
                'endpoint': 'contract_logs',
                'method': 'GET', 
                'params': ['chain', 'address', 'from_date']
            },
            'token_volume': {
                'endpoint': 'token_transfers',
                'method': 'GET',
                'params': ['chain', 'address', 'from_date', 'to_date']
            },
            'nft_transfers': {
                'endpoint': 'nft_transfers',
                'method': 'GET',
                'params': ['chain', 'from_date', 'to_date', 'contract_addresses']
            }
        }

    def extract_address(self, prompt: str) -> Optional[str]:
        """Extract Ethereum address from prompt"""
        match = re.search(r'0x[a-fA-F0-9]{40}', prompt)
        return match.group(0) if match else None

    def extract_token_symbol(self, prompt: str) -> Optional[str]:
        """Extract token symbol from prompt"""
        # Look for common token patterns
        tokens = ['PEPE', 'USDC', 'USDT', 'WETH', 'DAI']
        for token in tokens:
            if token.upper() in prompt.upper():
                return token
        return None

    def classify_prompt(self, prompt: str) -> Optional[str]:
        """Classify the prompt into one of our supported categories"""
        for category, pattern in self.patterns.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                return category
        return None

    def build_query(self, prompt: str) -> Optional[Dict]:
        """Convert natural language prompt to Moralis API call"""
        category = self.classify_prompt(prompt)
        if not category:
            return None
            
        address = self.extract_address(prompt)
        template = self.templates[category]
        
        query = {
            'endpoint': template['endpoint'],
            'method': template['method'],
            'params': {}
        }
        
        # Build parameters based on category
        if category == 'balance':
            query['params'] = {
                'chain': 'eth',
                'address': address
            }
        elif category == 'transactions':
            query['params'] = {
                'chain': 'eth', 
                'address': address,
                'limit': 10
            }
        elif category == 'contract_interactions':
            query['params'] = {
                'chain': 'eth',
                'address': address,
                'from_date': '2024-01-01'  # Last 24 hours logic needed
            }
        elif category == 'token_volume':
            token_symbol = self.extract_token_symbol(prompt)
            query['params'] = {
                'chain': 'eth',
                'contract_address': self.get_token_address(token_symbol),
                'from_date': '2024-01-01',
                'to_date': '2024-01-02'
            }
        elif category == 'nft_transfers':
            query['params'] = {
                'chain': 'eth',
                'contract_addresses': [address],
                'from_date': '2024-01-01',
                'to_date': '2024-01-08'
            }
            
        return query

    def get_token_address(self, symbol: str) -> str:
        """Get contract address for token symbol"""
        token_addresses = {
            'PEPE': '0x6982508145454Ce325dDbE47a25d4ec3d2311933',
            'USDC': '0xA0b86a33E6441b8C4505B4afDcA7FBf074497C23',
            'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        }
        return token_addresses.get(symbol.upper(), '')
```

### Step 6: Moralis API Runner Implementation

Create `src/moralis_runner.py`:

```python
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
            elif endpoint == 'nft_transfers':
                return self._get_nft_transfers(params)
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

    def _get_nft_transfers(self, params: Dict) -> Dict:
        """Get NFT transfer data"""
        chain = params.get('chain', 'eth')
        contract_addresses = params.get('contract_addresses', [])
        
        url = f"{self.base_url}/nft/transfers"
        response = requests.get(url, headers=self.headers, params={
            'chain': chain,
            'contract_addresses': contract_addresses
        })
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'formatted': self._format_nft_response(data)
            }
        else:
            return {'error': f'API Error: {response.status_code}', 'message': response.text}

    def _format_balance_response(self, data: Dict) -> str:
        """Format balance data for display"""
        balance_eth = float(data.get('balance', 0)) / 1e18
        return f"ETH Balance: {balance_eth:.6f} ETH"

    def _format_transaction_response(self, data: Dict) -> str:
        """Format transaction data for display"""
        if 'result' not in data:
            return "No transactions found"
            
        transactions = data['result'][:10]  # Limit to 10
        formatted = "Recent Transactions:\n"
        for tx in transactions:
            hash_short = tx.get('hash', '')[:10] + '...'
            value_eth = float(tx.get('value', 0)) / 1e18
            formatted += f"- {hash_short}: {value_eth:.6f} ETH\n"
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

    def _format_nft_response(self, data: Dict) -> str:
        """Format NFT transfer data"""
        if 'result' not in data:
            return "No NFT transfers found"
            
        transfers = data['result']
        recipients = {}
        for transfer in transfers:
            to_addr = transfer.get('to_address', '')
            token_id = transfer.get('token_id', '')
            if to_addr not in recipients:
                recipients[to_addr] = []
            recipients[to_addr].append(token_id)
        
        formatted = "NFT Recipients:\n"
        for addr, tokens in recipients.items():
            formatted += f"- {addr}: {len(tokens)} NFTs\n"
        return formatted
```

### Step 7: Main Application Implementation

Create `src/app.py`:

```python
import streamlit as st
import os
from dotenv import load_dotenv
from query_builder import QueryBuilder
from moralis_runner import MoralisRunner

# Load environment variables
load_dotenv()

def main():
    st.title("🔗 Blockchain AI Assistant")
    st.write("Ask questions about blockchain data using natural language!")
    
    # Initialize components
    query_builder = QueryBuilder()
    moralis_runner = MoralisRunner()
    
    # Sample prompts
    st.sidebar.header("Sample Prompts")
    sample_prompts = [
        "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?",
        "List the last 10 transactions for address 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b",
        "Which addresses interacted with contract 0x6982508145454Ce325dDbE47a25d4ec3d2311933 in the past 24 hours?",
        "What's the 24-hour transfer volume of token PEPE?",
        "Which wallets received NFTs from 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b last week?"
    ]
    
    for i, prompt in enumerate(sample_prompts):
        if st.sidebar.button(f"Sample {i+1}", key=f"sample_{i}"):
            st.session_state.user_input = prompt
    
    # User input
    user_input = st.text_area(
        "Enter your blockchain question:",
        value=st.session_state.get('user_input', ''),
        height=100,
        key='input_area'
    )
    
    if st.button("Ask Question", type="primary"):
        if user_input:
            with st.spinner("Processing your question..."):
                # Build query
                query = query_builder.build_query(user_input)
                
                if query:
                    st.subheader("Generated API Call")
                    st.json(query)
                    
                    # Execute query
                    result = moralis_runner.run_query(query)
                    
                    st.subheader("Result")
                    if result.get('success'):
                        st.success("Query executed successfully!")
                        st.text(result['formatted'])
                        
                        with st.expander("Raw API Response"):
                            st.json(result['data'])
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                        if 'message' in result:
                            st.text(result['message'])
                else:
                    st.error("Could not understand your question. Please try one of the sample prompts.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
```

### Step 8: CLI Version (Alternative)

Create `src/cli_app.py`:

```python
import click
import os
from dotenv import load_dotenv
from query_builder import QueryBuilder
from moralis_runner import MoralisRunner
from tabulate import tabulate

load_dotenv()

@click.command()
@click.option('--prompt', '-p', help='Natural language prompt')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(prompt, interactive):
    """Blockchain AI Assistant CLI"""
    
    query_builder = QueryBuilder()
    moralis_runner = MoralisRunner()
    
    if interactive:
        click.echo("🔗 Blockchain AI Assistant (Interactive Mode)")
        click.echo("Type 'quit' to exit\n")
        
        while True:
            user_input = click.prompt("Enter your blockchain question")
            
            if user_input.lower() == 'quit':
                break
                
            process_query(user_input, query_builder, moralis_runner)
            click.echo()
    
    elif prompt:
        process_query(prompt, query_builder, moralis_runner)
    else:
        click.echo("Please provide a prompt with -p or use -i for interactive mode")

def process_query(user_input, query_builder, moralis_runner):
    """Process a single query"""
    click.echo(f"Question: {user_input}")
    
    # Build query
    query = query_builder.build_query(user_input)
    
    if query:
        click.echo(f"API Call: {query['endpoint']}")
        
        # Execute query
        result = moralis_runner.run_query(query)
        
        if result.get('success'):
            click.echo("✅ Success!")
            click.echo(result['formatted'])
        else:
            click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
    else:
        click.echo("❌ Could not understand your question.")

if __name__ == "__main__":
    main()
```

### Step 9: Demo Script

Create `demo.md`:

```markdown
# Demo Script

## Setup
1. Ensure Moralis API key is set in .env
2. Run: `streamlit run src/app.py`
3. Open browser to localhost:8501

## Demo Flow

### Test 1: Wallet Balance
- **Input**: "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
- **Expected**: ETH balance display
- **API Call**: GET /wallets/{address}/balance

### Test 2: Transaction History  
- **Input**: "List the last 10 transactions for address 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b"
- **Expected**: Table with transaction hashes and values
- **API Call**: GET /wallets/{address}/history

### Test 3: Contract Interactions
- **Input**: "Which addresses interacted with contract 0x6982508145454Ce325dDbE47a25d4ec3d2311933 in the past 24 hours?"
- **Expected**: List of wallet addresses
- **API Call**: GET /contracts/{address}/logs

### Test 4: Token Volume
- **Input**: "What's the 24-hour transfer volume of token PEPE?"
- **Expected**: Volume in PEPE tokens
- **API Call**: GET /erc20/{address}/transfers

### Test 5: NFT Transfers
- **Input**: "Which wallets received NFTs from 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b last week?"
- **Expected**: List of recipient addresses with token IDs
- **API Call**: GET /nft/transfers
```

### Step 10: Testing

Create `tests/test_query_builder.py`:

```python
import unittest
from src.query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = QueryBuilder()
    
    def test_extract_address(self):
        prompt = "What's the balance of 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        address = self.builder.extract_address(prompt)
        self.assertEqual(address, "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b")
    
    def test_classify_balance_prompt(self):
        prompt = "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        category = self.builder.classify_prompt(prompt)
        self.assertEqual(category, "balance")
    
    def test_build_balance_query(self):
        prompt = "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"
        query = self.builder.build_query(prompt)
        self.assertIsNotNone(query)
        self.assertEqual(query['endpoint'], 'wallet_balance')

if __name__ == '__main__':
    unittest.main()
```

## 🚀 Running the Application

### Streamlit Web App
```bash
streamlit run src/app.py
```

### CLI Version
```bash
python src/cli_app.py -i  # Interactive mode
python src/cli_app.py -p "What's the balance of 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"  # Single query
```

### Run Tests
```bash
python -m pytest tests/
```

## 🔧 Troubleshooting

### Common Issues:
1. **API Key Error**: Ensure MORALIS_API_KEY is set in .env
2. **Rate Limiting**: Moralis has rate limits, add delays if needed
3. **Invalid Address**: Ensure Ethereum addresses are valid 40-character hex strings
4. **Network Issues**: Check internet connection and Moralis API status

### Debug Mode:
Add to any Python file:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Next Steps

1. **MCP Integration**: Set up actual MCP server wrapper
2. **Error Handling**: Add comprehensive error handling
3. **Caching**: Implement response caching for better performance
4. **UI Improvements**: Add charts and better data visualization
5. **More Chains**: Extend to support other blockchains (Polygon, BSC, etc.)

## ✅ Completion Checklist

- [ ] Moralis API key configured
- [ ] All Python files created
- [ ] Dependencies installed
- [ ] Streamlit app running
- [ ] All 5 use cases tested
- [ ] Demo script validated
- [ ] Error handling implemented
- [ ] Documentation complete
