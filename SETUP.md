# GEO Principles - Setup Guide

This guide will help you set up and run the GEO Principles application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Git (for version control)

## Quick Start

### 1. Clone the Repository (if not already done)

```bash
git clone <repository-url>
cd geo
```

### 2. Set Up Python Backend

#### Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
cd python
python app.py
```

The API server will start at `http://localhost:5000`

You should see:
```
Starting GEO Principles API server...
* Running on http://0.0.0.0:5000
```

### 4. Open the Frontend

Open a new terminal/command prompt and navigate to the project root:

**Option A: Simple File Open**
- Simply open `index.html` in your web browser

**Option B: Local Server (Recommended)**
```bash
# In the project root directory
python -m http.server 8000
```

Then open your browser to: `http://localhost:8000`

## Testing the Application

### 1. Test the API

Check if the API is running:
```bash
curl http://localhost:5000/
```

Or open `http://localhost:5000/` in your browser.

### 2. Test Content Analysis

Try the analyzer on the main page:
1. Open `index.html` in your browser
2. Navigate to the "Analyzer" section
3. Enter some sample content
4. Click "Analyze Content"

### Sample Content for Testing

```
What is Generative Engine Optimization?

Generative Engine Optimization (GEO) is the practice of optimizing content for AI-powered search engines and language models. Unlike traditional SEO which focuses on ranking in search results, GEO aims to make content more likely to be included in AI-generated responses.

Key principles include:
- Using semantic HTML structure
- Including authoritative citations from sources like nature.com
- Writing in clear, natural language
- Providing comprehensive information

According to a 2024 study, websites implementing GEO principles saw a 45% increase in AI-generated citations.

Source: https://example.com/geo-study
```

## Project Structure

```
geo/
├── index.html              # Main HTML page
├── css/
│   └── styles.css         # Styling
├── js/
│   ├── geo-analyzer.js    # Content analysis
│   ├── citation-manager.js # Citation management
│   ├── semantic-optimizer.js # Semantic optimization
│   └── main.js            # Main application logic
├── python/
│   ├── app.py             # Flask API server
│   ├── geo_analyzer.py    # Content analyzer
│   ├── nlp_processor.py   # NLP processing
│   ├── citation_validator.py # Citation validation
│   └── config.py          # Configuration
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
└── SETUP.md              # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```bash
# Flask configuration
DEBUG=True
SECRET_KEY=your-secret-key-here

# API settings
MAX_CONTENT_LENGTH=1048576
DEFAULT_LANGUAGE=en

# CORS settings
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
```

### Python Configuration

Edit `python/config.py` to customize:
- Scoring thresholds
- Citation validation rules
- NLP settings
- Rate limiting

## Development

### Running Tests

```bash
# From the python directory
pytest

# With coverage
pytest --cov=. --cov-report=html
```

### Code Quality

```bash
# Run pylint
pylint python/*.py

# Type checking
mypy python/
```

## Troubleshooting

### Backend Issues

**Problem: Port 5000 already in use**
```bash
# Change the port in python/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Problem: Module not found**
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Frontend Issues

**Problem: CORS errors**
- Ensure the backend is running
- Use a local server instead of opening the HTML file directly

**Problem: Analysis not working**
- Check browser console for errors (F12)
- Verify the API URL in `js/geo-analyzer.js` matches your backend

### Common Errors

**Python Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**JavaScript Errors**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console (F12) for specific errors

## Advanced Features

### Adding NLP Libraries (Optional)

For advanced NLP features, uncomment and install in `requirements.txt`:

```bash
pip install nltk spacy textblob
```

Then download required data:

```bash
python -m nltk.downloader punkt averaged_perceptron_tagger
python -m spacy download en_core_web_sm
```

### API Documentation

Access API documentation at:
```
http://localhost:5000/
```

Available endpoints:
- `POST /api/analyze` - Analyze content
- `POST /api/citations` - Validate citations
- `POST /api/optimize` - Get optimization suggestions
- `POST /api/schema` - Generate Schema.org markup
- `POST /api/nlp` - NLP analysis
- `GET /api/health` - Health check

## Deployment

### Deploy to Production

1. Set environment variables:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
```

2. Use a production server (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 python.app:app
```

3. Set up a reverse proxy (Nginx/Apache)

4. Enable HTTPS

### Deploy to Cloud

- **Heroku**: Add `Procfile` with `web: gunicorn python.app:app`
- **AWS**: Use Elastic Beanstalk or EC2
- **Google Cloud**: Use App Engine or Cloud Run
- **Azure**: Use App Service

## Support

For issues or questions:
1. Check the README.md
2. Review the code comments
3. Open an issue in the repository

## License

MIT License - See LICENSE file for details
