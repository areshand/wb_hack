# 🚀 Blockchain AI Assistant - Execution Guide

This document provides step-by-step instructions to implement the advanced Blockchain AI Assistant that translates natural language questions into real GraphQL queries as outlined in the PRD.

## 📋 Prerequisites

1. **API Keys Setup**
   - **OpenAI API**: Sign up at [platform.openai.com](https://platform.openai.com) for LLM capabilities
   - **The Graph API**: Get API key from [thegraph.com](https://thegraph.com) for GraphQL data access
   - **Moralis API**: Sign up at [moralis.io](https://moralis.io) for real-time blockchain data
   - **CoinGecko API**: Get free API key from [coingecko.com](https://coingecko.com) for price data
   - **OpenSea API**: Register at [opensea.io/developers](https://opensea.io/developers) for NFT data

2. **Development Environment**
   - Python 3.9+ installed
   - Node.js 18+ (for MCP servers and GraphQL tooling)
   - Docker & Docker Compose (for local development environment)
   - Git initialized (already done)
   - Code editor (VS Code recommended with GraphQL extensions)

## 🏗️ Implementation Steps

### Step 1: Enhanced Project Structure Setup

Create the advanced project structure:

```bash
mkdir -p src config schemas tests examples
touch src/__init__.py
touch src/intelligent_query_processor.py
touch src/graphql_query_builder.py
touch src/multi_api_aggregator.py
touch src/result_synthesizer.py
touch src/advanced_web_app.py
touch src/blockchain_schema_manager.py
touch src/data_correlation_engine.py
touch config/mcp-config.json
touch config/subgraph-endpoints.json
touch config/api-keys.env
touch examples/sample_queries.md
touch examples/expected_outputs.json
touch docker-compose.yml
touch requirements.txt
```

### Step 2: Enhanced Dependencies Installation

Create `requirements.txt` with advanced dependencies:

```txt
# Core LLM and AI
openai>=1.0.0
anthropic>=0.8.0
langchain>=0.1.0
langchain-openai>=0.0.5

# GraphQL and API clients
graphql-core>=3.2.0
gql>=3.4.0
aiohttp>=3.8.0
requests>=2.31.0

# Blockchain and Web3
web3>=6.0.0
moralis>=0.1.0
eth-account>=0.9.0

# Data processing and analysis
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
streamlit>=1.28.0

# Utilities
python-dotenv>=1.0.0
click>=8.1.0
tabulate>=0.9.0
pydantic>=2.0.0
asyncio>=3.4.3
redis>=4.5.0
celery>=5.3.0

# Development and testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Comprehensive Environment Configuration

Create `config/api-keys.env`:
```bash
# LLM APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Blockchain Data APIs
MORALIS_API_KEY=your_moralis_api_key_here
THE_GRAPH_API_KEY=your_thegraph_api_key_here
ALCHEMY_API_KEY=your_alchemy_api_key_here

# Price and Market Data
COINGECKO_API_KEY=your_coingecko_api_key_here
COINMARKETCAP_API_KEY=your_coinmarketcap_api_key_here

# NFT and Marketplace Data
OPENSEA_API_KEY=your_opensea_api_key_here
RESERVOIR_API_KEY=your_reservoir_api_key_here

# Infrastructure
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://localhost/blockchain_ai
```

### Step 4: Advanced MCP Server Configuration

Create `config/mcp-config.json` for multi-API integration:

```json
{
  "mcpServers": {
    "thegraph": {
      "command": "node",
      "args": ["thegraph-mcp-server.js"],
      "env": {
        "THE_GRAPH_API_KEY": "${THE_GRAPH_API_KEY}"
      }
    },
    "moralis": {
      "command": "node", 
      "args": ["moralis-mcp-server.js"],
      "env": {
        "MORALIS_API_KEY": "${MORALIS_API_KEY}"
      }
    },
    "coingecko": {
      "command": "node",
      "args": ["coingecko-mcp-server.js"],
      "env": {
        "COINGECKO_API_KEY": "${COINGECKO_API_KEY}"
      }
    },
    "opensea": {
      "command": "node",
      "args": ["opensea-mcp-server.js"],
      "env": {
        "OPENSEA_API_KEY": "${OPENSEA_API_KEY}"
      }
    }
  }
}
```

Create `config/subgraph-endpoints.json`:

```json
{
  "uniswap-v3": {
    "url": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    "description": "Uniswap V3 pools, swaps, and liquidity data"
  },
  "compound-v2": {
    "url": "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2",
    "description": "Compound lending protocol data"
  },
  "aave-v3": {
    "url": "https://api.thegraph.com/subgraphs/name/aave/aave-v3-ethereum",
    "description": "Aave V3 lending and borrowing data"
  },
  "ens": {
    "url": "https://api.thegraph.com/subgraphs/name/ensdomains/ens",
    "description": "Ethereum Name Service domains and registrations"
  },
  "cryptopunks": {
    "url": "https://api.thegraph.com/subgraphs/name/cryptopunks/cryptopunks",
    "description": "CryptoPunks NFT collection data"
  }
}
```

### Step 5: OpenAI-Integrated Query Builder

Update `src/query_builder.py` to use OpenAI for intelligent query understanding:

```python
import re
import os
from typing import Dict, Optional, Tuple
from intelligent_query_processor import IntelligentQueryProcessor

class QueryBuilder:
    def __init__(self):
        # Initialize OpenAI-powered query processor
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'your_openai_api_key_here':
            self.intelligent_processor = IntelligentQueryProcessor(openai_key)
            self.use_ai = True
        else:
            self.intelligent_processor = None
            self.use_ai = False
            print("OpenAI API key not found, falling back to pattern matching")
        
        # Fallback patterns for when OpenAI is not available
        self.patterns = {
            'balance': r'balance.*(?:wallet|address).*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)',
            'transactions': r'transactions.*(?:address|wallet).*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)',
            'contract_interactions': r'interact.*contract.*(?:0x[a-fA-F0-9]{39,42}|[a-zA-Z0-9-]+\.eth)',
            'token_volume': r'volume.*token.*(\w+)'
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
```

### Key Features of OpenAI Integration:

1. **Intelligent Query Understanding**: Uses GPT-4 to understand any variation of blockchain questions
2. **Flexible Address Detection**: Handles 39-42 character Ethereum addresses
3. **ENS Resolution**: Supports vitalik.eth, ethereum.eth, buterin.eth
4. **Graceful Fallback**: Falls back to pattern matching if OpenAI API is unavailable
5. **Enhanced Error Handling**: Robust error handling with multiple fallback layers

### Step 6: Dynamic GraphQL Query Builder

Create `src/graphql_query_builder.py`:

```python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import asyncio
from typing import Dict, List, Optional
import json

class GraphQLQueryBuilder:
    def __init__(self, subgraph_endpoints: Dict[str, str]):
        self.subgraph_endpoints = subgraph_endpoints
        self.clients = {}
        self._initialize_clients()
        
    def _initialize_clients(self):
        """Initialize GraphQL clients for each subgraph"""
        for name, config in self.subgraph_endpoints.items():
            transport = AIOHTTPTransport(url=config["url"])
            self.clients[name] = Client(transport=transport, fetch_schema_from_transport=True)
    
    async def introspect_schema(self, subgraph_name: str) -> Dict:
        """Introspect GraphQL schema for a subgraph"""
        client = self.clients.get(subgraph_name)
        if not client:
            raise ValueError(f"Unknown subgraph: {subgraph_name}")
        
        introspection_query = gql("""
            query IntrospectionQuery {
                __schema {
                    types {
                        name
                        fields {
                            name
                            type {
                                name
                                kind
                            }
                        }
                    }
                }
            }
        """)
        
        result = await client.execute_async(introspection_query)
        return result
    
    def build_wallet_analysis_query(self, address: str, metrics: List[str]) -> Dict[str, str]:
        """Build GraphQL queries for wallet analysis"""
        queries = {}
        
        # Uniswap positions query
        if "liquidity" in metrics or "positions" in metrics:
            queries["uniswap-v3"] = f"""
                query WalletLiquidity {{
                    positions(where: {{owner: "{address.lower()}"}}, first: 100) {{
                        id
                        liquidity
                        depositedToken0
                        depositedToken1
                        withdrawnToken0
                        withdrawnToken1
                        collectedFeesToken0
                        collectedFeesToken1
                        pool {{
                            token0 {{
                                symbol
                                decimals
                            }}
                            token1 {{
                                symbol
                                decimals
                            }}
                        }}
                    }}
                }}
            """
        
        # ENS domains query
        if "domains" in metrics or "ens" in metrics:
            queries["ens"] = f"""
                query WalletDomains {{
                    domains(where: {{owner: "{address.lower()}"}}, first: 100) {{
                        name
                        labelName
                        createdAt
                        expiryDate
                        resolver {{
                            addr {{
                                id
                            }}
                        }}
                    }}
                }}
            """
        
        return queries
    
    def build_token_analytics_query(self, token_address: str, metrics: List[str]) -> Dict[str, str]:
        """Build GraphQL queries for token analytics"""
        queries = {}
        
        # Uniswap token data
        queries["uniswap-v3"] = f"""
            query TokenAnalytics {{
                token(id: "{token_address.lower()}") {{
                    symbol
                    name
                    decimals
                    totalSupply
                    volume
                    volumeUSD
                    txCount
                    poolCount
                    totalValueLocked
                    totalValueLockedUSD
                }}
                
                tokenDayDatas(
                    where: {{token: "{token_address.lower()}"}}
                    orderBy: date
                    orderDirection: desc
                    first: 30
                ) {{
                    date
                    volume
                    volumeUSD
                    totalValueLocked
                    totalValueLockedUSD
                    priceUSD
                }}
            }}
        """
        
        return queries
    
    def build_defi_operations_query(self, protocol: str, metrics: List[str]) -> Dict[str, str]:
        """Build GraphQL queries for DeFi operations"""
        queries = {}
        
        if protocol.lower() == "compound":
            queries["compound-v2"] = """
                query CompoundMetrics {
                    markets(first: 100) {
                        id
                        symbol
                        name
                        supplyRate
                        borrowRate
                        totalSupply
                        totalBorrows
                        cash
                        reserves
                        exchangeRate
                    }
                }
            """
        
        elif protocol.lower() == "aave":
            queries["aave-v3"] = """
                query AaveMetrics {
                    reserves(first: 100) {
                        id
                        symbol
                        name
                        liquidityRate
                        variableBorrowRate
                        stableBorrowRate
                        totalLiquidity
                        totalATokenSupply
                        totalCurrentVariableDebt
                        utilizationRate
                    }
                }
            """
        
        return queries
    
    async def execute_queries(self, queries: Dict[str, str]) -> Dict[str, Dict]:
        """Execute multiple GraphQL queries across different subgraphs"""
        results = {}
        
        for subgraph_name, query_string in queries.items():
            try:
                client = self.clients.get(subgraph_name)
                if client:
                    query = gql(query_string)
                    result = await client.execute_async(query)
                    results[subgraph_name] = result
            except Exception as e:
                results[subgraph_name] = {"error": str(e)}
        
        return results
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
# Advanced Demo Script

## Setup
1. Ensure all API keys are set in .env (OpenAI, Moralis, The Graph, Alchemy)
2. Run: `streamlit run src/advanced_web_app.py`
3. Open browser to localhost:8501

## Demo Flow

### Test 1: ENS Resolution & Wallet Balance
- **Input**: "What's the current balance of wallet vitalik.eth?"
- **Expected**: ENS resolution to address + ETH balance display
- **Features**: ENS name resolution, balance interpretation
- **API Calls**: ENS resolution + GET /wallets/{address}/balance

### Test 2: ENS Transaction History  
- **Input**: "Show me the transaction history for ethereum.eth"
- **Expected**: ENS resolution + formatted transaction list with human-readable amounts
- **Features**: ENS resolution, transaction data interpretation, gas fee analysis
- **API Calls**: ENS resolution + GET /wallets/{address}/history

### Test 3: Contract Interactions with Interpretation
- **Input**: "Which addresses interacted with the PEPE token contract recently?"
- **Expected**: List of addresses with interaction details and explanations
- **Features**: Contract address resolution, interaction analysis, data interpretation
- **API Call**: GET /contracts/{address}/logs with intelligent formatting

### Test 4: Token Analytics with GraphQL
- **Input**: "What's the trading volume and price trend for PEPE token over the last 30 days?"
- **Expected**: Volume data, price charts, and trend analysis
- **Features**: GraphQL query generation, data visualization, trend insights
- **API Call**: GraphQL query to Uniswap subgraph + price data interpretation

### Test 5: DeFi Protocol Comparison
- **Input**: "Compare yield rates between Compound and Aave protocols"
- **Expected**: Side-by-side comparison with recommendations
- **Features**: Multi-protocol data aggregation, intelligent comparison, actionable insights
- **API Calls**: Multiple GraphQL queries + cross-protocol analysis
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

### Step 7: Multi-API Data Aggregation Layer

Create `src/multi_api_aggregator.py`:

```python
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass

@dataclass
class APIResponse:
    source: str
    data: Dict[str, Any]
    success: bool
    error: Optional[str] = None

class MultiAPIAggregator:
    def __init__(self, api_configs: Dict[str, Dict]):
        self.api_configs = api_configs
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def aggregate_data(self, query_plan: Dict[str, Any]) -> List[APIResponse]:
        """Aggregate data from multiple APIs based on query plan"""
        tasks = []
        
        # GraphQL queries
        if "graphql_queries" in query_plan:
            for subgraph, query in query_plan["graphql_queries"].items():
                tasks.append(self._execute_graphql_query(subgraph, query))
        
        # REST API calls
        if "rest_calls" in query_plan:
            for api_name, call_config in query_plan["rest_calls"].items():
                tasks.append(self._execute_rest_call(api_name, call_config))
        
        # Execute all queries concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process responses
        api_responses = []
        for response in responses:
            if isinstance(response, Exception):
                api_responses.append(APIResponse(
                    source="unknown",
                    data={},
                    success=False,
                    error=str(response)
                ))
            else:
                api_responses.append(response)
        
        return api_responses
    
    async def _execute_graphql_query(self, subgraph: str, query: str) -> APIResponse:
        """Execute GraphQL query against subgraph"""
        config = self.api_configs.get("thegraph", {})
        url = config.get("endpoints", {}).get(subgraph)
        
        if not url:
            return APIResponse(
                source=subgraph,
                data={},
                success=False,
                error=f"No endpoint configured for {subgraph}"
            )
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if config.get("api_key"):
            headers["Authorization"] = f"Bearer {config['api_key']}"
        
        payload = {
            "query": query
        }
        
        try:
            async with self.session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                return APIResponse(
                    source=subgraph,
                    data=data,
                    success=response.status == 200
                )
        except Exception as e:
            return APIResponse(
                source=subgraph,
                data={},
                success=False,
                error=str(e)
            )
    
    async def _execute_rest_call(self, api_name: str, call_config: Dict) -> APIResponse:
        """Execute REST API call"""
        config = self.api_configs.get(api_name, {})
        base_url = config.get("base_url", "")
        
        url = f"{base_url}/{call_config['endpoint']}"
        headers = config.get("headers", {})
        
        try:
            async with self.session.request(
                call_config.get("method", "GET"),
                url,
                params=call_config.get("params", {}),
                headers=headers
            ) as response:
                data = await response.json()
                return APIResponse(
                    source=api_name,
                    data=data,
                    success=response.status == 200
                )
        except Exception as e:
            return APIResponse(
                source=api_name,
                data={},
                success=False,
                error=str(e)
            )
```

### Step 8: Result Synthesis & Formatting

Create `src/result_synthesizer.py`:

```python
import openai
from typing import Dict, List, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass

@dataclass
class SynthesizedResult:
    summary: str
    insights: List[str]
    visualizations: List[Dict]
    raw_data: Dict[str, Any]
    recommendations: List[str]

class ResultSynthesizer:
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
    
    def synthesize_results(self, 
                         api_responses: List[Any], 
                         original_query: str,
                         query_intent: str) -> SynthesizedResult:
        """Synthesize results from multiple API responses"""
        
        # Combine all successful responses
        combined_data = {}
        for response in api_responses:
            if response.success:
                combined_data[response.source] = response.data
        
        # Generate natural language summary
        summary = self._generate_summary(combined_data, original_query)
        
        # Extract insights
        insights = self._extract_insights(combined_data, query_intent)
        
        # Create visualizations
        visualizations = self._create_visualizations(combined_data, query_intent)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(combined_data, query_intent)
        
        return SynthesizedResult(
            summary=summary,
            insights=insights,
            visualizations=visualizations,
            raw_data=combined_data,
            recommendations=recommendations
        )
    
    def _generate_summary(self, data: Dict[str, Any], original_query: str) -> str:
        """Generate natural language summary using LLM with blockchain context"""
        
        system_prompt = """You are an expert blockchain data analyst. Provide a clear, concise summary of blockchain data analysis results. 

Key responsibilities:
- Interpret raw blockchain data (wei amounts, timestamps, hex values) into human-readable format
- Explain gas fees, transaction costs, and token amounts in context
- Provide insights about wallet behavior, trading patterns, and DeFi activities
- Convert technical blockchain concepts into accessible language
- Highlight significant findings and anomalies in the data"""
        
        # Pre-process data for better interpretation
        interpreted_data = self._interpret_blockchain_data(data)
        
        user_prompt = f"""
        Original query: "{original_query}"
        
        Raw blockchain data analysis results:
        {json.dumps(data, indent=2)[:1500]}...
        
        Interpreted blockchain data:
        {json.dumps(interpreted_data, indent=2)[:1500]}...
        
        Provide a comprehensive summary that:
        1. Explains what the data means in plain English
        2. Highlights key insights and patterns
        3. Interprets numerical values (token amounts, USD values, percentages)
        4. Explains any significant blockchain-specific findings
        5. Provides context for the user's original question
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=700
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def _interpret_blockchain_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret raw blockchain data into human-readable format"""
        interpreted = {}
        
        for source, source_data in data.items():
            interpreted[source] = {}
            
            if source == "moralis" and isinstance(source_data, dict):
                # Interpret Moralis API responses
                if "balance" in source_data:
                    balance_wei = int(source_data.get("balance", 0))
                    balance_eth = balance_wei / 1e18
                    interpreted[source]["balance"] = {
                        "wei": balance_wei,
                        "eth": round(balance_eth, 6),
                        "usd_estimate": round(balance_eth * 2000, 2)  # Rough ETH price estimate
                    }
                
                if "result" in source_data and isinstance(source_data["result"], list):
                    # Interpret transaction data
                    transactions = source_data["result"]
                    interpreted_txs = []
                    
                    for tx in transactions[:10]:  # Limit to 10 transactions
                        interpreted_tx = {
                            "hash": tx.get("hash", ""),
                            "value_wei": int(tx.get("value", 0)),
                            "value_eth": int(tx.get("value", 0)) / 1e18,
                            "gas_used": tx.get("gas_used", ""),
                            "gas_price": tx.get("gas_price", ""),
                            "timestamp": tx.get("block_timestamp", ""),
                            "from_address": tx.get("from_address", ""),
                            "to_address": tx.get("to_address", "")
                        }
                        
                        # Calculate gas fee
                        if tx.get("gas_used") and tx.get("gas_price"):
                            gas_fee_wei = int(tx.get("gas_used", 0)) * int(tx.get("gas_price", 0))
                            interpreted_tx["gas_fee_eth"] = gas_fee_wei / 1e18
                            interpreted_tx["gas_fee_usd"] = (gas_fee_wei / 1e18) * 2000
                        
                        interpreted_txs.append(interpreted_tx)
                    
                    interpreted[source]["transactions"] = interpreted_txs
            
            elif "uniswap" in source and isinstance(source_data, dict):
                # Interpret Uniswap GraphQL data
                if "data" in source_data:
                    uniswap_data = source_data["data"]
                    
                    if "token" in uniswap_data:
                        token = uniswap_data["token"]
                        interpreted[source]["token_info"] = {
                            "name": token.get("name", "Unknown"),
                            "symbol": token.get("symbol", "N/A"),
                            "total_volume_usd": float(token.get("volumeUSD", 0)),
                            "total_value_locked_usd": float(token.get("totalValueLockedUSD", 0)),
                            "transaction_count": int(token.get("txCount", 0))
                        }
                    
                    if "tokenDayDatas" in uniswap_data:
                        day_data = uniswap_data["tokenDayDatas"]
                        interpreted_days = []
                        
                        for day in day_data[:7]:  # Last 7 days
                            interpreted_day = {
                                "date": day.get("date", ""),
                                "volume_usd": float(day.get("volumeUSD", 0)),
                                "price_usd": float(day.get("priceUSD", 0)),
                                "tvl_usd": float(day.get("totalValueLockedUSD", 0))
                            }
                            interpreted_days.append(interpreted_day)
                        
                        interpreted[source]["recent_activity"] = interpreted_days
        
        return interpreted
    
    def _extract_insights(self, data: Dict[str, Any], intent: str) -> List[str]:
        """Extract key insights from the data"""
        insights = []
        
        # Intent-specific insight extraction
        if intent == "wallet_analysis":
            insights.extend(self._wallet_insights(data))
        elif intent == "token_analytics":
            insights.extend(self._token_insights(data))
        elif intent == "defi_operations":
            insights.extend(self._defi_insights(data))
        
        return insights
    
    def _wallet_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract wallet-specific insights"""
        insights = []
        
        # Analyze Uniswap positions
        if "uniswap-v3" in data and "positions" in data["uniswap-v3"].get("data", {}):
            positions = data["uniswap-v3"]["data"]["positions"]
            if positions:
                insights.append(f"Wallet has {len(positions)} active liquidity positions on Uniswap V3")
                
                total_liquidity = sum(float(p.get("liquidity", 0)) for p in positions)
                if total_liquidity > 0:
                    insights.append(f"Total liquidity provided: {total_liquidity:.2e}")
        
        # Analyze ENS domains
        if "ens" in data and "domains" in data["ens"].get("data", {}):
            domains = data["ens"]["data"]["domains"]
            if domains:
                insights.append(f"Wallet owns {len(domains)} ENS domain(s)")
        
        return insights
    
    def _token_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract token-specific insights"""
        insights = []
        
        if "uniswap-v3" in data and "token" in data["uniswap-v3"].get("data", {}):
            token_data = data["uniswap-v3"]["data"]["token"]
            if token_data:
                insights.append(f"Token: {token_data.get('name', 'Unknown')} ({token_data.get('symbol', 'N/A')})")
                
                volume_usd = float(token_data.get("volumeUSD", 0))
                if volume_usd > 0:
                    insights.append(f"Total trading volume: ${volume_usd:,.2f}")
                
                tvl_usd = float(token_data.get("totalValueLockedUSD", 0))
                if tvl_usd > 0:
                    insights.append(f"Total Value Locked: ${tvl_usd:,.2f}")
        
        return insights
    
    def _defi_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract DeFi-specific insights"""
        insights = []
        
        # Compound insights
        if "compound-v2" in data and "markets" in data["compound-v2"].get("data", {}):
            markets = data["compound-v2"]["data"]["markets"]
            if markets:
                avg_supply_rate = sum(float(m.get("supplyRate", 0)) for m in markets) / len(markets)
                insights.append(f"Average Compound supply rate: {avg_supply_rate:.4%}")
        
        # Aave insights
        if "aave-v3" in data and "reserves" in data["aave-v3"].get("data", {}):
            reserves = data["aave-v3"]["data"]["reserves"]
            if reserves:
                avg_liquidity_rate = sum(float(r.get("liquidityRate", 0)) for r in reserves) / len(reserves)
                insights.append(f"Average Aave liquidity rate: {avg_liquidity_rate:.4%}")
        
        return insights
    
    def _create_visualizations(self, data: Dict[str, Any], intent: str) -> List[Dict]:
        """Create data visualizations"""
        visualizations = []
        
        # Token price chart
        if "uniswap-v3" in data and "tokenDayDatas" in data["uniswap-v3"].get("data", {}):
            day_data = data["uniswap-v3"]["data"]["tokenDayDatas"]
            if day_data:
                df = pd.DataFrame(day_data)
                df['date'] = pd.to_datetime(df['date'], unit='s')
                df['priceUSD'] = pd.to_numeric(df['priceUSD'], errors='coerce')
                
                fig = px.line(df, x='date', y='priceUSD', title='Token Price Over Time')
                visualizations.append({
                    "type": "line_chart",
                    "title": "Token Price History",
                    "data": fig.to_json()
                })
        
        return visualizations
    
    def _generate_recommendations(self, data: Dict[str, Any], intent: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if intent == "defi_operations":
            # Compare rates across protocols
            compound_rates = []
            aave_rates = []
            
            if "compound-v2" in data:
                markets = data["compound-v2"].get("data", {}).get("markets", [])
                compound_rates = [float(m.get("supplyRate", 0)) for m in markets]
            
            if "aave-v3" in data:
                reserves = data["aave-v3"].get("data", {}).get("reserves", [])
                aave_rates = [float(r.get("liquidityRate", 0)) for r in reserves]
            
            if compound_rates and aave_rates:
                avg_compound = sum(compound_rates) / len(compound_rates)
                avg_aave = sum(aave_rates) / len(aave_rates)
                
                if avg_aave > avg_compound:
                    recommendations.append("Consider Aave for higher average yields")
                else:
                    recommendations.append("Consider Compound for higher average yields")
        
        return recommendations

### Step 9: Advanced Web Application

Create `src/advanced_web_app.py`:

```python
import streamlit as st
import asyncio
import json
import plotly.graph_objects as go
from intelligent_query_processor import IntelligentQueryProcessor
from graphql_query_builder import GraphQLQueryBuilder
from multi_api_aggregator import MultiAPIAggregator
from result_synthesizer import ResultSynthesizer
import os
from dotenv import load_dotenv

load_dotenv()

class AdvancedBlockchainAI:
    def __init__(self):
        self.query_processor = IntelligentQueryProcessor(os.getenv("OPENAI_API_KEY"))
        
        # Load subgraph endpoints
        with open("config/subgraph-endpoints.json", "r") as f:
            subgraph_endpoints = json.load(f)
        
        self.graphql_builder = GraphQLQueryBuilder(subgraph_endpoints)
        self.result_synthesizer = ResultSynthesizer(os.getenv("OPENAI_API_KEY"))
        
        # API configurations
        self.api_configs = {
            "thegraph": {
                "api_key": os.getenv("THE_GRAPH_API_KEY"),
                "endpoints": subgraph_endpoints
            },
            "moralis": {
                "base_url": "https://deep-index.moralis.io/api/v2.2",
                "headers": {"X-API-Key": os.getenv("MORALIS_API_KEY")}
            }
        }
    
    async def process_query(self, natural_language_query: str):
        """Process natural language query end-to-end"""
        
        # Step 1: Understand the query
        understanding = self.query_processor.understand_query(natural_language_query)
        
        # Step 2: Build GraphQL queries
        queries = {}
        
        if understanding.intent.value == "wallet_analysis":
            address = next((e.value for e in understanding.entities if e.type == "address"), None)
            if address:
                queries = self.graphql_builder.build_wallet_analysis_query(address, understanding.metrics)
        
        elif understanding.intent.value == "token_analytics":
            token = next((e.value for e in understanding.entities if e.type == "token"), None)
            if token:
                # Convert token symbol to address if needed
                token_address = self.query_processor.blockchain_knowledge["token_addresses"].get(token.upper(), token)
                queries = self.graphql_builder.build_token_analytics_query(token_address, understanding.metrics)
        
        elif understanding.intent.value == "defi_operations":
            protocol = next((e.value for e in understanding.entities if e.type == "protocol"), None)
            if protocol:
                queries = self.graphql_builder.build_defi_operations_query(protocol, understanding.metrics)
        
        # Step 3: Execute queries
        query_plan = {"graphql_queries": queries}
        
        async with MultiAPIAggregator(self.api_configs) as aggregator:
            api_responses = await aggregator.aggregate_data(query_plan)
        
        # Step 4: Synthesize results
        result = self.result_synthesizer.synthesize_results(
            api_responses, 
            natural_language_query, 
            understanding.intent.value
        )
        
        return understanding, result

def main():
    st.set_page_config(
        page_title="Advanced Blockchain AI Assistant",
        page_icon="🔗",
        layout="wide"
    )
    
    st.title("🔗 Advanced Blockchain AI Assistant")
    st.markdown("*Powered by LLM + GraphQL + Multi-API Intelligence*")
    
    # Initialize the AI assistant
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AdvancedBlockchainAI()
    
    # Sidebar with advanced examples
    st.sidebar.header("🚀 Advanced Query Examples")
    
    advanced_examples = [
        "Show me all DeFi positions for wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "What's the trading volume and price trend for PEPE token over the last 30 days?",
        "Compare yield rates between Compound and Aave protocols",
        "Find the largest Uniswap V3 liquidity providers for USDC/ETH",
        "Show me ENS domains owned by 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    ]
    
    for i, example in enumerate(advanced_examples):
        if st.sidebar.button(f"Example {i+1}", key=f"example_{i}"):
            st.session_state.user_query = example
    
    # Main query interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "Enter your blockchain question:",
            value=st.session_state.get('user_query', ''),
            height=120,
            placeholder="Ask anything about blockchain data - wallets, tokens, DeFi, NFTs..."
        )
    
    with col2:
        st.markdown("### Query Understanding")
        st.markdown("The AI will:")
        st.markdown("- 🧠 Understand your intent")
        st.markdown("- 🔍 Extract entities & metrics")
        st.markdown("- 📊 Generate GraphQL queries")
        st.markdown("- 🔗 Aggregate multi-API data")
        st.markdown("- 💡 Synthesize insights")
    
    if st.button("🚀 Analyze", type="primary", use_container_width=True):
        if user_query:
            with st.spinner("🔍 Processing your query with advanced AI..."):
                try:
                    # Run async query processing
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    understanding, result = loop.run_until_complete(
                        st.session_state.ai_assistant.process_query(user_query)
                    )
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Query Understanding
                    with st.expander("🧠 Query Understanding", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Intent", understanding.intent.value.replace("_", " ").title())
                        
                        with col2:
                            st.metric("Complexity", understanding.complexity.title())
                        
                        with col3:
                            st.metric("Entities Found", len(understanding.entities))
                        
                        if understanding.entities:
                            st.markdown("**Extracted Entities:**")
                            for entity in understanding.entities:
                                st.markdown(f"- {entity.type}: `{entity.value}` (confidence: {entity.confidence:.2f})")
                    
                    # Results Summary
                    st.markdown("### 📊 Analysis Summary")
                    st.markdown(result.summary)
                    
                    # Key Insights
                    if result.insights:
                        st.markdown("### 💡 Key Insights")
                        for insight in result.insights:
                            st.markdown(f"- {insight}")
                    
                    # Visualizations
                    if result.visualizations:
                        st.markdown("### 📈 Visualizations")
                        for viz in result.visualizations:
                            st.plotly_chart(json.loads(viz["data"]), use_container_width=True)
                    
                    # Recommendations
                    if result.recommendations:
                        st.markdown("### 🎯 Recommendations")
                        for rec in result.recommendations:
                            st.markdown(f"- {rec}")
                    
                    # Raw Data
                    with st.expander("🔍 Raw Data"):
                        st.json(result.raw_data)
                
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.markdown("Please try a different query or check your API keys.")
        else:
            st.warning("Please enter a question to analyze.")

if __name__ == "__main__":
    main()
```

## 🚀 Running the Advanced Application

### Development Environment Setup
```bash
# Start Redis (for caching)
docker run -d -p 6379:6379 redis:alpine

# Install all dependencies
pip install -r requirements.txt

# Set up environment variables
cp config/api-keys.env .env
# Edit .env with your actual API keys
```

### Launch the Advanced Web App
```bash
streamlit run src/advanced_web_app.py
```

### Docker Development Environment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8501
```

## 🔧 Advanced Troubleshooting

### Common Issues:
1. **GraphQL Schema Errors**: Ensure subgraph endpoints are accessible
2. **LLM API Limits**: Monitor OpenAI usage and implement rate limiting
3. **Async Issues**: Ensure proper event loop handling in Streamlit
4. **Memory Usage**: Implement result caching for large datasets
5. **API Rate Limits**: Implement exponential backoff and request queuing

### Performance Optimization:
```python
# Enable result caching
import redis
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

# Implement query result caching
@st.cache_data(ttl=300)  # 5-minute cache
def cached_query_execution(query_hash):
    # Your query execution logic
    pass
```

## 📝 Advanced Next Steps

1. **Real-time Data Streaming**: Implement WebSocket connections for live updates
2. **Advanced Analytics**: Add machine learning models for predictive insights
3. **Multi-chain Support**: Extend to Polygon, Arbitrum, Optimism, BSC
4. **Custom Dashboards**: Allow users to create and save custom dashboard views
5. **API Rate Optimization**: Implement intelligent query batching and caching
6. **Advanced Visualizations**: Add 3D network graphs and interactive charts

## ✅ Advanced Completion Checklist

- [ ] All API keys configured (OpenAI, The Graph, Moralis, CoinGecko, OpenSea)
- [ ] Advanced project structure created
- [ ] Enhanced dependencies installed
- [ ] LLM-powered query processor implemented
- [ ] Dynamic GraphQL query builder working
- [ ] Multi-API aggregation layer functional
- [ ] Result synthesis and formatting complete
- [ ] Advanced web application deployed
- [ ] Real-time capabilities tested
- [ ] Performance optimization implemented
- [ ] Comprehensive error handling added
- [ ] Advanced demo scenarios validated
