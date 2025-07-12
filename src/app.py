import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_builder import QueryBuilder
from moralis_runner import MoralisRunner

# Load environment variables
load_dotenv()

def main():
    st.title("🔗 Blockchain AI Assistant")
    st.write("Ask questions about blockchain data using natural language!")
    
    # Check API keys
    moralis_key = os.getenv('MORALIS_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not moralis_key or moralis_key == 'your_moralis_api_key_here':
        st.error("⚠️ Please configure your MORALIS_API_KEY in the .env file")
        st.info("1. Sign up at moralis.io\n2. Get your API key\n3. Update the .env file")
        return
    
    # Show AI status
    if openai_key and openai_key != 'your_openai_api_key_here':
        st.success("🤖 AI-Powered Query Understanding: ENABLED")
        st.info("Using OpenAI GPT-4 for intelligent query parsing - can handle any variation!")
    else:
        st.warning("🔍 Using Pattern Matching: Limited query understanding")
        st.info("Add OPENAI_API_KEY to .env for AI-powered query understanding")
    
    # Initialize components
    query_builder = QueryBuilder()
    moralis_runner = MoralisRunner()
    
    # Sample prompts with ENS support
    st.sidebar.header("Sample Prompts")
    sample_prompts = [
        "What's the current balance of wallet vitalik.eth?",
        "List the last 10 transactions for address ethereum.eth",
        "Show me the transaction history for buterin.eth",
        "Which addresses interacted with the PEPE token contract recently?",
        "What's the 24-hour transfer volume of token PEPE?"
    ]
    
    st.sidebar.markdown("### ENS Support")
    st.sidebar.markdown("✅ vitalik.eth")
    st.sidebar.markdown("✅ ethereum.eth") 
    st.sidebar.markdown("✅ buterin.eth")
    st.sidebar.markdown("🔍 Auto-resolves to addresses")
    
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
    
    # Instructions
    with st.expander("How to use"):
        st.markdown("""
        **Supported Questions:**
        1. **Wallet Balance**: "What's the current balance of wallet vitalik.eth?" or "0x..."
        2. **Transaction History**: "List the last 10 transactions for address ethereum.eth"
        3. **Contract Interactions**: "Which addresses interacted with contract 0x... recently?"
        4. **Token Volume**: "What's the 24-hour transfer volume of token PEPE?"
        
        **ENS Support:**
        - ✅ vitalik.eth → Auto-resolves to Ethereum address
        - ✅ ethereum.eth → Auto-resolves to Ethereum address  
        - ✅ buterin.eth → Auto-resolves to Ethereum address
        
        **Tips:**
        - Use ENS names (like vitalik.eth) or Ethereum addresses (0x...)
        - Enhanced result interpretation with USD estimates and gas fees
        - Use the sample prompts as templates
        - Check that your Moralis API key is configured in the .env file
        """)

if __name__ == "__main__":
    main()
