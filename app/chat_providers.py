# Chat providers for the assistant
import os
import openai
import requests
import google.generativeai as genai
import anthropic
from flask import current_app
from typing import Optional

class ChatProvider:
    """Abstract provider for chat models."""
    def reply(self, message: str) -> str:
        raise NotImplementedError

class OpenAIProvider(ChatProvider):
    def __init__(self, model: str, api_key: str):
        self.model = model
        openai.api_key = api_key

    def reply(self, message: str) -> str:
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

class HuggingFaceProvider(ChatProvider):
    def __init__(self, model: str, api_token: Optional[str] = None):
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}

    def reply(self, message: str) -> str:
        resp = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": message},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "")
        return data.get("generated_text", "")

class GeminiProvider(ChatProvider):
    def __init__(self, model: str, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def reply(self, message: str) -> str:
        response = self.model.generate_content(message)
        return getattr(response, "text", str(response))

class AnthropicProvider(ChatProvider):
    def __init__(self, model: str, api_key: str):
        self.client = anthropic.Client(api_key)
        self.model = model

    def reply(self, message: str) -> str:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": message}],
        )
        content = resp.content
        if isinstance(content, list) and content:
            part = content[0]
            if hasattr(part, "text"):
                return part.text
        return str(content)

class LocalHFProvider(ChatProvider):
    """Run open-source models locally via transformers."""

    def __init__(self, model_path: str):
        from transformers import pipeline

        self.pipeline = pipeline("text-generation", model=model_path, tokenizer=model_path)

    def reply(self, message: str) -> str:
        outputs = self.pipeline(message, max_new_tokens=128)
        if outputs:
            return outputs[0]["generated_text"]
        return ""

def get_chat_provider() -> ChatProvider:
    provider = current_app.config.get("CHAT_PROVIDER", "openai")
    if provider == "huggingface":
        model = current_app.config.get("HUGGINGFACE_MODEL", "google/flan-t5-small")
        token = current_app.config.get("HUGGINGFACE_API_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")
        return HuggingFaceProvider(model, token)
    if provider == "gemini":
        model = current_app.config.get("GEMINI_MODEL", "gemini-pro")
        api_key = current_app.config.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        return GeminiProvider(model, api_key)
    if provider == "anthropic":
        model = current_app.config.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
        api_key = current_app.config.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        return AnthropicProvider(model, api_key)
    if provider == "localhf":
        model_path = current_app.config.get("LOCAL_MODEL_PATH", "./model")
        return LocalHFProvider(model_path)
    model = current_app.config.get("OPENAI_MODEL", "gpt-3.5-turbo")
    api_key = current_app.config.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    return OpenAIProvider(model, api_key)
