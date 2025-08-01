
# 🖼️ AI Image Creator: Text-to-Image Generation

This project takes user input text (in Uzbek, Russian, or English) and generates a relevant image using artificial intelligence. The backend is powered by Django and natural language processing (NLP) tools. The interface simulates a simple chat, and the results are shown as images.

## 🔍 Key Features

- 🌐 Input text in Uzbek, Russian, or English.
- 🧠 AI-generated images based on user input.
- 📦 Backend powered by Django (`nltk`, `transformers`, `torch`, `diffusers`, etc.).
- 💬 Simple, Telegram-style web chat interface.

---

## 🛠️ Technologies Used

- Python 3.10+
- Django 5.2.4
- NLTK
- HuggingFace Transformers
- Stable Diffusion / Diffusers
- HTML + CSS (basic UI)

---

## 🚀 Local Setup Instructions

Follow the steps below to run the project locally on either Windows or Linux/macOS.

### 1. Clone the Repository

```bash
git clone https://github.com/username/text-to-image-ai.git
cd text-to-image-ai
```

### 2. Create a Virtual Environment

#### 💻 On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Django Development Server

```bash
python manage.py runserver
```

Then open your browser and go to:

```
http://127.0.0.1:8000/
```


## 📧 Author

Abrorjon — [Portfolio Website](https://abrorjon.pythonanywhere.com/en/)  
Feel free to reach out for any questions or feedback!

