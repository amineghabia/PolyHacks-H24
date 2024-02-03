import streamlit as st
from PIL import Image

def main():
    st.title("Image Upload and Display App")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

if __name__ == "main":
    main()