# 🔗 Blockchain AI Assistant

An intelligent AI-powered assistant that translates natural language questions into blockchain queries with OpenAI integration, ENS resolution, and enhanced API result interpretation.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🤖 **AI-Powered Query Understanding**: Uses OpenAI GPT-4 for intelligent natural language processing
- 🔍 **ENS Resolution**: Supports vitalik.eth, ethereum.eth, buterin.eth with automatic address resolution
- 💰 **Enhanced Result Interpretation**: USD estimates, gas fees, wallet classification, human-readable data
- 🔄 **Flexible Address Detection**: Handles 39-42 character Ethereum addresses
- 🛡️ **Robust Fallback System**: Works even without OpenAI API key using pattern matching
- 🌐 **Multiple Interfaces**: Both web UI (Streamlit) and CLI support

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/areshand/wb_hack.git
cd wb_hack
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Moralis API for blockchain data
MORALIS_API_KEY=your_moralis_api_key_here

# Optional: OpenAI API for intelligent query understanding (recommended)
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Get API Keys

#### Required: Moralis API Key
1. Sign up at [moralis.io](https://moralis.io)
2. Create a new project
3. Copy your API key to the `.env` file

#### Recommended: OpenAI API Key
1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Create an API key
3. Add it to the `.env` file for intelligent query understanding

### 5. Run the Application

#### Option A: Web Interface (Recommended)
```bash
streamlit run src/app.py
```
Then open your browser to `http://localhost:8501`

#### Option B: Command Line Interface
```bash
# Interactive mode
python src/cli_app.py -i

# Single query
python src/cli_app.py -p "What's the current balance of wallet vitalik.eth?"
```

## 💡 Usage Examples

### Supported Query Types

The assistant can handle various blockchain questions:

```bash
# Wallet Balance (with ENS support)
"What's the current balance of wallet vitalik.eth?"
"Show me the balance for 0x3Cc19ad349C4afC532673CfA4a561517Aa7cfB84"

# Transaction History
"List the last 10 transactions for ethereum.eth"
"Show transaction history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

# Contract Interactions
"Which addresses interacted with the PEPE token contract recently?"

# Token Analytics
"What's the 24-hour transfer volume of token PEPE?"
```

### ENS Name Support

The system automatically resolves ENS names:
- ✅ `vitalik.eth` → `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
- ✅ `ethereum.eth` → `0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359`
- ✅ `buterin.eth` → `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
python tests/test_query_builder.py
```

Expected output: `OK` with all tests passing.

## 🔧 Configuration

### AI Mode vs Pattern Matching

The system operates in two modes:

1. **AI Mode** (with OpenAI API key):
   - Uses GPT-4 for intelligent query understanding
   - Handles any variation of blockchain questions
   - Provides enhanced entity extraction and intent classification

2. **Pattern Matching Mode** (fallback):
   - Uses keyword-based classification
   - Still handles most common query variations
   - Works without OpenAI API key

### Supported Blockchain Operations

- **Wallet Analysis**: Balance queries, transaction history
- **Token Analytics**: Volume analysis, transfer patterns
- **Contract Intelligence**: Interaction analysis, event logs
- **ENS Resolution**: Automatic domain-to-address conversion

## 📁 Project Structure

```
wb_hack/
├── src/
│   ├── app.py                          # Streamlit web interface
│   ├── cli_app.py                      # Command line interface
│   ├── query_builder.py                # Query processing with AI integration
│   ├── moralis_runner.py               # Blockchain API integration
│   └── intelligent_query_processor.py  # OpenAI-powered query understanding
├── config/
│   ├── mcp-config.json                 # MCP server configurations
│   └── subgraph-endpoints.json         # GraphQL endpoint configurations
├── tests/
│   └── test_query_builder.py           # Unit tests
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (create this)
├── PRD.md                              # Product Requirements Document
├── EXECUTION.md                        # Detailed implementation guide
└── demo.md                             # Demo script and examples
```

## 🛠️ Development

### Adding New Query Types

1. Update patterns in `src/query_builder.py`
2. Add corresponding API endpoints in `src/moralis_runner.py`
3. Update tests in `tests/test_query_builder.py`

### Extending ENS Support

Add new ENS domains to the `well_known_ens` dictionary in:
- `src/query_builder.py`
- `src/intelligent_query_processor.py`

## 🐛 Troubleshooting

### Common Issues

1. **"Could not understand your question"**
   - Ensure your query contains blockchain-related keywords (balance, transaction, etc.)
   - Try using one of the sample prompts
   - Add OpenAI API key for better query understanding

2. **"Please configure your MORALIS_API_KEY"**
   - Sign up at moralis.io and get your API key
   - Add it to the `.env` file
   - Restart the application

3. **OpenAI API errors**
   - Check your OpenAI API key is valid
   - Ensure you have sufficient credits
   - The system will fall back to pattern matching if OpenAI fails

4. **Address not recognized**
   - Ensure Ethereum addresses are 39-42 characters long
   - Check that addresses start with "0x"
   - Try using supported ENS names instead

### Debug Mode

For detailed debugging, check the console output when running the application. Error messages will indicate:
- Whether AI mode is enabled
- API key validation status
- Query processing steps

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [demo.md](demo.md) for usage examples
3. Open an issue on GitHub

## 🙏 Acknowledgments

- [Moralis](https://moralis.io) for blockchain API services
- [OpenAI](https://openai.com) for GPT-4 integration
- [Streamlit](https://streamlit.io) for the web interface
- [The Graph Protocol](https://thegraph.com) for GraphQL blockchain data

---

**Built with ❤️ for the blockchain community**
