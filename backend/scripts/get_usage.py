import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from backend/.env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print(f"Error: SUPABASE_URL and SUPABASE_KEY must be set in {env_path}")
    exit(1)

supabase: Client = create_client(url, key)

async def get_usage(account_id: str = None):
    """Calls the Supabase RPC to get usage data and prints the result."""
    try:
        # Call the appropriate RPC function
        if account_id:
            response = supabase.rpc('get_llm_usage', {'account_id': account_id}).execute()
            title = f"--- Suna Usage for Account {account_id} ---"
        else:
            response = supabase.rpc('get_total_project_usage').execute()
            title = "--- Suna Project Usage ---"

        if response.data and len(response.data) > 0:
            usage_data = response.data[0]
            total_cost = usage_data.get('total_cost', 0)
            total_input_tokens = usage_data.get('total_input_tokens', 0)
            total_output_tokens = usage_data.get('total_output_tokens', 0)
            model = usage_data.get('model', 'N/A')

            print(title)
            print(f"Model: {model}")
            print(f"Total Cost: ${total_cost:.6f}")
            print(f"Total Input Tokens: {total_input_tokens}")
            print(f"Total Output Tokens: {total_output_tokens}")
            print("-" * len(title))
        else:
            print("No usage data found.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Get Suna LLM usage statistics')
    parser.add_argument('--account-id', type=str, help='Optional account ID to get specific account usage')
    args = parser.parse_args()

    # Supabase client is not async, but the execute method might be.
    # Using asyncio.run for compatibility if needed in the future,
    # though for simple RPC call it might not be strictly necessary.
    asyncio.run(get_usage(args.account_id))