import os
import json
import requests
import time
from openai import AzureOpenAI
import streamlit as st

client = AzureOpenAI(
  azure_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"],
  api_key= st.secrets["AZURE_OPENAI_API_KEY"],
  api_version="2024-05-01-preview"
)

assistant = client.beta.assistants.create(
    model="gpt-4o",
    instructions="You are an assistant that answers the users questions",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search":{"vector_store_ids":["vs_zWOfI3HZgB77bohRLyDnGLEk"]}},
    temperature=0.3
)

def process_message(content: str):
    # Create a thread
    thread = client.beta.threads.create()

    # Add a user question to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content # Users prompt 
    )

    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            messages = messages.to_json(indent=2)
            messages = json.loads(messages)
            break
        else:
             time.sleep(5)

    contents = []
    for message in messages["data"]:
        if 'content' in message:
            for content_item in message['content']:
                if 'text' in content_item and 'value' in content_item['text']:
                    contents.append(content_item['text']['value'])

    return contents[0]
