"""
Flask API Server for GEO Principles
Provides backend endpoints for content analysis and optimization
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from geo_analyzer import GEOContentAnalyzer
from nlp_processor import NLPProcessor
from citation_validator import CitationValidator
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize analyzers
geo_analyzer = GEOContentAnalyzer()
nlp_processor = NLPProcessor()
citation_validator = CitationValidator()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'GEO Principles API',
        'version': '1.0.0',
        'endpoints': [
            '/api/analyze',
            '/api/citations',
            '/api/optimize',
            '/api/schema',
            '/api/nlp'
        ]
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """
    Analyze content for GEO compliance

    Request body:
    {
        "content": "text to analyze",
        "options": {
            "check_semantic": true,
            "check_citations": true,
            "check_readability": true,
            "check_keywords": true
        }
    }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400

        content = data['content']
        options = data.get('options', {})

        # Perform analysis
        results = geo_analyzer.analyze(content, options)

        return jsonify(results), 200

    except Exception as e:
        logger.error(f'Analysis error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/citations', methods=['POST'])
def validate_citations():
    """
    Validate citations in content

    Request body:
    {
        "citations": [
            {
                "title": "Citation title",
                "url": "https://example.com",
                "author": "Author name"
            }
        ]
    }
    """
    try:
        data = request.get_json()

        if not data or 'citations' not in data:
            return jsonify({'error': 'Citations are required'}), 400

        citations = data['citations']

        # Validate each citation
        results = []
        for citation in citations:
            validation = citation_validator.validate(citation)
            results.append(validation)

        return jsonify({
            'total': len(citations),
            'valid': sum(1 for r in results if r['valid']),
            'results': results
        }), 200

    except Exception as e:
        logger.error(f'Citation validation error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize', methods=['POST'])
def optimize_content():
    """
    Get optimization suggestions for content

    Request body:
    {
        "content": "text to optimize",
        "target": "readability|seo|geo"
    }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400

        content = data['content']
        target = data.get('target', 'geo')

        # Get optimization suggestions
        suggestions = geo_analyzer.get_optimization_suggestions(content, target)

        return jsonify(suggestions), 200

    except Exception as e:
        logger.error(f'Optimization error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/schema', methods=['POST'])
def generate_schema():
    """
    Generate Schema.org markup for content

    Request body:
    {
        "content": "text content",
        "type": "Article|FAQ|HowTo|Product",
        "metadata": {
            "title": "Title",
            "author": "Author",
            "date": "2024-01-01"
        }
    }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400

        content = data['content']
        schema_type = data.get('type', 'Article')
        metadata = data.get('metadata', {})

        # Generate schema
        schema = geo_analyzer.generate_schema(content, schema_type, metadata)

        return jsonify(schema), 200

    except Exception as e:
        logger.error(f'Schema generation error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/nlp', methods=['POST'])
def process_nlp():
    """
    Perform NLP analysis on content

    Request body:
    {
        "content": "text to analyze",
        "tasks": ["entities", "sentiment", "keywords"]
    }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400

        content = data['content']
        tasks = data.get('tasks', ['entities', 'keywords'])

        # Perform NLP processing
        results = nlp_processor.process(content, tasks)

        return jsonify(results), 200

    except Exception as e:
        logger.error(f'NLP processing error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GEO Principles API'
    }), 200


if __name__ == '__main__':
    logger.info('Starting GEO Principles API server...')
    app.run(debug=True, host='0.0.0.0', port=5000)
