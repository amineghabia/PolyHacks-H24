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

arr = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

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
    transformations = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    
    st.title("Image Upload and Display App")

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

            if text = 'cardboard':
                markdown_content = """
                ## How to Recycle Cardboard
            
                Cardboard recycling is an essential step towards reducing waste and promoting sustainability. Here are some simple steps to recycle cardboard:
            
                1. **Flatten the Cardboard:**
                    Flatten and fold the cardboard boxes before placing them in the recycling bin. This helps save space and makes it easier for recycling facilities to process.
            
                2. **Remove Contaminants:**
                    Ensure that the cardboard is free from contaminants such as food residues, tape, and labels. Clean cardboard is more valuable in the recycling process.
            
                3. **Check Local Guidelines:**
                    Check your local recycling guidelines to understand specific requirements and collection schedules for cardboard recycling in your area.
            
                4. **Separate from Other Materials:**
                    Separate cardboard from other materials like plastics or metals. This makes the recycling process more efficient.
            
                5. **Reuse if Possible:**
                    Before recycling, consider whether the cardboard can be reused. Reusing boxes for storage or shipping is an eco-friendly option.
            
                Remember, proper cardboard recycling contributes to a healthier environment and conserves valuable resources.
            
                *Recycle responsibly and make a positive impact on the planet!*
                """
            
                st.markdown(markdown_content)
                
    except FileNotFoundError:
        st.error(f"Error: Model file not found at path: {PATH}")
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
