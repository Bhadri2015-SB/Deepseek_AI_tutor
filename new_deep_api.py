from huggingface_hub import InferenceClient
import streamlit as st

#creating subject and messages
if "subject" not in st.session_state:
    st.session_state.subject = None  # To store the subject name
if "messages" not in st.session_state:
    st.session_state.messages = []  # To store the conversation history

#title
st.title("📚Troudz AI Tutor")

# Set Subject
if st.session_state.subject is None:
    subject = st.text_input("Enter the subject name for your exam:")
    if subject:
        st.session_state.subject = subject
        st.success(f"Subject set to: {subject}")
else:
    st.write(f"**Subject:** {st.session_state.subject}")

# Display Conversation History
st.write("### Conversation:")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
question = st.chat_input("Ask your question about this subject:")

if question:
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    #client call
    client = InferenceClient(
        provider="together",
        api_key="YOUR_API_KEY"
    )

    messages = [
        {
            "role": "user",
            "content": f"I have a doubt in {question} from {st.session_state.get('subject')}. Could you please explain it in a simple way and provide some examples within 400 tokens?"
        }
    ]

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=messages, 
        max_tokens=500
    )
    # print(completion.choices[0].message)
    with st.chat_message("assistant"):
            st.write(completion.choices[0].message["content"])

    st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message["content"]})

