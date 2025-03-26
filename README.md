# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
The Regulatory Data Profiler is an AI-driven solution designed to automate regulatory compliance and fraud detection in financial transactions. This project addresses the challenge of regulatory data profiling by:

✅ Extracting profiling rules from regulatory reporting instructions
✅ Detecting anomalies and potential fraud in transaction data
✅ Generating Python validation code for compliance checks
✅ Computing risk scores for flagged transactions
✅ Suggesting remediation actions for compliance violations

This solution ensures accuracy, scalability, and transparency in regulatory compliance, helping financial institutions detect risks, prevent fraud, and meet compliance requirements efficiently. 🚀

## 🎥 Demo
🔗 [Live Demo](https://github.com/ewfx/gaidp-tech-titans/blob/main/artifacts/demo/Demo.mp4)

## 💡 Inspiration
Regulatory compliance in financial transactions is a time-consuming and complex process that requires manual rule extraction, anomaly detection, and fraud prevention. Institutions often struggle with interpreting regulatory instructions, ensuring data integrity, and identifying high-risk transactions.

Our inspiration came from the need to automate compliance validation while maintaining accuracy, scalability, and explainability. By leveraging AI, machine learning, and automation, we aim to simplify compliance processes, detect fraud in real time, and help financial institutions avoid penalties.

## ⚙️ What It Does
The Regulatory Data Profiler is an end-to-end AI-powered compliance pipeline that:

🔹 Extracts Profiling Rules 📜
   ➤ Interprets regulatory instructions and generates validation rules automatically.

🔹 Detects Anomalies & Fraud 🚨
   ➤ Uses unsupervised ML techniques to detect unusual patterns and suspicious transactions.

🔹 Generates Python Validation Code 🖥️
   ➤ Creates Python scripts for data validation, ensuring compliance with financial regulations.

🔹 Computes Risk Scores 📊
   ➤ Assigns risk scores to transactions based on historical data and fraud indicators.

🔹 Provides Suggested Remediation Actions ✅
   ➤ Suggests actions such as manual review, enhanced due diligence, or regulatory reporting.

🔹 Interactive UI for Auditors 🎛️
   ➤ Streamlit-based UI where auditors can upload datasets, view flagged transactions, and analyze risk scores.

## 🛠️ How We Built It
We developed this solution using a modular, scalable approach with the following technologies:

🔹 Python 🐍 – Core programming language
🔹 Flask 🚀 – Backend API for data processing and rule validation
🔹 Streamlit 🎨 – Interactive UI for auditors
🔹 Pandas & NumPy 📊 – Data manipulation and processing
🔹 Scikit-learn 🏆 – Anomaly detection using unsupervised ML
🔹 OpenAI / OpenRouter API 🤖 – Generating compliance rules dynamically
🔹 Hugging Face Models 🧠 – Advanced AI-driven rule extraction
🔹 Docker 🐳 – Containerized deployment for scalability

The backend efficiently processes uploaded datasets, extracts rules from regulatory instructions, validates transactions, and returns flagged transactions to the UI in real-time.

## 🚧 Challenges We Faced
🚧 Ensuring AI-Generated Rules Are Accurate
   ➤ AI sometimes generates vague or inconsistent rules. We refined prompts and validated outputs to ensure relevance.

🚧 Handling Large Datasets Efficiently
   ➤ Compliance datasets can be huge. We optimized our pipeline using batch processing and multiprocessing for scalability.

🚧 Seamless Integration Between AI, Backend, and UI
   ➤ Managing real-time interactions between Flask (backend), OpenAI/Hugging Face (AI models), and Streamlit (frontend) required careful API structuring.

🚧 Mapping AI-Generated Rules to Data Schema Dynamically
   ➤ We ensured that rules dynamically adapt to different datasets without hardcoded field names.

🚧 Handling Unsupported Operators in Validation
   ➤ AI sometimes used unsupported operators (e.g., match, not in). We handled them gracefully while ensuring other rules still function.

Despite these challenges, we successfully built an intelligent, scalable, and user-friendly solution that can revolutionize regulatory compliance automation! 🚀

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaidp-tech-titans.git
   cd gaidp-tech-titans
   ```
2. Install dependencies  
   ```sh
   cd code
   pip install -r requirements.txt
   ```
3. Run the project  
   Backend
   ```sh
   cd src\backend\app
   py app.py
   ```
   Frontend. New Seperate Terminal
   ```sh
   cd src\frontend\app
   py app.py
   ```	

## 🏗️ Tech Stack
🔹 Frontend: Streamlit (for an interactive and user-friendly UI)
🔹 Backend: Flask (for handling API requests, processing data, and running ML models)
🔹 Database: CSV-based storage (can be extended to SQL/NoSQL databases)
🔹 AI & ML:
    🤖 OpenRouter API / Hugging Face Models (for AI-powered rule generation)
    📊 Scikit-learn (for anomaly detection and risk scoring)
🔹 Other: Pandas, NumPy, Requests (for efficient data processing and API communication)

## 👥 Team
- **Manoj Kumar Pasumarthi** - [GitHub](#) | [LinkedIn](#)
- **Dubey, Pritesh** - [GitHub](#) | [LinkedIn](#)