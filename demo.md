# Enhanced Demo Script with ENS Support

## Setup
1. Ensure Moralis API key is set in .env
2. Run: `streamlit run src/app.py`
3. Open browser to localhost:8501

## Demo Flow

### Test 1: ENS Resolution & Wallet Balance
- **Input**: "What's the current balance of wallet vitalik.eth?"
- **Expected**: ENS resolution to address + ETH balance with USD estimate and wallet classification
- **Features**: ENS name resolution, enhanced balance interpretation
- **API Call**: ENS resolution + GET /wallets/{address}/balance

### Test 2: ENS Transaction History  
- **Input**: "Show me the transaction history for ethereum.eth"
- **Expected**: ENS resolution + formatted transaction list with gas fees and timestamps
- **Features**: ENS resolution, transaction data interpretation, gas fee analysis
- **API Call**: ENS resolution + GET /wallets/{address}/history

### Test 3: Contract Interactions with Interpretation
- **Input**: "Which addresses interacted with the PEPE token contract recently?"
- **Expected**: List of addresses with interaction details and explanations
- **Features**: Contract address resolution, interaction analysis, data interpretation
- **API Call**: GET /contracts/{address}/logs with intelligent formatting

### Test 4: Token Volume Analysis
- **Input**: "What's the 24-hour transfer volume of token PEPE?"
- **Expected**: Volume data with transfer count and analysis
- **Features**: Token volume calculation, transfer pattern analysis
- **API Call**: GET /erc20/{address}/transfers with enhanced interpretation

### Test 5: ENS Name Variations
- **Input**: "List the last 10 transactions for address buterin.eth"
- **Expected**: ENS resolution + transaction history with enhanced formatting
- **Features**: Multiple ENS name support, consistent address resolution
- **API Call**: ENS resolution + GET /wallets/{address}/history

## Key Features Demonstrated

### ENS Resolution
- ✅ vitalik.eth → 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
- ✅ ethereum.eth → 0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359
- ✅ buterin.eth → 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

### Enhanced Result Interpretation
- 💰 Balance classification (High/Active/Regular/Low balance wallet)
- 💵 USD estimates for ETH amounts
- ⛽ Gas fee calculations and display
- 📅 Human-readable timestamps
- 📊 Transaction summaries and totals

### Improved User Experience
- 🔍 Auto-resolves ENS names to addresses
- 📈 Enhanced data visualization
- 💡 Contextual insights and explanations
- 🎯 Clear error handling and feedback

## CLI Demo Alternative

### Setup CLI
```bash
python src/cli_app.py -i
```

### Test Commands
```bash
# Single query
python src/cli_app.py -p "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?"

# Interactive mode
python src/cli_app.py -i
```

## Expected Outputs

### Wallet Balance Response
```
ETH Balance: 0.123456 ETH
```

### Transaction History Response
```
Recent Transactions:
- 0x1234567890...: 0.050000 ETH
- 0xabcdef1234...: 0.025000 ETH
- 0x9876543210...: 0.100000 ETH
```

### Contract Interactions Response
```
Unique addresses that interacted: 15
- 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b
- 0x1234567890abcdef1234567890abcdef12345678
- 0xabcdef1234567890abcdef1234567890abcdef12
```

### Token Volume Response
```
24h Transfer Volume: 1000000.00 tokens
Number of transfers: 250
```


## Troubleshooting Demo Issues

### Common Problems:
1. **API Key Not Set**: Update .env file with valid Moralis API key
2. **Invalid Address**: Ensure addresses are 42 characters (0x + 40 hex chars)
3. **Rate Limiting**: Wait between requests if hitting rate limits
4. **Network Issues**: Check internet connection

### Debug Steps:
1. Check .env file configuration
2. Verify Moralis API key is valid
3. Test with known valid Ethereum addresses
4. Check console for detailed error messages
