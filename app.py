


import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks import get_openai_callback

st.set_page_config(page_title="🦜🔗 LangChain Quickstart", page_icon="🦜", layout="wide")

st.title('🦜🔗 LangChain Quickstart App')

st.markdown("""
This app demonstrates a simple use case of LangChain with OpenAI's GPT model.
Enter your OpenAI API key in the sidebar, and ask a question in the text area below.
""")

with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input('OpenAI API Key', type='password')
    model = st.selectbox("Choose a model", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"], index=0)

st.markdown("---")

def generate_response(input_text, model, api_key):
    chat = ChatOpenAI(temperature=0.7, model_name=model, openai_api_key=api_key)
    messages = [HumanMessage(content=input_text)]
    
    with get_openai_callback() as cb:
        response = chat(messages)
    
    return response.content, cb

with st.form('my_form'):
    text = st.text_area('Enter your question:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')

if submitted:
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API Key in the sidebar!', icon='⚠')
    else:
        with st.spinner('Generating response... Please wait.'):
            try:
                response, cb = generate_response(text, model, openai_api_key)
                st.success('Response generated successfully!')
                st.write(response)

                # Display API call information
                st.info('API Call Information', icon='ℹ️')
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Tokens", cb.total_tokens)
                    st.metric("Prompt Tokens", cb.prompt_tokens)
                    st.metric("Completion Tokens", cb.completion_tokens)
                with col2:
                    st.metric("Total Cost (USD)", f"${cb.total_cost:.4f}")
                    st.metric("Model Name", model)
                    st.metric("Successful Requests", cb.successful_requests)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and LangChain")
