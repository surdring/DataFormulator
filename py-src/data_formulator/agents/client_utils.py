import litellm
import openai
import httpx
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from typing import Dict, Optional, Union

_FALLBACK_HTTPX_CLIENT = httpx.Client(timeout=120, trust_env=False)
_OPENAI_CLIENT_CACHE: Dict[tuple[str, str], openai.OpenAI] = {}


def _get_openai_client(base_url: Optional[str], api_key: str) -> openai.OpenAI:
    key = (base_url or "", api_key or "")
    client = _OPENAI_CLIENT_CACHE.get(key)
    if client is None:
        client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=120,
        )
        _OPENAI_CLIENT_CACHE[key] = client
    return client

class OpenAIClientAdapter(object):
    """
    Wrapper around OpenAI or AzureOpenAI client that provides the same interface as Client.
    """
    def __init__(self, openai_client: Union[openai.OpenAI, openai.AzureOpenAI], model: str):
        self._openai_client = openai_client
        self.model = model
        self.params = {}
        
    def get_completion(self, messages, stream=False, max_tokens: Optional[int] = None):
        """
        Returns a completion using the wrapped OpenAI client.
        """
        completion_params = {
            "model": self.model,
            "messages": messages,
        }

        if max_tokens is not None:
            completion_params["max_tokens"] = int(max_tokens)
        
        return self._openai_client.chat.completions.create(**completion_params, stream=stream)

class Client(object):
    """
    Returns a LiteLLM client configured for the specified endpoint and model.
    Supports OpenAI, Azure, Ollama, and other providers via LiteLLM.
    """
    def __init__(self, endpoint, model, api_key=None,  api_base=None, api_version=None):
        
        self.endpoint = endpoint
        self.model = model
        self.params = {}

        if api_key is not None and api_key != "":
            self.params["api_key"] = api_key
        if api_base is not None and api_base != "":
            self.params["api_base"] = api_base
        if api_version is not None and api_version != "":
            self.params["api_version"] = api_version

        if self.endpoint == "gemini":
            if model.startswith("gemini/"):
                self.model = model
            else:
                self.model = f"gemini/{model}"
        elif self.endpoint == "anthropic":
            if model.startswith("anthropic/"):
                self.model = model
            else:
                self.model = f"anthropic/{model}"
        elif self.endpoint == "azure":
            self.params["api_base"] = api_base
            self.params["api_version"] = api_version if api_version else "2025-04-01-preview"
            if api_key is None or api_key == "":
                token_provider = get_bearer_token_provider(
                    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
                )
                self.params["azure_ad_token_provider"] = token_provider
            self.params["custom_llm_provider"] = "azure"
        elif self.endpoint == "ollama":
            self.params["api_base"] = api_base if api_base else "http://localhost:11434"
            self.params["max_tokens"] = self.params["max_completion_tokens"]
            if model.startswith("ollama/"):
                self.model = model
            else:
                self.model = f"ollama/{model}"

    @classmethod
    def from_config(cls, model_config: Dict[str, str]):
        """
        Create a client instance from model configuration.
        
        Args:
            model_config: Dictionary containing endpoint, model, api_key, api_base, api_version
            
        Returns:
            Client instance for making API calls
        """
        # Strip whitespace from all values
        for key in model_config:
            if isinstance(model_config[key], str):
                model_config[key] = model_config[key].strip()

        return cls(
            model_config["endpoint"],
            model_config["model"],
            model_config.get("api_key"),
            model_config.get("api_base"),
            model_config.get("api_version")
        )

    def get_completion(self, messages, stream=False, max_tokens: Optional[int] = None):
        """
        Returns a LiteLLM client configured for the specified endpoint and model.
        Supports OpenAI, Azure, Ollama, and other providers via LiteLLM.
        """
        # Configure LiteLLM 

        if self.endpoint == "openai":
            base_url = self.params.get("api_base", None)
            if isinstance(base_url, str):
                base_url = base_url.strip()
                if base_url.startswith("http://localhost"):
                    base_url = "http://127.0.0.1" + base_url[len("http://localhost"):]
                if base_url.startswith("https://localhost"):
                    base_url = "https://127.0.0.1" + base_url[len("https://localhost"):]
                if base_url.endswith("/"):
                    base_url = base_url[:-1]

            api_key = self.params.get("api_key", "")

            # Performance: for local llama.cpp/openai-compatible servers, prefer direct httpx
            # to avoid OpenAI SDK retries/backoff and the extra exception+fallback path.
            is_local_base = isinstance(base_url, str) and (
                base_url.startswith("http://127.0.0.1")
                or base_url.startswith("https://127.0.0.1")
            )

            completion_params = {
                "model": self.model,
                "messages": messages,
            }

            if max_tokens is not None:
                completion_params["max_tokens"] = int(max_tokens)

            if self.model.startswith("gpt-5") or self.model.startswith("o1") or self.model.startswith("o3"):
                completion_params["reasoning_effort"] = "low"
            
            try:
                if not is_local_base:
                    client = _get_openai_client(base_url, api_key)
                    return client.chat.completions.create(**completion_params, stream=stream)
                raise RuntimeError("local_base_use_httpx")
            except Exception as e:
                status = getattr(e, "status_code", None)
                if status is None:
                    resp = getattr(e, "response", None)
                    status = getattr(resp, "status_code", None)

                # Fallback for llama.cpp/openai-compatible servers where the OpenAI SDK may misbehave.
                if (is_local_base or (status is not None and int(status) >= 500)) and isinstance(base_url, str):
                    url = base_url.rstrip("/") + "/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }

                    # llama.cpp text-only servers may not support image inputs.
                    # If messages contain multi-part content with image_url, drop the image parts.
                    filtered_messages = []
                    try:
                        for m in messages:
                            if not isinstance(m, dict):
                                filtered_messages.append(m)
                                continue
                            c = m.get("content")
                            if isinstance(c, list):
                                text_parts = []
                                for part in c:
                                    if isinstance(part, dict) and part.get("type") == "text":
                                        t = part.get("text")
                                        if isinstance(t, str) and t:
                                            text_parts.append(t)
                                m2 = dict(m)
                                m2["content"] = "\n".join(text_parts)
                                filtered_messages.append(m2)
                            else:
                                filtered_messages.append(m)
                    except Exception:
                        filtered_messages = messages

                    fallback_max_tokens = int(max_tokens) if max_tokens is not None else (512 if stream else 64)
                    payload = {
                        "model": self.model,
                        "messages": filtered_messages,
                        "max_tokens": fallback_max_tokens,
                        "stream": bool(stream),
                    }

                    def _raise_for_status_with_debug(resp: httpx.Response, err: Exception):
                        # For streaming responses, accessing .text requires reading the body first.
                        body_preview = ""
                        try:
                            if resp.is_stream_consumed is False:
                                resp.read()
                            body_preview = (resp.text or "")[:800]
                        except Exception:
                            body_preview = ""
                        headers_preview = dict(resp.headers)
                        raise httpx.HTTPStatusError(
                            f"{err} response_headers={headers_preview} response_body={body_preview}",
                            request=resp.request,
                            response=resp,
                        )

                    # When stream=True, return an iterable of chunks compatible with OpenAI SDK streaming
                    if stream:
                        class _Delta:
                            def __init__(self, c):
                                self.content = c

                        class _Choice:
                            def __init__(self, c):
                                self.delta = _Delta(c)

                        class _Chunk:
                            def __init__(self, c):
                                self.choices = [_Choice(c)]

                        def _iter_stream_chunks():
                            with _FALLBACK_HTTPX_CLIENT.stream("POST", url, headers=headers, json=payload) as r:
                                try:
                                    r.raise_for_status()
                                except Exception as hx_err:
                                    _raise_for_status_with_debug(r, hx_err)

                                for line in r.iter_lines():
                                    if not line:
                                        continue
                                    if isinstance(line, bytes):
                                        line = line.decode("utf-8", errors="replace")
                                    line = line.strip()
                                    if not line.startswith("data:"):
                                        continue
                                    data_str = line[len("data:"):].strip()
                                    if data_str == "[DONE]":
                                        break
                                    try:
                                        import json as _json
                                        data = _json.loads(data_str)
                                    except Exception:
                                        continue

                                    delta = ((data.get("choices") or [{}])[0].get("delta") or {})
                                    delta_content = delta.get("content")
                                    yield _Chunk(delta_content)

                        return _iter_stream_chunks()

                    # Non-streaming fallback
                    r = _FALLBACK_HTTPX_CLIENT.post(url, headers=headers, json=payload)
                    try:
                        r.raise_for_status()
                    except Exception as hx_err:
                        _raise_for_status_with_debug(r, hx_err)
                    data = r.json()

                    msg = (data.get("choices") or [{}])[0].get("message") or {}
                    content = msg.get("content") or ""
                    finish_reason = (data.get("choices") or [{}])[0].get("finish_reason")

                    class _Msg:
                        def __init__(self, c: str):
                            self.role = "assistant"
                            self.content = c

                    class _Choice:
                        def __init__(self, c: str, fr=None):
                            self.message = _Msg(c)
                            self.finish_reason = fr

                    class _Resp:
                        def __init__(self, c: str, fr=None):
                            self.choices = [_Choice(c, fr)]

                    return _Resp(content, finish_reason)

                raise
        else:

            params = self.params.copy()

            if max_tokens is not None:
                params["max_tokens"] = int(max_tokens)

            if (self.model.startswith("gpt-5") or self.model.startswith("o1") or self.model.startswith("o3")
                or self.model.startswith("claude-sonnet-4-5") or self.model.startswith("claude-opus-4")):
                params["reasoning_effort"] = "low"

            return litellm.completion(
                model=self.model,
                messages=messages,
                drop_params=True,
                stream=stream,
                **params
            )

        
    def get_response(self, messages: list[dict], tools: Optional[list] = None):
        """
        Returns a response using OpenAI's Response API approach.
        """
        if self.endpoint == "openai":
            client = openai.OpenAI(
                base_url=self.params.get("api_base", None),
                api_key=self.params.get("api_key", ""),
                timeout=120
            )
            return client.responses.create(
                model=self.model,
                input=messages,
                tools=tools,
                **self.params
            )
        else:
            return litellm.responses(
                model=self.model,
                input=messages,
                tools=tools,
                drop_params=True,
                **self.params
            )