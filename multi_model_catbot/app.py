import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyBBDr9CopHtJIiPTWhTZP-37MWkTwi0rVM"))


st.set_page_config(
    page_title="AI Multi-Modal Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Multi-Modal Chatbot")
st.markdown("### 💬 Ask questions with text, upload an image, or both!")
st.write("This chatbot uses **Google Gemini 1.5 Flash** to understand text + images and generate intelligent responses.")


genai.configure(api_key="AIzaSyBBDr9CopHtJIiPTWhTZP-37MWkTwi0rVM")
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

prompt = st.text_area("📝 Type your question:",
                      placeholder="e.g. Describe this image or What’s in the picture?")
uploaded_img = st.file_uploader(
    "📷 Upload an image (optional):", type=["jpg", "jpeg", "png"])


if uploaded_img:
    st.image(uploaded_img, caption="Your uploaded image",
             use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    generate_text = st.button("💬 Generate Response")
with col2:
    generate_image = st.button("🖼️ Generate Image")


if generate_text:
    if not prompt and not uploaded_img:
        st.warning("Please enter a prompt or upload an image first.")
    else:
        with st.spinner("🤔 Thinking..."):
            try:
                if uploaded_img:
                    image = Image.open(uploaded_img)
                    response = model.generate_content([prompt, image])
                else:
                    response = model.generate_content(prompt)
                st.success("✅ Response Generated!")
                st.markdown("### 🧠 AI Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
if generate_image:
    if not prompt:
        st.warning("Please enter a text prompt to generate an image.")
    else:
        with st.spinner("🎨 Creating image..."):
            try:
                response = model.generate_content(
                    f"Generate an image of {prompt}")
                image_data = response.candidates[0].content.parts[0].inline_data.data
                st.image(image_data, caption="Generated Image",
                         use_container_width=True)
                st.success("✅ Image Generated!")
            except Exception:
                st.error(
                    "Sorry, image generation is not supported in this model version.")


st.markdown("---")
st.caption("✨ Created by Aastik Sonkar | Powered by Google Gemini 1.5 Flash | Nullclass Internship Project")
