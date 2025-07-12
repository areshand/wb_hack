import click
import os
import sys
from dotenv import load_dotenv
from tabulate import tabulate

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_builder import QueryBuilder
from moralis_runner import MoralisRunner

load_dotenv()

@click.command()
@click.option('--prompt', '-p', help='Natural language prompt')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(prompt, interactive):
    """Blockchain AI Assistant CLI"""
    
    # Check API key
    if not os.getenv('MORALIS_API_KEY') or os.getenv('MORALIS_API_KEY') == 'your_moralis_api_key_here':
        click.echo("❌ Please configure your MORALIS_API_KEY in the .env file")
        click.echo("1. Sign up at moralis.io")
        click.echo("2. Get your API key")
        click.echo("3. Update the .env file")
        return
    
    query_builder = QueryBuilder()
    moralis_runner = MoralisRunner()
    
    if interactive:
        click.echo("🔗 Blockchain AI Assistant (Interactive Mode)")
        click.echo("Type 'quit' to exit\n")
        
        # Show sample prompts
        click.echo("Sample prompts:")
        samples = [
            "What's the current balance of wallet 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?",
            "List the last 10 transactions for address 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b",
            "Which addresses interacted with contract 0x6982508145454Ce325dDbE47a25d4ec3d2311933 in the past 24 hours?",
            "What's the 24-hour transfer volume of token PEPE?",
            "Which wallets received NFTs from 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b last week?"
        ]
        
        for i, sample in enumerate(samples, 1):
            click.echo(f"{i}. {sample}")
        click.echo()
        
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
        click.echo("Example: python src/cli_app.py -p \"What's the balance of 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b?\"")

def process_query(user_input, query_builder, moralis_runner):
    """Process a single query"""
    click.echo(f"Question: {user_input}")
    
    # Build query
    query = query_builder.build_query(user_input)
    
    if query:
        click.echo(f"API Call: {query['endpoint']}")
        click.echo("Parameters:", nl=False)
        for key, value in query['params'].items():
            click.echo(f" {key}={value}", nl=False)
        click.echo()
        
        # Execute query
        with click.progressbar(length=1, label='Executing query') as bar:
            result = moralis_runner.run_query(query)
            bar.update(1)
        
        if result.get('success'):
            click.echo("✅ Success!")
            click.echo(result['formatted'])
        else:
            click.echo(f"❌ Error: {result.get('error', 'Unknown error')}")
            if 'message' in result:
                click.echo(f"Details: {result['message']}")
    else:
        click.echo("❌ Could not understand your question.")
        click.echo("Please try one of the supported question formats.")

if __name__ == "__main__":
    main()
