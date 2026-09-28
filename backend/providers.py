"""
LYRA - Provider Abstraction Layer

Yeh file "adapter pattern" implement karti hai. Maqsad yeh hai ke hamara
main.py kisi ek AI provider (Claude, Ollama, OpenAI, waghera) se seedha
"chipka" na rahe. Har provider ka apna alag SDK/API format hota hai -
yeh file un differences ko chupa deti hai, aur ek common "chat()" function
deti hai jo har provider ke liye same tareeqe se kaam karta hai.

Isse fayda: kal agar hum Claude ya OpenAI add karna chahein, sirf ek nayi
class banani hogi is file mein - main.py ko chhoona nahi paray ga.
"""

import os
from abc import ABC, abstractmethod
import requests


class AIProvider(ABC):
    """
    Yeh ek "base interface" hai (abstract class). Isay khud kabhi
    directly use nahi karte - yeh sirf ek "contract" define karta hai:
    "jo bhi provider banao, usme yeh chat() function zaroor hona chahiye".
    """

    @abstractmethod
    def chat(self, message: str) -> str:
        """Message leta hai, AI se response leta hai, text wapas karta hai."""
        pass


class OllamaProvider(AIProvider):
    """
    Yeh provider local Ollama se baat karta hai. Ollama background mein
    ek local web server chalata hai (http://localhost:11434) - hum seedha
    usay HTTP request bhejte hain, bilkul jaise koi normal API ho, bas
    yeh local hai, internet par nahi jaata.
    """

    def __init__(self, model: str = "qwen3.5:4b"):
        self.model = model
        self.base_url = "http://localhost:11434"

    def chat(self, message: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": message}],
                    "stream": False,  # abhi simple rakhte hain, streaming baad mein
                    "think": False,  # thinking mode band - seedha, fast jawab chahiye
                },
                timeout=300,  # CPU-only hardware par model load + response generate hone mein zyada time lag sakta hai
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Ollama se connect nahi ho saka. Kya Ollama background mein chal raha hai? "
                "Terminal mein 'ollama list' chala kar verify karein."
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Ollama response dene mein bohot time le raha hai (timeout).")


def get_provider() -> AIProvider:
    """
    Yeh function .env file mein likhe AI_PROVIDER variable ke hisaab se
    sahi provider class wapas karta hai. main.py sirf isay call karega -
    isay pata nahi hoga (aur zaroorat bhi nahi) ke peeche Ollama hai ya
    kal ko Claude/OpenAI.
    """
    provider_name = os.getenv("AI_PROVIDER", "ollama").lower()

    if provider_name == "ollama":
        model = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
        return OllamaProvider(model=model)

    raise ValueError(f"Unknown AI_PROVIDER: '{provider_name}'. Abhi sirf 'ollama' supported hai.")