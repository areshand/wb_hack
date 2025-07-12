Perfect. Here’s a structured, developer-friendly PRD broken down so it can be directly translated into implementation tasks. You can easily paste this into Notion, Linear, Trello, or GitHub issues.

⸻

🚀 PRD: Blockchain AI Assistant — 1-Day Hackathon Demo

🎯 Goal

Build a minimal AI assistant that answers 5 pre-defined blockchain questions using:
	•	Natural language input
	•	LLM-based prompt → Moralis API call conversion (via templates or few-shot)
	•	MCP-wrapped Moralis Web3 API endpoints
	•	Simple local UI (CLI or Web)

Target: working demo in 1 day

⸻

🔍 Use Cases (Fixed)

The system will only support the following prompts:

ID	Prompt	Expected Output
1	“What’s the current balance of wallet 0xabc...?”	ETH + ERC-20 balances
2	“List the last 10 transactions for address 0xabc...”	Table with txn hash, time, value
3	“Which addresses interacted with contract 0x123... in the past 24 hours?”	Wallet list
4	“What’s the 24-hour transfer volume of token PEPE?”	Volume in PEPE + USD
5	“Which wallets received NFTs from 0xcollection... last week?”	Wallet list + token IDs

These can be implemented via:
	•	Templated Moralis API calls
	•	Few-shot prompting
	•	Static Moralis API documentation knowledge

⸻

🛠️ Components & Implementation Tasks

1. MCP Setup

Goal: Serve Moralis Web3 API endpoints via MCP

Tasks:
	•	Set up Moralis Web3 API key and account
	•	Wrap Moralis REST API endpoints in local MCP config
	•	Configure MCP server to expose Moralis endpoints for:
		- Wallet balances (native + ERC-20 tokens)
		- Transaction history
		- Contract interactions
		- Token transfers and volumes
		- NFT transfers
	•	Test manual API calls through MCP wrapper

Deliverable: mcp-config.json with Moralis API integration + verified endpoints

⸻

2. Prompt → API Call Converter

Goal: Convert user prompt to Moralis API calls using templates or prompt chaining

Tasks:
	•	Define 5 Moralis API endpoint calls (1 per use case):
		- GET /wallets/{address}/balance (native + ERC-20)
		- GET /wallets/{address}/history (transaction history)
		- GET /contracts/{address}/logs (contract interactions)
		- GET /erc20/{address}/transfers (token volume analysis)
		- GET /nft/transfers (NFT transfer tracking)
	•	Create few-shot prompt examples OR static API call templates
	•	Implement a simple converter (can be if prompt contains + match logic)
	•	Test LLM generation of API calls against Moralis documentation

Deliverable: query_builder.py or convert_prompt(prompt_str) function

⸻

3. Moralis API Query Runner

Goal: Given an API call, send to Moralis via MCP endpoint and return response

Tasks:
	•	Implement run_moralis_query(endpoint, params) function
	•	Handle Moralis API authentication and rate limits
	•	Handle errors, timeouts, and API response codes
	•	Parse Moralis JSON responses into clean output format (HTML/markdown table or JSON)
	•	Format blockchain data (addresses, transaction hashes, token amounts) for readability

Deliverable: moralis_runner.py

⸻

4. UI Layer (CLI or Chat UI)

Goal: Let user input prompt and see answer

Tasks:
	•	Build a simple CLI or Streamlit app
	•	Allow typing or pasting a prompt
	•	Display both output and raw Moralis API call (optional)
	•	Format results in a readable table

Deliverable: app.py or streamlit_app.py

⸻

5. Demo Script / Testing

Goal: Validate demo and ensure smooth flow

Tasks:
	•	Write out a full script: what to type, what to expect
	•	Hardcode test wallet/contract/token addresses in UI or config
	•	Validate all 5 use cases give usable, correct responses
	•	Record 30–60 sec walkthrough video (optional)

Deliverable: demo.md + test screenshots or screencast

⸻

📦 File Structure Proposal

/blockchain-ai-demo
├── app.py                 # Main UI or CLI app
├── mcp-config.json        # Moralis API MCP wrapper config
├── query_builder.py       # Prompt to Moralis API call conversion
├── moralis_runner.py      # Sends API calls to Moralis and returns parsed result
├── demo.md                # Scripted demo instructions
├── requirements.txt       # deps (e.g., openai, requests, streamlit, moralis)
└── README.md              # Brief intro + how to run


⸻

✅ Success Criteria
	•	All 5 prompts produce correct live responses using Moralis Web3 API
	•	Each Moralis API call goes through MCP server
	•	Blockchain data (balances, transactions, contracts) is accurately retrieved and formatted
	•	Answers are formatted clearly in CLI or web interface
	•	Demo is reproducible from local setup with Moralis API key

⸻

Let me know if you’d like this exported to README.md, GitHub Issues, or as a task board!
