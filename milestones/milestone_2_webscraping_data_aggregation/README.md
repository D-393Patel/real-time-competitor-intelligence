# 📌 Milestone 2: Web Scraping & Data Aggregation

This module focuses on two core **data engineering and NLP tasks**:

- **Question Answering (QA)** using Transformer-based NLP models  
- **Web Scraping and Data Aggregation** from both dynamic and structured websites  

The goal is to analyze **QA model performance under varying question–context scenarios** and to implement **robust web scraping pipelines** using industry-standard tools.

---

## 🎯 Objectives

- 🔍 Evaluate transformer-based extractive Question Answering models  
- 🌐 Scrape dynamic JavaScript-rendered websites using Playwright  
- 🕷 Crawl structured paginated websites using Scrapy  
- 📁 Store extracted data in CSV and JSON formats  
- ⚙ Address real-world environment challenges in Google Colab  

---

## 🛠 Tools & Technologies Used

### 🔠 Programming & Environment

- Python 3.x  
- Google Colab (Linux)  

### 🧠 NLP & Machine Learning

- 🤗 Hugging Face Transformers  
  - `deepset/roberta-base-squad2`  
  - `deepset/tinyroberta-squad2`  

### 🌐 Web Scraping

- 🎭 Playwright – Dynamic & AJAX-rendered websites  
- 🕷 Scrapy – Structured crawling and pagination  

### 📦 Libraries & Dependencies

- asyncio, nest_asyncio  
- json, csv, pathlib  
- os, sys, subprocess, tempfile, site  
- Pandas – Data handling & visualization  

---

## 🧠 NLP Question Answering Module

### 📌 Description

- Uses pre-trained **RoBERTa models** fine-tuned on **SQuAD 2.0**
- Performs **extractive Question Answering** by identifying answer spans within a given context

### ⚙ Implementation Highlights

- Uses `pipeline("question-answering")` from Hugging Face
- **Inputs:** Question + Context  
- **Outputs:** Predicted Answer + Confidence Score  

### 📈 Key Observations

- ✅ High confidence for direct, fact-based questions  
- ⚠ Lower confidence for indirect or inference-based questions  
- 🚫 Correctly returns *no answer* for unrelated questions  
- ⚡ TinyRoBERTa performs efficiently for straightforward queries  

---

## 🌐 Web Scraping Module

### 🎭 Playwright (Dynamic Content)

**Target Website:**
- Laptops & Tablets – `webscraper.io`

**Features:**
- Handles AJAX and JavaScript rendering
- Supports:
  - “Load More” buttons
  - Multi-page pagination

**Data Extracted:**
- Product title  
- Price  
- Rating  
- Product URL  
- Image URL  

**Output Formats:**
- CSV  
- JSON  

---

### 🕷 Scrapy (Structured Crawling)

**Target Website:**
- 📚 `books.toscrape.com`

**Features:**
- Recursive pagination handling  
- CSS selector-based extraction  
- Textual → numeric rating conversion  
- Absolute URL normalization  

**Google Colab Challenge Solved Using:**
- Temporary execution scripts  
- Manual `PYTHONPATH` configuration  
- `scrapy.cmdline.execute()` via subprocess  

---

## 📊 Data Preprocessing

- ✂ Whitespace trimming  
- 🔢 Rating standardization  
- 🔗 Relative → absolute URL conversion  
- 📄 Direct serialization to CSV & JSON  

⚠ No advanced normalization or currency conversion was applied to preserve raw extracted values.

---

## 📈 Model Evaluation

### 🧠 QA Model Evaluation

- Confidence score used as reliability indicator  
- Performs best when context relevance is high  
- Robust handling of unanswerable queries  

### 🌐 Web Scraping Validation

Validated through:
- Product count verification  
- Pandas DataFrame inspection  
- CSV & JSON output integrity checks  

---

## 🏁 Conclusion

This milestone successfully demonstrates:

- ✅ Practical application of Transformer-based QA models  
- ✅ Efficient scraping of both dynamic and static websites  
- ✅ Proper tool selection based on website architecture  
- ✅ Real-world debugging in cloud-based environments  

---

## 🚀 Future Enhancements

- 📊 Add Exact Match & F1-score evaluation for QA  
- 💱 Normalize prices and textual attributes  
- 🛡 Handle CAPTCHAs and rate limiting  
- 🔄 Integrate scraped data directly into QA pipelines  
