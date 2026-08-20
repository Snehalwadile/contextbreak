import os

from dotenv import load_dotenv
from mistralai.client import Mistral


load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in .env")

client = Mistral(api_key=API_KEY)


def run_mistral(prompt: str) -> str:
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    response = run_mistral(
        "Reply with exactly one word: PROCESS"
    )

    print("Mistral response:", response)