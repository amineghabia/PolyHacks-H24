import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from pages.myconfig import *

arr = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

uri = "mongodb+srv://jadrabhi:5AFOr0GCVREThK64@hackathon.upngmgt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Hackathon']

collection = db['types']

def get_all_documents(category_collection):
    cursor = category_collection.find()
    all_documents = []
    for document in cursor:
        all_documents.append(document)

    return all_documents

data = get_all_documents(collection)

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss.detach(), 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch {}: train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch+1, result['train_loss'], result['val_loss'], result['val_acc']))

class ResNet(ImageClassificationBase):
    def __init__(self):
        super().__init__()
        # Use a pretrained model
        self.network = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        # Replace last layer
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, len(dataset.classes))
    
    def forward(self, xb):
        return torch.sigmoid(self.network(xb))

def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

device = get_default_device()

def predict_image(img, model):
    # Convert to a batch of 1
    xb = to_device(img.unsqueeze(0), device)
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    prob, preds  = torch.max(yb, dim=1)
    # Retrieve the class label
    return arr[preds[0].item()]

def main():

    st.set_page_config(initial_sidebar_state="collapsed")

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    transformations = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    
    st.title("EcoSort")

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        st.text("connected to MongoDB")
    except Exception as e:
        st.text(e)

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    PATH = "model/entire_model.pt"
    try:
        # Attempt to load the PyTorch model
        model_loaded = torch.load(PATH, map_location=torch.device('cpu'))
        model_loaded = to_device(model_loaded, device)
        st.success("PyTorch model loaded successfully!")

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            img = transformations(image)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
            text = predict_image(img, model_loaded)
            st.text(text)
            
            st.markdown(dict_markdown[text])

            collection.update_one(
                {'categorie': text},
                {'$inc': {'count': 1}},
                upsert=True
            )

            data = get_all_documents(collection)
            categories = [entry['categorie'] for entry in data]
            counts = [entry['count'] for entry in data]
            st.text("")
            fig, ax = plt.subplots()
            ax.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90)
            ax.set_title('Proportion of scanned waste categories')
            
            st.pyplot(fig)
                
    except FileNotFoundError:
        st.error(f"Error: Model file not found at path: {PATH}")
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
