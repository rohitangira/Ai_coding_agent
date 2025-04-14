from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()


def callLLM(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages,
    )
    return response.choices[0].message.content
