import os
import json
import requests
import time
from openai import AzureOpenAI
import streamlit as st

client = AzureOpenAI(
  azure_endpoint = st.secrets["aoai"]["AZURE_OPENAI_ENDPOINT"],
  api_key= st.secrets["aoai"]["AZURE_OPENAI_API_KEY"],
  api_version="2024-05-01-preview"
)

assistant = client.beta.assistants.create(
  model="gpt-4o", # replace with model deployment name.
  instructions="You are an expert customer service representative for the HMG Personal Security Controls. Use your knowledge base from the vector store to answer questions about HMG Personal Security Controls. You can also have a normal conversation with the user as well",
  tools=[{"type":"file_search","file_search":{"ranking_options":{"ranker":"default_2024_08_21","score_threshold":0}}}],
  tool_resources={"file_search":{"vector_store_ids":["vs_lXeuIICtA81N5LPRhFfpimMt"]}},
  temperature=1,
  top_p=1
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

    thread = client.beta.threads.create()

    # Run the thread for the result
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
