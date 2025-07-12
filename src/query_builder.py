import re
import os
from typing import Dict, Optional, Tuple
from intelligent_query_processor import IntelligentQueryProcessor

class QueryBuilder:
    def __init__(self):
        # Initialize OpenAI-powered query processor
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'your_openai_api_key_here':
            try:
                self.intelligent_processor = IntelligentQueryProcessor(openai_key)
                # Check if OpenAI client was successfully initialized
                if self.intelligent_processor.client is not None:
                    self.use_ai = True
                else:
                    self.use_ai = False
                    print("OpenAI client initialization failed, falling back to pattern matching")
            except Exception as e:
                print(f"Failed to initialize IntelligentQueryProcessor: {e}")
                self.intelligent_processor = None
                self.use_ai = False
        else:
            self.intelligent_processor = None
            self.use_ai = False
            print("OpenAI API key not found, falling back to pattern matching")
        
        # Fallback patterns for when OpenAI is not available - more flexible patterns
        self.patterns = {
            'balance': r'balance.*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)|(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth).*balance',
            'transactions': r'transaction.*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)|(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth).*transaction|history.*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)',
            'contract_interactions': r'interact.*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)|(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth).*interact',
            'token_volume': r'volume.*token.*(\w+)|token.*volume'
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
            }
        }
        
        # ENS resolution capability
        self.well_known_ens = {
            "vitalik.eth": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            "ethereum.eth": "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359",
            "buterin.eth": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        }

    def extract_address_or_ens(self, prompt: str) -> Optional[str]:
        """Extract Ethereum address or ENS name from prompt and resolve to address"""
        # First try to find a regular Ethereum address (flexible length 39-42 chars)
        address_match = re.search(r'0x[a-fA-F0-9]{39,42}', prompt)
        if address_match:
            return address_match.group(0)
        
        # Then try to find ENS names
        ens_match = re.search(r'\b([a-zA-Z0-9-]+\.eth)\b', prompt, re.IGNORECASE)
        if ens_match:
            ens_name = ens_match.group(1).lower()
            # Check if it's a known ENS name
            if ens_name in self.well_known_ens:
                return self.well_known_ens[ens_name]
            # For unknown ENS names, try Web3 resolution (would need Web3 integration)
            # For now, return None for unknown ENS names
            return None
        
        return None

    def extract_address(self, prompt: str) -> Optional[str]:
        """Extract Ethereum address from prompt (legacy method)"""
        return self.extract_address_or_ens(prompt)

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
        prompt_lower = prompt.lower()
        
        # Simple keyword-based classification - much more reliable
        if 'balance' in prompt_lower:
            return 'balance'
        elif any(word in prompt_lower for word in ['transaction', 'history', 'tx']):
            return 'transactions'
        elif any(word in prompt_lower for word in ['interact', 'contract', 'call']):
            return 'contract_interactions'
        elif any(word in prompt_lower for word in ['volume', 'transfer']):
            return 'token_volume'
        
        # Fallback to regex patterns if keywords don't match
        for category, pattern in self.patterns.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                return category
        
        return None

    def build_query(self, prompt: str) -> Optional[Dict]:
        """Convert natural language prompt to Moralis API call using AI or fallback"""
        
        if self.use_ai and self.intelligent_processor:
            # Use OpenAI-powered intelligent processing
            try:
                understanding = self.intelligent_processor.understand_query(prompt)
                
                # Extract address from entities
                address = None
                for entity in understanding.entities:
                    if entity.type == "address":
                        address = entity.value
                        break
                
                if not address:
                    return None
                
                # Map AI intent to our endpoints
                intent_to_category = {
                    "wallet_analysis": "balance",
                    "token_analytics": "token_volume", 
                    "contract_intelligence": "contract_interactions"
                }
                
                category = intent_to_category.get(understanding.intent.value)
                
                # If AI detected transactions in metrics, override to transactions
                if "transactions" in understanding.metrics or "history" in understanding.metrics:
                    category = "transactions"
                
                if not category:
                    # Fallback: try to infer from the prompt content
                    if any(word in prompt.lower() for word in ['balance', 'wallet']):
                        category = "balance"
                    elif any(word in prompt.lower() for word in ['transaction', 'history']):
                        category = "transactions"
                    elif any(word in prompt.lower() for word in ['interact', 'contract']):
                        category = "contract_interactions"
                    elif any(word in prompt.lower() for word in ['volume', 'token']):
                        category = "token_volume"
                    else:
                        category = "balance"  # Default to balance
                
            except Exception as e:
                print(f"AI processing failed: {e}, falling back to pattern matching")
                return self._build_query_fallback(prompt)
        else:
            # Use pattern matching fallback
            return self._build_query_fallback(prompt)
        
        # Build the query using the determined category and address
        if not category:
            return None
            
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
                'from_date': '2024-01-01'
            }
        elif category == 'token_volume':
            token_symbol = self.extract_token_symbol(prompt)
            query['params'] = {
                'chain': 'eth',
                'contract_address': self.get_token_address(token_symbol),
                'from_date': '2024-01-01',
                'to_date': '2024-01-02'
            }
            
        return query
    
    def _build_query_fallback(self, prompt: str) -> Optional[Dict]:
        """Fallback method using pattern matching"""
        category = self.classify_prompt(prompt)
        if not category:
            return None
            
        address = self.extract_address(prompt)
        if not address:
            return None
            
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
                'from_date': '2024-01-01'
            }
        elif category == 'token_volume':
            token_symbol = self.extract_token_symbol(prompt)
            query['params'] = {
                'chain': 'eth',
                'contract_address': self.get_token_address(token_symbol),
                'from_date': '2024-01-01',
                'to_date': '2024-01-02'
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
