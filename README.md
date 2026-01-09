# 📚 Real-Time Competitor Intelligence & LLM-Driven Dynamic Pricing System

## 📖 Project Overview

This project implements an **end-to-end intelligent pricing system** that combines **web scraping, machine learning, deep learning, and Large Language Models (LLMs)** to analyze competitor book data and dynamically adjust pricing strategies.

The system is developed across **four milestones**, progressing from foundational neural network implementation to **LLM-powered competitor intelligence and pricing decision-making**.

---

## 🧩 Project Milestones Overview

| Milestone | Description |
|---------|------------|
| **Milestone 1** | Neural Network from Scratch (MNIST Classification) |
| **Milestone 2** | Web Scraping & Data Extraction |
| **Milestone 3** | LLM-Based Semantic & Sentiment Analysis |
| **Milestone 4** | Dynamic Pricing Logic & Results |

---

## 🛠️ Technologies Used

- **Python**
- **NumPy, Pandas**
- **Requests, BeautifulSoup**
- **Pillow (PIL)**
- **Matplotlib**
- **Large Language Models (Gemini / GPT)**
- **CSV-based Data Pipelines**

---

## 🚀 Milestone 1: Neural Network from Scratch

### Objective
To build a **Deep Neural Network from scratch using NumPy**, enabling a clear understanding of core deep learning concepts without relying on frameworks such as TensorFlow or PyTorch.

### Key Features
- 4-layer neural network architecture  
  *(Input → Hidden Layer 1 → Hidden Layer 2 → Output)*
- Implemented components:
  - Forward propagation
  - Backpropagation
  - Stochastic Gradient Descent (SGD)
- Activation functions:
  - Sigmoid
  - ReLU
  - Softmax
- Loss function:
  - Binary Cross-Entropy

### Results
- **Training Accuracy:** 99.90%
- **Validation Accuracy:** 97.45%
- ReLU activation demonstrated faster convergence and lower validation loss compared to sigmoid.

---

## 🌐 Milestone 2: Web Scraping & Data Extraction

### Website Used
**books.toscrape.com** — an educational e-commerce platform explicitly designed for practicing web scraping techniques.

### Data Extracted
- Book Title
- Price (GBP)
- Category / Genre
- Stock Availability
- Star Rating
- Product Description
- Technical Metadata (UPC, tax details, price including/excluding tax)

### Workflow
1. Genre-wise crawling with pagination handling
2. Product-level data extraction
3. Structured storage in CSV format
4. Dataset preparation for analysis and pricing models

---

## 🧠 Milestone 3: LLM-Based Semantic & Sentiment Analysis

### Objective
To leverage **Large Language Models (LLMs)** for extracting semantic meaning and sentiment from book descriptions and metadata.

### LLM Capabilities Utilized
- Contextual understanding of product descriptions
- Sentiment classification (Positive / Neutral / Negative)
- Demand inference using keywords and textual tone
- Context-aware pricing recommendations

### Outcome
LLM analysis enhances raw scraped data with **qualitative intelligence**, enabling informed and explainable pricing decisions beyond numeric features.

---

## 💰 Milestone 4: Dynamic Pricing Logic & Results

### Pricing Strategy
Book prices are dynamically adjusted based on:
- Competitor pricing
- Stock availability
- Product ratings
- LLM-generated sentiment scores
- Demand signals inferred from descriptions

### Price Adjustment Rules (Examples)
- High rating + positive sentiment → **Price Increase**
- Low rating or negative sentiment → **Price Decrease**
- Low stock + high demand → **Premium pricing**
- Overstocked items → **Discount pricing**

### Output
- Original vs adjusted price comparison
- Pricing decision explanations
- CSV-based pricing reports
- Visualized pricing changes for analysis

---

## 📊 System Architecture (High-Level)

