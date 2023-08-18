import os

import streamlit as st
from langchain.chat_models import ChatOpenAI

from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler

st.caption('Enter OpenAI API key')
open_ai_api = st.text_input('OpenAI API:',key='open_ai_key')

if st.session_state['open_ai_key'] != '':
    os.environ["OPENAI_API_KEY"] = open_ai_api

    llm = ChatOpenAI(temperature=0)
    tools = load_tools(["wikipedia"], llm=llm)

    agent= initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose = False)
    st.caption('Ask questions, ignore parsing errors:')

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)