import requests
import os
import re
import subprocess

# Function to get available Ollama models
def get_ollama_models():
    ollama_api_base = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
    try:
        response = requests.get(f"{ollama_api_base}/api/tags")
        response.raise_for_status() # Raise an exception for bad status codes
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ollama models: {e}")
        return []

# Function to read file content
def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

# Function to write file content
def write_file(filepath, content):
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Successfully updated {filepath}")
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")

# Function to update backend/agent/api.py
def update_api_file(model_name):
    filepath = "backend/agent/api.py"
    content = read_file(filepath)
    if content is None:
        return

    # Update AgentStartRequest
    # Find the line with model_name default
    # Example: model_name: Optional[str] = "anthropic/claude-3-7-sonnet-latest"
    # Example: model_name: Optional[str] = "perplexity/sonar-pro"
    # Example: model_name: Optional[str] = "ollama/<your_model_name>"

    # Use regex to find the line setting the default model_name in AgentStartRequest
    # This regex looks for 'model_name: Optional[str] = ' followed by any string in quotes
    # and captures the part after the equals sign.
    pattern_agent_start = r'(model_name:\s*Optional\[str\]\s*=\s*)"[^"]+"'
    replace_agent_start = rf'\g<1>"{model_name}"'
    content = re.sub(pattern_agent_start, replace_agent_start, content, count=1)

    # Update initiate_agent_with_files
    # Find the line with model_name default in Form(...)
    # Example: model_name: Optional[str] = Form("anthropic/claude-3-7-sonnet-latest"),
    # Example: model_name: Optional[str] = Form("perplexity/sonar-pro"),
    # Example: model_name: Optional[str] = Form("ollama/<your_model_name>"),

    # Use regex to find the line setting the default model_name in Form(...)
    # This regex looks for a line starting with optional whitespace, then 'model_name: Optional[str] = Form('
    # followed by any characters up to a quote, then captures the content within quotes,
    # and the rest of the line after the closing quote.
    pattern_initiate = r'^(\s*model_name:\s*Optional\[str\]\s*=\s*Form\()"[^"]+"(.*)$'
    replace_initiate = rf'\g<1>"{model_name}"\g<2>'
    content = re.sub(pattern_initiate, replace_initiate, content, count=1, flags=re.MULTILINE)

    write_file(filepath, content)

# Function to update backend/agentpress/context_manager.py
def update_context_manager_file(model_name):
    filepath = "backend/agentpress/context_manager.py"
    content = read_file(filepath)
    if content is None:
        return

    # Update create_summary function
    # Find the line with model default
    # Example: model: str = "openai/gpt-4o-mini" # Change this model name
    # Example: model: str = "perplexity/sonar-pro"
    # Example: model: str = "ollama/<your_model_name>"

    # Use regex to find the line setting the default model in create_summary
    # This regex looks for 'model:\s*str\s*=\s*"' followed by any string in quotes
    # and captures the part after the equals sign.
    import re
    pattern_summary = r'(model:\s*str\s*=\s*)"[^"]+"'
    replace_summary = rf'\g<1>"{model_name}"'
    content = re.sub(pattern_summary, replace_summary, content, count=1)

    write_file(filepath, content)

# Function to update backend/agentpress/thread_manager.py
def update_thread_manager_file(model_name):
    filepath = "backend/agentpress/thread_manager.py"
    content = read_file(filepath)
    if content is None:
        return

    # Update run_thread function
    # Find the line with llm_model default
    # Example: llm_model: str = "gpt-4o",
    # Example: llm_model: str = "anthropic/claude-3-7-sonnet-latest",
    # Example: llm_model: str = "perplexity/sonar-pro",
    # Example: llm_model: str = "ollama/<your_model_name>",

    # Use regex to find the line setting the default llm_model in run_thread
    pattern_thread_manager = r'(llm_model:\s*str\s*=\s*)"[^"]+"'
    replace_thread_manager = rf'\g<1>"{model_name}"'
    content = re.sub(pattern_thread_manager, replace_thread_manager, content, count=1)

    write_file(filepath, content)

# Function to update backend/agent/run.py
def update_run_file(model_name):
    filepath = "backend/agent/run.py"
    content = read_file(filepath)
    if content is None:
        return

    # Update run_agent function
    # Find the line with model_name default
    # Example: model_name: str = "anthropic/claude-3-7-sonnet-latest",
    # Example: model_name: str = "perplexity/sonar-pro",
    # Example: model_name: str = "ollama/<your_model_name>",

    # Use regex to find the line setting the default model_name in run_agent
    pattern_run_agent = r'(model_name:\s*str\s*=\s*)"[^"]+"'
    replace_run_agent = rf'\g<1>"{model_name}"'
    content = re.sub(pattern_run_agent, replace_run_agent, content, count=1)

    write_file(filepath, content)


# Main script logic
if __name__ == "__main__":
    print("AgentPress Model Changer Script")
    print("------------------------------")

    ollama_models = get_ollama_models()

    options = {
        "1": "anthropic/claude-3-7-sonnet-latest",
        "2": "perplexity/sonar-pro",
    }
    next_option_num = 3

    if ollama_models:
        print("\nAvailable Ollama Models:")
        for model in ollama_models:
            options[str(next_option_num)] = f"ollama/{model}"
            print(f"{next_option_num}: {model}")
            next_option_num += 1

    print("\nSelect a model to set as default:")
    for key, value in options.items():
        if value.startswith("ollama/"):
            continue # Already printed Ollama models separately
        print(f"{key}: {value}")

    while True:
        choice = input("Enter option number: ")
        if choice in options:
            selected_model = options[choice]
            print(f"\nYou selected: {selected_model}")
            break
        else:
            print("Invalid option. Please try again.")

    # Implement file modification logic
    update_api_file(selected_model)
    update_context_manager_file(selected_model)
    update_run_file(selected_model)
    update_thread_manager_file(selected_model)

    print("\nModel change process completed.")

    print("\nStarting backend and frontend...")

    # Start backend
    backend_process = subprocess.Popen(["uvicorn", "api:app", "--reload"], cwd="backend/")
    print("Backend started.")

    # Start frontend
    frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend/")
    print("Frontend started.")

    print("\nAgentPress is running. Press Ctrl+C to stop both processes.")

    # Keep the script running until interrupted
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Processes stopped.")

        # Run cost analysis script
        print("\nRunning cost analysis...")
        subprocess.run(["python", "analyze_logs_cost.py"])
