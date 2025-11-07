

---

# 🔍✨ Gemini-Powered Text Summarizer App 📘🧠

## 🚀 Overview
This project is a **Streamlit-based AI summarization tool** powered by **Google Gemini 2.5 Pro**. It allows users to paste any text, generate a clean and concise summary, and export it as a beautifully styled PDF — all in one click.

---

## 🎯 Features

- 🧠 **Gemini 2.5 Pro Integration**: Uses Google’s generative AI to produce high-quality summaries.
- 📝 **Streamlit UI**: Clean, responsive interface with custom CSS styling.
- 📄 **PDF Export**: Stylish summary PDFs with headers, typography, and timestamps.
- 🔐 **Environment Config**: Secure API key management via `.env` file.
- 🧪 **Graceful Imports**: Optional modules handled with fallback logic to prevent UI crashes.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/gemini-summarizer.git
cd gemini-summarizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your API Key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🧪 How It Works

| Step | Action |
|------|--------|
| 1️⃣ | Paste or type your text into the input box |
| 2️⃣ | Click **🔎 Summarize Text** |
| 3️⃣ | View the AI-generated summary |
| 4️⃣ | Click **⬇️ Download PDF** to export |

---

## 📦 Tech Stack

- **Streamlit** – UI framework
- **Google Generative AI (Gemini)** – Text summarization
- **ReportLab** – PDF generation
- **dotenv** – Environment variable management
- **Regex** – Markdown-to-HTML conversion

---

## 📁 Output Example

Your exported PDF includes:
- 🧠 Gemini branding
- ✨ Executive summary title
- 📘 Clean summary card
- 🕒 Timestamp & word count
- ❤️ Footer note: *Made with love using Streamlit & Gemini*

---

## 💡 Tips

- Keep input text under a few thousand words for best results.
- Ensure your `.env` file is correctly configured.
- PDF export requires `reportlab` — install it if missing.

---

## 🙌 Credits

Made with ❤️ by [Arjumand Afreen]  
Inspired by the power of **AI + UX** to simplify information.


