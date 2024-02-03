import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F

import streamlit as st
from PIL import Image
<<<<<<< Updated upstream
import matplotlib.pyplot as plt
=======
import torch
from torchvision import transforms
from torchvision.models import resnet50
from torchvision import models
>>>>>>> Stashed changes

# Charger le modèle PyTorch pré-entraîné (exemple avec ResNet50)
model = models.resnet50(pretrained=True)
model.eval()

# Définir les transformations d'image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Fonction pour effectuer la classification
def classify_image(image):
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    _, predicted_idx = torch.max(output, 1)
    return predicted_idx.item()

# Interface utilisateur Streamlit
st.title("Classification des déchets")

uploaded_file = st.file_uploader("Choisissez une image de déchet", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Afficher l'image téléchargée
    image = Image.open(uploaded_file)
    st.image(image, caption="Image téléchargée", use_column_width=True)

    # Effectuer la classification
    class_idx = classify_image(image)

    # Afficher le résultat
    classes = ['Type de déchet 1', 'Type de déchet 2', 'Type de déchet 3']  # Remplacez par vos classes
    st.write("Type de déchet prédit :", classes[class_idx])
