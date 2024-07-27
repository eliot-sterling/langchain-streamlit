


import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title="🦜🔗 LangChain Quickstart", page_icon="🦜", layout="wide")

st.title('🦜🔗 LangChain Quickstart App')

st.markdown("""
This app demonstrates a simple use case of LangChain with OpenAI's GPT model.
Enter your OpenAI API key in the sidebar, and ask a question in the text area below.
""")

with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input('OpenAI API Key', type='password')
    model = st.selectbox("Choose a model", ["gpt-4o-mini","gpt-3.5-turbo", "gpt-4"], index=0)

st.markdown("---")

@st.cache_data(show_spinner=False)
def generate_response(input_text, model):
    llm = OpenAI(temperature=0.7, model_name=model, openai_api_key=openai_api_key)
    return llm(input_text)

with st.form('my_form'):
    text = st.text_area('Enter your question:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')

if submitted:
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key in the sidebar!', icon='⚠')
    else:
        st.info('Generating response... Please wait.')
        try:
            response = generate_response(text, model)
            st.success('Response generated successfully!')
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and LangChain")
