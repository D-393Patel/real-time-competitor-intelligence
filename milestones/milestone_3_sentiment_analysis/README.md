Module 3: 
# Analyze customer reviews and implement Sentiment analysis

This project implements an intelligent dynamic pricing system for e-commerce books that adjusts prices in real time based on current news relevance and inventory levels. By leveraging semantic similarity models instead of simple keyword matching, the system identifies trending demand and optimizes pricing to maximize profit.

---

## 🚀 Key Idea

Public interest in certain topics fluctuates rapidly due to real-world events. When book content aligns with trending news, demand increases. This project captures that signal using semantic AI and adjusts prices dynamically rather than relying on static pricing.

---

## 🧠 Core Technologies

- **Web Scraping**: `BeautifulSoup`, `Requests`
- **Text Processing**: `NLTK`, `regex`
- **Semantic Similarity**
  - TF-IDF (baseline)
  - Sentence-BERT (`all-MiniLM-L6-v2`)
- **Vector Similarity**: Cosine similarity
- **Data Handling**: `Pandas`, `NumPy`

---

## 📊 Data Sources

- **Books**: `books.toscrape.com`  
  - Title  
  - Description  
  - Price  
  - Stock availability  

- **News Headlines**: `bbc.com/news`  
  - Real-time trending headlines  

---

## 🔍 Method Overview

1. Scrape book data and live news headlines.
2. Clean and normalize text (lowercasing, punctuation removal, stopword filtering).
3. Compute semantic similarity between book descriptions and news headlines.
4. Compare TF-IDF and Sentence-BERT for relevance detection.
5. Adjust prices dynamically based on:
   - News relevance score
   - Inventory level

---

## 🧪 Model Comparison

| Aspect | TF-IDF | Sentence-BERT |
|------|-------|---------------|
| Semantic understanding | ❌ | ✅ |
| Handles synonyms/context | ❌ | ✅ |
| Short text performance | Weak | Strong |
| Real-world relevance | Limited | High |

Sentence-BERT consistently outperformed TF-IDF by capturing contextual meaning rather than relying on exact keyword overlap.

---

## 💰 Dynamic Pricing Logic

Prices are adjusted using two signals:

- **News Relevance (Cosine Similarity)**
- **Stock Availability**

Examples:
- High relevance + high stock → price increase
- High relevance + low stock → controlled increase
- Low relevance + high stock → discount for clearance

This strategy helps maximize revenue while optimizing inventory turnover.

---

## 📈 Business Value

- Captures short-lived market trends
- Improves revenue during peak demand
- Reduces slow-moving inventory
- Moves beyond static pricing models
- Provides competitive advantage using external signals

---

## 🧪 Validation Approach

- A/B testing with static vs dynamic pricing
- KPI tracking (revenue, sales velocity, profit per unit)
- Simulation using historical news and sales data
- Continuous threshold tuning

---

## 📌 Project Status

✅ Concept validated  
🧪 Ready for real-world testing  
🚀 Extendable to other product categories  

---

## 📄 License

This project is for educational and research purposes. Feel free to fork, modify, and experiment.

---

## 🙌 Acknowledgments

- Sentence-Transformers library
- Open-source datasets
- BBC News & Books to Scrape (for learning purposes)
