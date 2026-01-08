Milestone 2: Webscrapping and data aggregation
This module focuses on two core data engineering and NLP tasks:

Question Answering (QA) using Transformer-based NLP models

Web Scraping and Data Aggregation from both dynamic and structured websites

The goal is to analyze QA model performance under varying question–context scenarios and to implement robust web scraping pipelines using industry-standard tools.

🎯 Objectives

🔍 Evaluate transformer-based extractive Question Answering models

🌐 Scrape dynamic JavaScript-rendered websites using Playwright

🕷 Crawl structured paginated websites using Scrapy

📁 Store extracted data in CSV and JSON formats

⚙ Address real-world environment challenges in Google Colab

🛠 Tools & Technologies Used
🔠 Programming & Environment

Python 3.x

Google Colab (Linux)

🧠 NLP & Machine Learning

🤗 Hugging Face Transformers

deepset/roberta-base-squad2

deepset/tinyroberta-squad2

🌐 Web Scraping

🎭 Playwright (Dynamic & AJAX pages)

🕷 Scrapy (Structured crawling)

📦 Libraries & Dependencies

asyncio, nest_asyncio

json, csv, pathlib

os, sys, subprocess, tempfile, site

Pandas (Data handling & visualization)

🧠 NLP Question Answering Module
📌 Description

Uses pre-trained RoBERTa models fine-tuned on SQuAD 2.0

Performs extractive QA by identifying answer spans in a given context

⚙ Implementation Highlights

pipeline("question-answering") from Hugging Face

Inputs: Question + Context

Outputs: Answer + Confidence Score

📈 Key Observations

✅ High confidence for direct questions

⚠ Low confidence for indirect or inference-based questions

🚫 Correctly returns no answer for unrelated questions

⚡ TinyRoBERTa performs efficiently for straightforward queries

🌐 Web Scraping Module
🎭 Playwright (Dynamic Content)

Targets:

Laptops & Tablets – webscraper.io

Features:

Handles AJAX & JavaScript rendering

Supports:

“Load More” buttons

Multi-page pagination

Data Extracted:

Product Title

Price

Rating

Product URL

Image URL

Output Formats: CSV & JSON

🕷 Scrapy (Structured Crawling)

Target Website:

📚 books.toscrape.com

Features:

Recursive pagination

CSS selector-based extraction

Textual → numeric rating conversion

Absolute URL normalization

Colab Challenge Solved Using:

Temporary execution script

Manual PYTHONPATH setup

scrapy.cmdline.execute() via subprocess

📊 Data Preprocessing

✂ Whitespace trimming

🔢 Rating standardization

🔗 Relative → Absolute URL conversion

📄 Direct serialization to CSV & JSON

No advanced normalization or currency conversion was applied to preserve raw extracted values.

📈 Model Evaluation
🧠 QA Model

Confidence score used as reliability indicator

Performs best with high context relevance

Robust handling of unanswerable queries

🌐 Web Scraping

Validated through:

Product count verification

Pandas DataFrame inspection

CSV & JSON output integrity

🏁 Conclusion

This project successfully demonstrates:

✅ Practical application of Transformer-based QA models

✅ Efficient scraping of dynamic and static websites

✅ Proper tool selection based on website architecture

✅ Real-world debugging in cloud-based environments

🚀 Future Enhancements

📊 Add Exact Match & F1-score evaluation for QA

💱 Normalize prices and textual attributes

🛡 Handle CAPTCHAs and rate limiting

🔄 Integrate scraped data directly into QA pipelines
