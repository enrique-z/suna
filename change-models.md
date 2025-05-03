# How to Change LLM Models

This document explains how to switch the default Large Language Model (LLM) used in the AgentPress backend between Anthropic Sonnet 3.7 and Perplexity Sonar Pro, and also how to change the model used for conversation summarization. It also includes instructions for using local Ollama models.

## Changing the Default Agent Model

The default model used when starting a new agent thread is configured in the `backend/agent/api.py` file.

To switch the default model:

1.  Open the file `backend/agent/api.py`.
2.  Locate the `AgentStartRequest` BaseModel definition.
3.  Find the `model_name` field. Comment out the line setting the default to `"anthropic/claude-3-7-sonnet-latest"` and uncomment the line setting the default to `"perplexity/sonar-pro"`, or vice versa. To use an Ollama model, set the default to `"ollama/<your_model_name>"`, replacing `<your_model_name>` with the name of the Ollama model you want to use (e.g., `"ollama/llama2"`).

    ```python
    class AgentStartRequest(BaseModel):
        # To use Anthropic Sonnet 3.7 by default:
        # model_name: Optional[str] = "anthropic/claude-3-7-sonnet-latest"
        # To use Perplexity Sonar Pro by default:
        # model_name: Optional[str] = "perplexity/sonar-pro"
        # To use an Ollama model by default (replace <your_model_name>):
        model_name: Optional[str] = "ollama/<your_model_name>"
        # ... other fields
    ```

4.  Locate the `initiate_agent_with_files` function definition.
5.  Find the `model_name` form parameter. Comment out the line setting the default to `"anthropic/claude-3-7-sonnet-latest"` and uncomment the line setting the default to `"perplexity/sonar-pro"`, or vice versa. To use an Ollama model, set the default to `"ollama/<your_model_name>"`, replacing `<your_model_name>` with the name of the Ollama model you want to use (e.g., `"ollama/llama2"`).

    ```python
    async def initiate_agent_with_files(
        prompt: str = Form(...),
        # To use Anthropic Sonnet 3.7 by default:
        # model_name: Optional[str] = Form("anthropic/claude-3-7-sonnet-latest"),
        # To use Perplexity Sonar Pro by default:
        # model_name: Optional[str] = Form("perplexity/sonar-pro"),
        # To use an Ollama model by default (replace <your_model_name>):
        model_name: Optional[str] = Form("ollama/<your_model_name>"),
        # ... other parameters
    ):
    ```

## Changing the Summarization Model

The model used for summarizing conversation threads to manage context window size is configured in the `backend/agentpress/context_manager.py` file.

To switch the summarization model:

1.  Open the file `backend/agentpress/context_manager.py`.
2.  Locate the `create_summary` function definition.
3.  Find the `model` parameter in the function signature. Change the default value to your desired model (e.g., `"perplexity/sonar-pro"`, `"openai/gpt-4o-mini"`, or `"ollama/<your_model_name>"`).

    ```python
    async def create_summary(
        self,
        thread_id: str,
        messages: List[Dict[str, Any]],
        model: str = "ollama/<your_model_name>" # Change this model name
    ) -> Optional[Dict[str, Any]]:
    ```

## Using Local Ollama Models

To use local Ollama models, you need to have Ollama installed and running on your system. The AgentPress backend uses LiteLLM, which can automatically detect and use Ollama models running on the default address (`http://localhost:11434`).

If your Ollama instance is running on a different address, you can configure the `OLLAMA_API_BASE` environment variable in your backend's `.env` file.

1.  Open the `.env` file in the `backend/` directory.
2.  Add or update the `OLLAMA_API_BASE` variable with the URL of your Ollama instance.

    ```dotenv
    OLLAMA_API_BASE="http://your_ollama_host:11434"
    ```

    Replace `"http://your_ollama_host:11434"` with the actual address of your Ollama instance. If you are using the default address, you do not need to set this variable.

3.  In the `backend/agent/api.py` and `backend/agentpress/context_manager.py` files, specify the Ollama model you want to use by prefixing the model name with `ollama/` (e.g., `"ollama/llama2"`).

Remember to restart your backend service after making these code and configuration changes for them to take effect.
