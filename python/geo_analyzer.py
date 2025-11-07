"""
GEO Content Analyzer
Analyzes content for Generative Engine Optimization compliance
"""

import re
from typing import Dict, List, Any
from datetime import datetime


class GEOContentAnalyzer:
    """Main analyzer for GEO content optimization"""

    def __init__(self):
        self.max_score = 100

    def analyze(self, content: str, options: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Analyze content for GEO compliance

        Args:
            content: Text content to analyze
            options: Analysis options dict

        Returns:
            Analysis results dictionary
        """
        if options is None:
            options = {
                'check_semantic': True,
                'check_citations': True,
                'check_readability': True,
                'check_keywords': True
            }

        results = {
            'score': 0,
            'max_score': self.max_score,
            'checks': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }

        # Run requested checks
        if options.get('check_semantic'):
            semantic_result = self.check_semantic_structure(content)
            results['checks'].append(semantic_result)
            results['score'] += semantic_result['score']

        if options.get('check_citations'):
            citation_result = self.check_citations(content)
            results['checks'].append(citation_result)
            results['score'] += citation_result['score']

        if options.get('check_readability'):
            readability_result = self.check_readability(content)
            results['checks'].append(readability_result)
            results['score'] += readability_result['score']

        if options.get('check_keywords'):
            keyword_result = self.check_keywords(content)
            results['checks'].append(keyword_result)
            results['score'] += keyword_result['score']

        # Calculate percentage
        results['percentage'] = round((results['score'] / self.max_score) * 100)

        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results['checks'])

        return results

    def check_semantic_structure(self, content: str) -> Dict[str, Any]:
        """Check semantic structure of content"""
        result = {
            'name': 'Semantic Structure',
            'score': 0,
            'max_score': 25,
            'passed': [],
            'failed': []
        }

        # Check for headings
        heading_patterns = [
            r'^#{1,6}\s+.+',  # Markdown headings
            r'<h[1-6]>.+</h[1-6]>',  # HTML headings
        ]

        has_headings = any(re.search(pattern, content, re.MULTILINE)
                          for pattern in heading_patterns)

        if has_headings:
            result['score'] += 10
            result['passed'].append('Contains heading structure')
        else:
            result['failed'].append('Missing heading structure (H1-H6)')

        # Check for paragraph structure
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 1:
            result['score'] += 10
            result['passed'].append(f'Contains {len(paragraphs)} paragraphs')
        else:
            result['failed'].append('Missing clear paragraph breaks')

        # Check for lists
        list_patterns = [
            r'^\s*[-*+]\s+.+',  # Unordered lists
            r'^\s*\d+\.\s+.+',  # Ordered lists
            r'<[uo]l>.+</[uo]l>',  # HTML lists
        ]

        has_lists = any(re.search(pattern, content, re.MULTILINE)
                       for pattern in list_patterns)

        if has_lists:
            result['score'] += 5
            result['passed'].append('Contains lists for structured information')
        else:
            result['failed'].append('Consider using lists for better structure')

        return result

    def check_citations(self, content: str) -> Dict[str, Any]:
        """Check for citations and sources"""
        result = {
            'name': 'Citations & Sources',
            'score': 0,
            'max_score': 25,
            'passed': [],
            'failed': []
        }

        # Check for URLs
        url_pattern = r'https?://[^\s<>"]+'
        urls = re.findall(url_pattern, content)

        if urls:
            result['score'] += 10
            result['passed'].append(f'Found {len(urls)} external link(s)')
        else:
            result['failed'].append('No external citations or sources found')

        # Check for citation markers
        citation_patterns = [
            r'\[\d+\]',  # [1], [2], etc.
            r'<cite>',  # HTML cite tag
            r'(?i)source:',  # "Source:" mentions
            r'\(\w+,?\s+\d{4}\)',  # (Author, 2024)
        ]

        has_citations = any(re.search(pattern, content)
                           for pattern in citation_patterns)

        if has_citations:
            result['score'] += 10
            result['passed'].append('Contains citation markers')
        else:
            result['failed'].append('Missing citation markers or source attribution')

        # Check for dates
        date_patterns = [
            r'\b\d{4}\b',  # Year
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY
        ]

        has_dates = any(re.search(pattern, content)
                       for pattern in date_patterns)

        if has_dates:
            result['score'] += 5
            result['passed'].append('Contains dates for context')
        else:
            result['failed'].append('Consider adding dates for temporal context')

        return result

    def check_readability(self, content: str) -> Dict[str, Any]:
        """Check readability and natural language"""
        result = {
            'name': 'Readability & Natural Language',
            'score': 0,
            'max_score': 25,
            'passed': [],
            'failed': []
        }

        # Calculate average sentence length
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = content.split()
        words = [w for w in words if w.strip()]

        if sentences:
            avg_sentence_length = len(words) / len(sentences)

            if avg_sentence_length < 20:
                result['score'] += 10
                result['passed'].append(
                    f'Good average sentence length ({avg_sentence_length:.1f} words)'
                )
            else:
                result['failed'].append(
                    f'Sentences too long (avg: {avg_sentence_length:.1f} words, aim for <20)'
                )

        # Check for question format
        question_count = len(re.findall(r'\?', content))
        if question_count > 0:
            result['score'] += 5
            result['passed'].append(f'Uses question-answer format ({question_count} questions)')
        else:
            result['failed'].append('Consider using Q&A format for better GEO')

        # Check for passive voice
        passive_indicators = re.findall(
            r'\b(?:was|were|been|being)\s+\w+ed\b',
            content,
            re.IGNORECASE
        )

        if len(passive_indicators) < len(sentences) * 0.3:
            result['score'] += 10
            result['passed'].append('Mostly uses active voice')
        else:
            result['failed'].append('Too much passive voice detected')

        return result

    def check_keywords(self, content: str) -> Dict[str, Any]:
        """Check keyword optimization"""
        result = {
            'name': 'Keyword Optimization',
            'score': 0,
            'max_score': 25,
            'passed': [],
            'failed': []
        }

        # Check content length
        words = content.split()
        word_count = len([w for w in words if w.strip()])

        if word_count >= 300:
            result['score'] += 10
            result['passed'].append(f'Good content length ({word_count} words)')
        else:
            result['failed'].append(f'Content too short ({word_count} words, aim for 300+)')

        # Analyze keyword density
        word_freq = {}
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            if len(word_lower) > 4:  # Only significant words
                word_freq[word_lower] = word_freq.get(word_lower, 0) + 1

        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        if top_keywords:
            result['score'] += 10
            keywords_str = ', '.join([f"{word} ({count})" for word, count in top_keywords])
            result['passed'].append(f'Top keywords: {keywords_str}')

        # Check for statistics/numbers
        number_patterns = [
            r'\d+%',  # Percentages
            r'\d+\s+(?:percent|million|billion|thousand)',  # Written numbers
        ]

        has_numbers = any(re.search(pattern, content, re.IGNORECASE)
                         for pattern in number_patterns)

        if has_numbers:
            result['score'] += 5
            result['passed'].append('Contains statistical data')
        else:
            result['failed'].append('Consider adding statistics or data points')

        return result

    def generate_recommendations(self, checks: List[Dict]) -> List[Dict]:
        """Generate recommendations based on check results"""
        recommendations = []

        for check in checks:
            if check['failed']:
                priority = 'high' if check['score'] < check['max_score'] * 0.5 else 'medium'
                recommendations.append({
                    'category': check['name'],
                    'priority': priority,
                    'suggestions': check['failed']
                })

        return recommendations

    def get_optimization_suggestions(self, content: str, target: str = 'geo') -> Dict[str, Any]:
        """Get specific optimization suggestions"""
        suggestions = {
            'target': target,
            'suggestions': []
        }

        # Analyze content
        analysis = self.analyze(content)

        # Generate targeted suggestions based on target
        if target == 'readability':
            suggestions['suggestions'] = self._get_readability_suggestions(content, analysis)
        elif target == 'seo':
            suggestions['suggestions'] = self._get_seo_suggestions(content, analysis)
        else:  # geo
            suggestions['suggestions'] = self._get_geo_suggestions(content, analysis)

        return suggestions

    def _get_geo_suggestions(self, content: str, analysis: Dict) -> List[str]:
        """Get GEO-specific suggestions"""
        suggestions = []

        if analysis['percentage'] < 80:
            suggestions.append('Overall GEO score needs improvement')

        for rec in analysis['recommendations']:
            if rec['priority'] == 'high':
                suggestions.extend(rec['suggestions'][:2])  # Top 2 from high priority

        return suggestions

    def _get_readability_suggestions(self, content: str, analysis: Dict) -> List[str]:
        """Get readability-specific suggestions"""
        return ['Use shorter sentences', 'Add more questions', 'Use active voice']

    def _get_seo_suggestions(self, content: str, analysis: Dict) -> List[str]:
        """Get SEO-specific suggestions"""
        return ['Add more keywords', 'Include meta descriptions', 'Use heading hierarchy']

    def generate_schema(self, content: str, schema_type: str, metadata: Dict) -> Dict:
        """Generate Schema.org markup"""
        schema = {
            '@context': 'https://schema.org',
            '@type': schema_type
        }

        # Add metadata
        if schema_type == 'Article':
            schema.update({
                'headline': metadata.get('title', ''),
                'description': metadata.get('description', ''),
                'author': {
                    '@type': 'Person',
                    'name': metadata.get('author', '')
                },
                'datePublished': metadata.get('date', datetime.now().isoformat())
            })

        return schema
