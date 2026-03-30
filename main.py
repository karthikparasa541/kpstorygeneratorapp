# saving the api key
import os
import requests

#Used langchain, prompt template and chain modules in this code.
# import ChatAPI Model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import streamlit as st
from PIL import Image
from io import BytesIO
from openai import OpenAI

def display_image_from_url(url: str, max_width: int = 600, max_height: int = 400):
    """
    Display an image from a URL with a maximum size constraint.

    Args:
    url (str): The URL of the image to display.
    max_width (int): The maximum width of the displayed image. Default is 800.
    max_height (int): The maximum height of the displayed image. Default is 600.
    """
    try:
        from PIL import Image
        import requests
        from io import BytesIO
        
        # Fetch the image
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    
        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height
    
        # Determine new size while maintaining aspect ratio
        if img.width > max_width or img.height > max_height:
            if aspect_ratio > 1:
                new_width = min(img.width, max_width)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(img.height, max_height)
                new_width = int(new_height * aspect_ratio)
    
            img = img.resize((new_width, new_height))
    
        # Display the resized image
        st.image(img)
  
    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
  gpt4omini = ChatOpenAI(model_name = "gpt-4o-mini", openai_api_key = st.secrets["OPENAI_API_KEY"])
  client = OpenAI()

  #We are defining a template below
  query_template = "Generate a {story_type} story with {no_characters} character(s) in {language}. Do not include the story title in your response. Include the characters and then show full story."
  
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
      story_text = response.content
      title_response = gpt4omini.invoke(
      f"Generate a short, catchy book title (5 words or less) for this story:\n\n{story_text}"
      )
      book_title = title_response.content.strip()
      st.write("Book Title :" book_title) 
        
      image_prompt_response = gpt4omini.invoke(f"""
        Design a professional book cover for a book titled "{book_title}".
        The title "{book_title}" must appear prominently at the top of the cover in large, bold, decorative font.
        The cover illustration should depict the main scene or characters from this story: {story_text[:500]}
        The overall composition should look like a real published book cover with the title as the focal text element.""")       
        
      image_prompt = image_prompt_response.content[:4000]
        
      image_response = client.images.generate(
      model="dall-e-3",
      prompt=image_prompt,
      n=1,
      size="1024x1024"
      )
      image_url = image_response.data[0].url
      display_image_from_url(image_url)
      st.write(story_text)
      st.write("***** End Story ************")
      
  
  with bt2:
    if st.button("Clear"):
      st.write("")


if __name__ == '__main__':
    main()
