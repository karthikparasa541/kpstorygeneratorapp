# saving the api key
import os


#Used langchain, prompt template and chain modules in this code.
# import ChatAPI Model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import streamlit as st

gpt4omini = ChatOpenAI(model_name = "gpt-4o-mini", openai_api_key = st.secrets["OPENAI_API_KEY"])

#We are defining a template below
query_template = "Generate a {story_type} story with {no_characters} character(s) in {language}"

#preparing the prompt with the template and mentioning the input variables
query_prompt = PromptTemplate(input_variables = ["story_type","no_characters","language"], template = query_template)

st.header("Story Generator App")
st.subheader("Generate stories using Generative AI")

story_ty = st.text_input("Enter the type of story you want to generate")
no_ch = st.number_input("Enter the number of characters in the story",min_value = 1, max_value = 5, value = 1, step = 1)
lang = st.text_input("Enter the language in which you want the story to be generated")

bt1, bt2 = st.columns(2)

with bt1:
if st.button("Generate Story"):
  #invoking the LLM model with the prompt
  st.write("***** Begin Story ************")
  response = gpt4omini.invoke(query_template.format(story_type = story_ty, no_characters = no_ch , language = lang))
  st.write(response.content)
  st.write("***** End Story ************")

with bt2:
if st.button("Clear"):
  st.write("")
