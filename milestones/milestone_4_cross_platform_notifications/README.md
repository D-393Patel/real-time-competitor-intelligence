# 📚 Cross-Platform Integration & Notification System  
## Dynamic Book Pricing & Competitor Intelligence

This module implements an **automated competitor price intelligence system** for an e-commerce platform specializing in books.  
The system dynamically gathers book data, converts identifiers into standardized **ISBN formats**, queries **competitor pricing APIs**, and performs detailed **price comparisons** to recommend optimal pricing strategies.

The solution enables **data-driven decision-making** by continuously identifying opportunities to improve competitiveness or maximize profit margins.

---

## 🎯 Objectives

- 🔍 Scrape book data (title, UPC, price) from a source website  
- 🔄 Convert non-standard UPC identifiers into ISBN-10 / ISBN-13  
- 🌐 Retrieve real-time competitor pricing via external APIs  
- 📊 Perform accurate price comparison & difference analysis  
- 💡 Generate dynamic price adjustment recommendations  

---

## 🔄 High-Level System Workflow

1. 📥 Scrape book data from `books.toscrape.com`  
2. 🔢 Convert book titles → ISBN using Google Books API  
3. 🌍 Query competitor pricing using BooksRun API  
4. 🧹 Clean, normalize, and merge multi-source data  
5. 📈 Analyze price differences and suggest adjustments  
6. 📄 Generate actionable pricing reports  

---

## 🛠 Tools & Technologies Used

### 🔠 Programming & Data Handling

- **Python**
- **Pandas** – DataFrames, merging, cleaning, calculations
- **CSV** – Persistent structured storage

### 🌐 Web & API Interaction

- **Requests** – REST API communication
- **BeautifulSoup** – HTML parsing for scraping
- **REST APIs** – Google Books API & BooksRun API

### 📚 External APIs

- 📘 **Google Books API** – ISBN extraction
- 🏷 **BooksRun API** – Competitor pricing intelligence

---

## 🔢 Task 1: UPC to ISBN Conversion

### 📌 Why Conversion Is Needed

- UPC identifies retail products, not specific book editions
- ISBN uniquely identifies book editions and formats
- Book pricing APIs require ISBNs for accurate results

### ⚙ Methodology

- Used book titles as search queries to Google Books API
- Extracted identifiers from `industryIdentifiers`
- Prioritized **ISBN-13**, with fallback to **ISBN-10**
- Gracefully handled missing or invalid ISBNs

### 📤 Output

- Valid ISBN-10 / ISBN-13 mappings
- Structured dataset ready for competitor API queries

---

## 🌐 Task 2: Competitor Price Retrieval

### 🎯 Purpose

Enable real-time competitive intelligence to:

- 🔻 Reduce prices for better competitiveness
- 🔺 Increase prices to improve profit margins
- ⚖ Maintain optimal pricing balance

### ⚙ Implementation

- Queried BooksRun API using ISBN identifiers
- Extracted pricing data from:
  - New offers
  - Used offers
  - Marketplace listings
- Implemented robust error handling for:
  - Invalid ISBNs
  - Missing offers
  - API and network failures

### 📤 Output

- ISBN-based competitor pricing dataset
- Raw API responses retained for traceability and debugging

---

## 📊 Task 3: Price Comparison & Analysis

### 🔗 Data Integration Strategy

Merged the following datasets:

- Scraped website prices
- Google Books ISBN mappings
- Competitor pricing data

Used **inner joins** to ensure data integrity and consistency.

### 🧹 Data Cleaning & Normalization

- Removed currency symbols (£, $)
- Stripped descriptive labels (New, Used, Marketplace)
- Converted price fields to floating-point values
- Handled invalid or missing entries using NaN-safe logic

### 📈 Price Metrics Generated

- Absolute price difference
- Percentage price difference
- Competitiveness indicators per book

---

## 📈 Evaluation & Insights

- ✅ Accurate ISBN identification enables reliable API matching  
- ✅ Data normalization ensures correct numerical comparisons  
- ✅ System handles edge cases without pipeline failure  
- 📊 Enables clear, data-driven pricing recommendations per book  

---

## ✅ Module Outcome

- Fully automated competitor pricing intelligence pipeline
- Cross-platform data integration achieved
- Actionable pricing recommendations generated
- Strong foundation established for dynamic pricing systems
