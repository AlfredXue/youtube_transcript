import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def improve_transcript(transcript: str) -> str:
    openai.my_api_key = OPENAI_API_KEY  # get from environment
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent assitant tasked with correcting a transcript based on the context of the transcript. You should provide exactly and only the corrected transcript as your response.",
        }
    ]

    messages.append({"role": "user", "content": transcript})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    return reply
