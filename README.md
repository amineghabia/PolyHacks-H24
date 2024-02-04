# PolyHacks-H24

# EcoSort - Waste Sorting Assistant

Welcome to EcoSort Guide, a waste sorting assistant application developed for the PolyHacks 2024 Hackathon. This project aims to help users efficiently sort their waste by providing real-time guidance on how to properly dispose of various items.

## Project Overview

EcoSort leverages computer vision to analyze images of waste items and offers user-friendly instructions on how to segregate them into different categories, promoting environmental sustainability and proper waste management.

## Features

- **Image Recognition:** Utilizes computer vision to recognize waste items.
- **Sorting Instructions:** Provides clear and concise instructions on how to properly sort each item.
- **Statistical Resources:** Includes statistical content host with mongoDB.

### Prerequisites

- Python 3.6+
- Dependencies: [streamlit, pandas, numpy, torch, torchvision, matplotlib, pymongo[srv]]
  
## Usage
# Jupyter Notebook
Explore the initial development and analysis in the Jupyter Notebook available here.

[Training Notebook](hackathon-2024.ipynb)

## Streamlit App
To run the Streamlit app, follow this link:

[https://streamlit.app](https://polyhacks-h24-kwgzsfgnkjepfnt9kqvaty.streamlit.app/~/+/app)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/amineghabia/PolyHacks-H24.git
   cd PolyHacks-H24
   ```
2. Install dependencies:

    ```bash
   pip install -r requirements.txt
   ```

3. Run:
    ```bash
   streamlit run streamlit_app.py
   ```
