import streamlit as st
from azure_hmg1_assistant import process_message 
from PIL import Image
import base64

# load logos
banner_logo = "cgi_logo.png"

# Convert images to base64 so they can be displayed with HTML in Streamlit
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Base64 encoded images
banner_logo64 = get_image_base64(banner_logo)

def handle_chat_prompt(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = process_message(prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
 
def main():
    st.set_page_config(page_title="HMG1 Demo", layout="wide")

    st.markdown(
        f"""
        <style>
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {{
                position: sticky;
                top: 3.7rem;
                background-color: white;
                z-index: 999;
                padding-top: 10px;
            }}  

            logo-container {{
                width: 100px;
                height: 100px;
            }}

            .title-box {{
                font-family: Arial, sans-serif;
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                background-color: #cb092c;
                padding: 10px;
                text-align: center;
                border-radius: 10px;
                margin-top: 10px;
                width: 100%;
            }}

            .subtitle {{
                font-family: Arial, sans-serif;
                font-size: 24px;
                color: #ffffff;
                padding: 5px;
            }}
        </style>

        <div>
            <div class="logo-container">
                <img src="data:image/png;base64,{banner_logo64}" style="max-height: 150px; max-width: 150px;">
            </div>
            <hr style="width:100%; border: 1px solid #cb092c; margin: 20px 0;">
            <div class="title-box">
                UK HR Diversity, Equity and Inclusion Policy
                <br>
                <span class="subtitle">AI-Powered Insights from UK HR Diversity, Equity and Inclusion Policy</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if ('transcription_results' in st.session_state):
        speech_contents = ' '.join(st.session_state.transcription_results)
        del st.session_state.transcription_results
        handle_chat_prompt(speech_contents)

    # Await a user message and handle the chat prompt when it comes in.
    if prompt := st.chat_input("Enter a message:"):
        handle_chat_prompt(prompt)

if __name__ == "__main__":
    main()