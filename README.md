# 🛒 ShopSmart AI - Product Price Comparison Chatbot

An AI-powered chatbot that compares product prices across major Indian e-commerce platforms in real-time.

## 🚀 Features
- Compares prices across Flipkart, Amazon, Myntra, Ajio, and Meesho
- AI-powered product recommendations using Groq (LLaMA 3.1)
- Budget-based filtering in INR (₹)
- Clean and responsive chat interface
- Fast response with real-time suggestions

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Groq API (llama-3.1-8b-instant)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render (Backend), GitHub Pages (Frontend)

## ⚙️ Installation

1. Clone the repository
   git clone https://github.com/Kesavan-raj/ai-product-chatbot.git
   cd ai-product-chatbot

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your Groq API key in .env file
   GROQ_API_KEY=your_api_key_here

5. Run the backend
   uvicorn main:app --reload

6. Open frontend
   Open index.html in your browser

## 🌐 Live Demo
- **Backend API:** https://ai-product-chatbot.onrender.com
- **Frontend:** Open index.html locally or deploy to GitHub Pages

## 📁 Project Structure
ai-product-chatbot/
├── main.py
├── requirements.txt
├── .env
├── index.html
├── style.css
└── app.js

## 👨‍💻 Author
Kesavan Raj