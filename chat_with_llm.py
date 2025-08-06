import os
import requests

def get_llm_response(messages):
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "azure":
        api_key = os.getenv("AZURE_OPENAI_KEY")
        api_base = os.getenv("AZURE_OPENAI_BASE")
        api_version = os.getenv("AZURE_API_VERSION")
        deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")

        if not all([api_key, api_base, api_version]):
            raise ValueError("Missing one of AZURE_OPENAI_KEY, AZURE_OPENAI_BASE, or AZURE_API_VERSION.")

        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base,
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages
        )
        return response.choices[0].message.content

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )

        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content

    elif provider == "ollama":
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3")
        endpoint = f"{ollama_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        try:
            res = requests.post(endpoint, json=payload)
            res.raise_for_status()
            return res.json()["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama call failed: {e}")

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    try:
        reply = get_llm_response(messages)
        print("LLM Response:", reply)
    except Exception as e:
        print("Error:", str(e))

