import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from peewee import Model, SqliteDatabase, TextField, DateTimeField
import datetime
import re

# Load environment variables from the .env file
load_dotenv()

# Initialize the Groq model
groq_api_key = os.getenv("GROQ_API_KEY")
chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", groq_api_key=groq_api_key)

# Set up the database
db = SqliteDatabase('code_analysis.db')

class CodeAnalysis(Model):
    code_input = TextField()
    analysis_result = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Create tables if they don't exist
db.connect()
db.create_tables([CodeAnalysis], safe=True)

# Initialize session state to store conversations
if "conversations" not in st.session_state:
    st.session_state.conversations = []

# If no current conversation exists, create a new one automatically
if "current_conversation" not in st.session_state:
    new_conversation = {
        "id": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
        "title": "New Conversation"
    }
    st.session_state.conversations.append(new_conversation)
    st.session_state.current_conversation = new_conversation

# Function to generate an automatic conversation title
def generate_conversation_title(messages):
    if not messages:
        return "New Conversation"
    first_user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), None)
    if first_user_message:
        title = " ".join(first_user_message.split()[:5])
        return title
    else:
        return "Untitled Conversation"

# Function to clean the conversation title and make it a valid filename
def clean_filename(title):
    # Remove invalid characters in filenames
    cleaned_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return cleaned_title.strip()

# Update the title of the current conversation
st.session_state.current_conversation["title"] = generate_conversation_title(st.session_state.current_conversation["messages"])

# Streamlit interface
st.title("🤖 Code Assistant and Chat")
st.write("Enter code for analysis, describe an idea to convert into code, or start a general conversation.")

# Display the previous messages of the current conversation
for message in st.session_state.current_conversation["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Text input using st.chat_input
if prompt := st.chat_input("Enter code, describe an idea, or start a conversation..."):
    # Add user message to the current conversation
    st.session_state.current_conversation["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Determine the type of request
    is_code = any(keyword in prompt for keyword in ["def", "class", "=", "{", "}", "(", ")", "print", "return"])
    is_code_request = any(keyword in prompt for keyword in ["write", "create", "make", "required", "code", "function", "program"])

    if is_code:
        # If the text is code
        analysis_prompt = f"""
        Analyze the following code:
        {prompt}

        - Identify coding errors.
        - Suggest improvements to the code.
        - Evaluate security vulnerabilities if any.
        - Provide tips to improve performance.
        """
    elif is_code_request:
        # If the text is a description of an idea
        analysis_prompt = f"""
        Convert the following description into code:
        {prompt}

        - Ensure the code works correctly.
        - Add comments where necessary.
        """
    else:
        # If the text is general
        analysis_prompt = f"""
        {prompt}
        """

    # Send the request to the model
    with st.spinner("Processing..."):
        response = chat.invoke(analysis_prompt)

        # Save the results to the database (if it's code or a request to convert an idea into code)
        if is_code or is_code_request:
            CodeAnalysis.create(code_input=prompt, analysis_result=response.content)

        # Add the bot's response to the current conversation
        st.session_state.current_conversation["messages"].append({"role": "assistant", "content": response.content})
        with st.chat_message("assistant"):
            st.write(response.content)

    # Update the title of the current conversation after adding a new message
    st.session_state.current_conversation["title"] = generate_conversation_title(st.session_state.current_conversation["messages"])

# Display previous conversations in the sidebar
st.sidebar.title("Previous Conversations")

# Display a list of previous conversations
conversation_titles = [conv["title"] for conv in st.session_state.conversations]
if conversation_titles:  # Ensure there are conversations
    selected_conversation_title = st.sidebar.selectbox(
        "Select a conversation",
        conversation_titles,
        index=conversation_titles.index(st.session_state.current_conversation["title"]) if st.session_state.current_conversation["title"] in conversation_titles else 0
    )

    # Switch between conversations
    if selected_conversation_title != st.session_state.current_conversation["title"]:
        selected_conversation = next((conv for conv in st.session_state.conversations if conv["title"] == selected_conversation_title), None)
        if selected_conversation:  # Ensure a matching conversation exists
            st.session_state.current_conversation = selected_conversation
            st.rerun()
else:
    st.sidebar.write("No previous conversations.")

# Button to start a new conversation
if st.sidebar.button("Start a New Conversation"):
    new_conversation = {
        "id": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [],
        "title": "New Conversation"
    }
    st.session_state.conversations.append(new_conversation)
    st.session_state.current_conversation = new_conversation
    st.sidebar.success("A new conversation has started!")
