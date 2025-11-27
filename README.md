# 📄 AI Resume Analyzer

A **Streamlit** web application designed to analyze candidate resumes against specific job descriptions using **JamAI's** powerful artificial intelligence backend. This tool provides recruiters and hiring managers with instant, objective insights into candidate fit, saving valuable time in the screening process.

---

## ✨ Features

* **Multi-Format Upload:** Supports resume uploads in **DOC**, **DOCX**, and **PDF** formats.
* **Key Information Extraction:** Automatically extracts core candidate data, including **skills**, **experience**, and a general **profile**.
* **Overall Fit Score:** Provides an objective **AI-driven fit score** to quantify job alignment (e.g., 85/100).
* **Executive Summary:** Generates concise executive summaries in **English** and optionally **Malay** (if the data field is available).
* **Interview Question Generation:** Suggests specific **interview questions** based on the resume analysis and job requirements.
* **Analysis History:** Maintains a session-based analysis history in the sidebar for quick reference.
* **Report Download:** Allows users to download the full analysis report as a `.txt` file.

---

## 🛠️ Prerequisites

* **Python 3.13**.

> 💡 **Recommendation:** Always use a virtual environment for clean dependency management.

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/beastNico/RESUME-ANALYZER.git
cd RESUME-ANALYZER
```
### 2. Set Up Virtual Environment
Windows:

```bash
python -m venv venva
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the App
```bash
streamlit run app.py
```

### 📂 Slides & Recording:  
🔗 [Open Google Drive Folder](https://drive.google.com/drive/folders/1vWmdrAnxvTLADR9CwsBRNWthTFY6NDq9?usp=sharing)
