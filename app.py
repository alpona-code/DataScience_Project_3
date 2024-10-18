from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Google Gemini Pro Vision API and get the response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to handle image upload and convert it into parts
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set up Streamlit page config
st.set_page_config(page_title="Gemini Health App", page_icon="🍎", layout="wide")

# Main UI
st.title("🥗 Gemini Health App - Calorie Calculator")
st.write("This app helps you calculate the total calories in the food items from an image.")

# Input section
input = st.text_input("Describe your meal or give additional context:", key="input")
uploaded_file = st.file_uploader("Upload an image of your meal (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Instructions for the prompt
st.markdown("""
    **Instructions:**  
    - Upload an image of your food.
    - Provide any additional context (optional).
    - Click 'Calculate Calories' to see the total calorie count and breakdown of each food item.
""")

# Prompt used for getting the response
input_prompt = """
You are an expert nutritionist. Look at the food items in the image and calculate the total calories. 
Also, provide a detailed breakdown of each food item with the calorie count in the format below:

1. Item 1 - no. of calories  
2. Item 2 - no. of calories  
----  
Total calories: X
"""

# Submit button
submit = st.button("🍽️ Calculate Calories")

# If submit is clicked, call the function and display response
if submit:
    try:
        # Check for image upload and process the input
        if uploaded_file:
            with st.spinner("Analyzing the image and calculating calories..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data, input)
                st.success("Calorie breakdown is ready!")
                st.subheader("Calorie Breakdown")
                st.write(response)
        else:
            st.error("Please upload an image of your meal to proceed.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("""
---
*Powered by Google Gemini Pro Vision API*
""")
