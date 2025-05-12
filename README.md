# ABS IntelliScan 🚀

AI-powered tool to analyze Asset-Backed Securities (ABS) offering memorandums like TMUST 2024-1.

This Streamlit app extracts and analyzes tranche structure, generates insights, and simulates AI-style risk scoring.

---

## 💡 Features

- 📄 Upload any ABS offering memorandum (PDF)
- 🔍 Extract Class A/B/C tranche structure from real docs
- 📊 Display interest rates, balances, and enhancement visually
- 🧠 Generate smart insights and risk scores
- 🔗 Ready to scale using AWS (Textract, Comprehend, SageMaker)

---

## 📦 Tech Stack

- **Streamlit** – Web app
- **PyMuPDF (fitz)** – PDF parsing
- **Pandas + Matplotlib** – Data analysis & charts
- **Regex** – Parsing semi-structured financial text

---

## ▶️ How to Run

1. Clone the repo or download the code:

```bash
git clone https://github.com/your-username/abs-intelliscan.git
cd abs-intelliscan
