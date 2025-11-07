# Generative Engine Optimization (GEO) Principles - Skeleton

A comprehensive implementation demonstrating Generative Engine Optimization principles using HTML, JavaScript, and Python.

## 📋 Project Structure

```
geo/
├── index.html              # Main HTML with semantic markup
├── css/
│   └── styles.css         # Styling for the application
├── js/
│   ├── geo-analyzer.js    # GEO content analysis
│   ├── citation-manager.js # Citation and source management
│   ├── semantic-optimizer.js # Semantic markup optimization
│   └── main.js            # Main application logic
├── python/
│   ├── app.py             # Flask API server
│   ├── geo_analyzer.py    # Content analysis engine
│   ├── nlp_processor.py   # Natural language processing
│   └── citation_validator.py # Citation validation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 GEO Principles Covered

### 1. **Semantic Structure**
   - Proper HTML5 semantic elements
   - Schema.org structured data
   - Clear content hierarchy

### 2. **Authoritative Citations**
   - Source attribution
   - Citation management
   - Credibility scoring

### 3. **Content Quality**
   - Factual accuracy
   - Statistical validation
   - Context relevance

### 4. **Natural Language Optimization**
   - Clear, concise language
   - Question-answer format
   - Entity recognition

### 5. **Multi-modal Content**
   - Text optimization
   - Image alt text
   - Accessible content

### 6. **Information Hierarchy**
   - Logical content flow
   - Key information prominence
   - Summary generation

### 7. **Contextual Relevance**
   - Topic clustering
   - Semantic relationships
   - Intent matching

### 8. **Technical SEO for AI**
   - Structured data markup
   - Clean HTML
   - API accessibility

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Modern web browser
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd geo
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the Python backend**
```bash
python python/app.py
```

4. **Open the frontend**
```bash
# Simply open index.html in your browser
# Or use a local server:
python -m http.server 8000
```

## 📖 Usage

### Frontend (HTML/JavaScript)

The frontend demonstrates GEO principles through:
- Interactive content analyzer
- Citation manager
- Semantic markup visualizer
- Real-time optimization suggestions

### Backend (Python)

The Python backend provides:
- Content analysis API
- NLP processing
- Citation validation
- SEO scoring

### API Endpoints

```
POST /api/analyze        - Analyze content for GEO
POST /api/citations      - Validate citations
POST /api/optimize       - Get optimization suggestions
GET  /api/schema         - Generate schema.org markup
```

## 🔧 Configuration

Edit configuration in `python/config.py` for:
- API keys (for external NLP services)
- Scoring thresholds
- Citation sources

## 📚 GEO Best Practices Implemented

1. **Use semantic HTML5 elements** (`<article>`, `<section>`, `<header>`)
2. **Add structured data** (JSON-LD with Schema.org)
3. **Include authoritative citations** with proper attribution
4. **Optimize for question-answer format** (FAQ schema)
5. **Provide clear information hierarchy** (H1-H6 proper usage)
6. **Use descriptive meta tags** and alt attributes
7. **Implement clean URL structure**
8. **Ensure content accessibility**

## 🧪 Testing

```bash
# Run Python tests
python -m pytest python/tests/

# Check code quality
pylint python/
```

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please follow the GEO principles when adding content.

## 📧 Contact

For questions about GEO implementation, please open an issue.
