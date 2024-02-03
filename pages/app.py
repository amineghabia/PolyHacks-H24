import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

def main():
    st.title("Image Upload and Display App")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    PATH = "../model/entire_model.pt"
    model_loaded = torch.load(PATH)

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

if __name__ == "__main__":
    main()
