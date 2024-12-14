import streamlit as st
from langchain_ollama import OllamaLLM
import streamlit.components.v1 as components

base_url = "http://localhost:11434"

models = {"llama3.2:1b  1 billion-parameter model ":"llama3.2:1b",
            "llama3.2:3b  3 billion-parameter model ":"llama3.2:3b",
            "llama3:8b    8 billion-parameter model ":"llama3:8b",
            "llama3:3     70 billion-parameter model ":"llama3.3:latest"}

with st.sidebar:
    selected_model_name = st.selectbox("Select a model:", options=list(models.keys()))
    selected_model = models[selected_model_name]

llm = OllamaLLM(model=selected_model, base_url=base_url, temperature=0.8)

st.title("Chatbot using Ollama Models")
st.markdown("### Reach out to me at **mvsreejith0@gmail.com** to understand more.")

prompt=st.chat_input("Ask your question....")

if "message" not in st.session_state.keys():
    st.session_state['message']=[{"role":"assistant","content":"How can I assist you today ?"}]

if prompt:
    st.session_state['message'].append({"role":"user","content":prompt})

for msg in st.session_state['message']:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if st.session_state['message'][-1]["role"]!="assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            streamed_response_container = st.empty()
            streamed_content = ""
            for output in llm.stream(prompt):
                streamed_content += output
                streamed_response_container.write(streamed_content)
            msg={"role":"user","content":streamed_content}
            st.session_state['message'].append(msg)