import openai
import re
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class QueryIntent(Enum):
    WALLET_ANALYSIS = "wallet_analysis"
    TOKEN_ANALYTICS = "token_analytics"
    CONTRACT_INTELLIGENCE = "contract_intelligence"
    DEFI_OPERATIONS = "defi_operations"
    CROSS_CHAIN_ANALYSIS = "cross_chain_analysis"

@dataclass
class ExtractedEntity:
    type: str
    value: str
    confidence: float

@dataclass
class QueryUnderstanding:
    intent: QueryIntent
    entities: List[ExtractedEntity]
    timeframe: Optional[str]
    metrics: List[str]
    complexity: str  # simple, medium, complex
    requires_correlation: bool

class IntelligentQueryProcessor:
    def __init__(self, openai_api_key: str):
        try:
            self.client = openai.OpenAI(api_key=openai_api_key)
        except Exception as e:
            print(f"OpenAI client initialization failed: {e}")
            self.client = None
            
        self.blockchain_knowledge = self._load_blockchain_knowledge()
        # Initialize Web3 for ENS resolution
        try:
            from web3 import Web3
            alchemy_key = os.getenv('ALCHEMY_API_KEY')
            if alchemy_key:
                self.w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}"))
            else:
                # Fallback to public endpoint
                self.w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com"))
        except Exception as e:
            print(f"Web3 initialization failed: {e}")
            self.w3 = None
        
    def _load_blockchain_knowledge(self) -> Dict:
        """Load comprehensive blockchain domain knowledge"""
        return {
            "token_addresses": {
                "USDC": "0xA0b86a33E6441b8C4505B4afDcA7FBf074497C23",
                "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "PEPE": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
                "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
            },
            "protocol_addresses": {
                "uniswap_v3_factory": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
                "compound_comptroller": "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",
                "aave_v3_pool": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
            },
            "well_known_ens": {
                "vitalik.eth": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
                "ethereum.eth": "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359",
                "buterin.eth": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
            }
        }
    
    def resolve_ens_name(self, ens_name: str) -> Optional[str]:
        """Resolve ENS name to Ethereum address"""
        try:
            # Check if it's a known ENS name first
            if ens_name.lower() in self.blockchain_knowledge["well_known_ens"]:
                return self.blockchain_knowledge["well_known_ens"][ens_name.lower()]
            
            # Validate ENS name format
            if not ens_name.endswith(('.eth', '.xyz', '.crypto', '.nft', '.dao')):
                return None
            
            # Resolve using Web3 if available
            if self.w3:
                address = self.w3.ens.address(ens_name)
                return address if address else None
            else:
                return None
        except Exception as e:
            print(f"ENS resolution failed for {ens_name}: {str(e)}")
            return None
    
    def extract_and_resolve_addresses(self, query: str) -> List[ExtractedEntity]:
        """Extract both regular addresses and ENS names, resolving ENS to addresses"""
        entities = []
        
        # Extract regular Ethereum addresses
        addresses = re.findall(r'0x[a-fA-F0-9]{40}', query)
        for addr in addresses:
            entities.append(ExtractedEntity("address", addr, 0.95))
        
        # Extract potential ENS names
        ens_pattern = r'\b([a-zA-Z0-9-]+\.(?:eth|xyz|crypto|nft|dao))\b'
        ens_names = re.findall(ens_pattern, query, re.IGNORECASE)
        
        for ens_name in ens_names:
            resolved_address = self.resolve_ens_name(ens_name)
            if resolved_address:
                entities.append(ExtractedEntity("address", resolved_address, 0.9))
                entities.append(ExtractedEntity("ens_name", ens_name, 0.9))
            else:
                entities.append(ExtractedEntity("ens_name", ens_name, 0.5))  # Lower confidence if not resolved
        
        return entities
    
    def understand_query(self, natural_language_query: str) -> QueryUnderstanding:
        """Use LLM to understand natural language blockchain query"""
        
        system_prompt = """You are an expert blockchain data analyst. Analyze the user's natural language query and extract:

1. Intent classification (wallet_analysis, token_analytics, contract_intelligence, defi_operations, cross_chain_analysis)
2. Entities (addresses, tokens, protocols, timeframes, metrics)
3. Query complexity (simple, medium, complex)
4. Whether cross-API data correlation is needed

Return a structured JSON response with your analysis."""

        user_prompt = f"""
        Analyze this blockchain query: "{natural_language_query}"
        
        Consider these aspects:
        - What type of blockchain data is being requested?
        - What specific entities (addresses, tokens, protocols) are mentioned?
        - What timeframe is specified or implied?
        - What metrics or calculations are needed?
        - Does this require data from multiple sources?
        
        Provide your analysis in this JSON format:
        {{
            "intent": "wallet_analysis|token_analytics|contract_intelligence|defi_operations|cross_chain_analysis",
            "entities": [
                {{"type": "address|token|protocol|timeframe|metric", "value": "extracted_value", "confidence": 0.0-1.0}}
            ],
            "timeframe": "extracted_timeframe_or_null",
            "metrics": ["list", "of", "requested", "metrics"],
            "complexity": "simple|medium|complex",
            "requires_correlation": true|false
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Add extracted addresses and ENS names
            address_entities = self.extract_and_resolve_addresses(natural_language_query)
            all_entities = [ExtractedEntity(**entity) for entity in analysis["entities"]] + address_entities
            
            return QueryUnderstanding(
                intent=QueryIntent(analysis["intent"]),
                entities=all_entities,
                timeframe=analysis.get("timeframe"),
                metrics=analysis["metrics"],
                complexity=analysis["complexity"],
                requires_correlation=analysis["requires_correlation"]
            )
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            # Fallback to pattern matching if LLM fails
            return self._fallback_pattern_matching(natural_language_query)
    
    def _fallback_pattern_matching(self, query: str) -> QueryUnderstanding:
        """Fallback pattern matching for query understanding"""
        # Extract addresses and ENS names
        entities = self.extract_and_resolve_addresses(query)
        
        # Simple intent classification
        if any(word in query.lower() for word in ['balance', 'wallet', 'holdings']):
            intent = QueryIntent.WALLET_ANALYSIS
        elif any(word in query.lower() for word in ['token', 'price', 'volume']):
            intent = QueryIntent.TOKEN_ANALYTICS
        elif any(word in query.lower() for word in ['defi', 'liquidity', 'yield', 'apy']):
            intent = QueryIntent.DEFI_OPERATIONS
        else:
            intent = QueryIntent.WALLET_ANALYSIS
        
        return QueryUnderstanding(
            intent=intent,
            entities=entities,
            timeframe=None,
            metrics=[],
            complexity="simple",
            requires_correlation=False
        )
