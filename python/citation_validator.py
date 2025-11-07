"""
Citation Validator
Validates and scores citations for GEO compliance
"""

import re
from typing import Dict, Any, List
from datetime import datetime
from urllib.parse import urlparse


class CitationValidator:
    """Validates citations and sources for credibility"""

    def __init__(self):
        # Authoritative domains for credibility scoring
        self.authoritative_domains = {
            # Educational
            '.edu': 50,
            # Government
            '.gov': 50,
            # Organizations
            '.org': 30,
            # Academic journals and databases
            'nature.com': 45,
            'science.org': 45,
            'sciencedirect.com': 40,
            'springer.com': 40,
            'ieee.org': 45,
            'acm.org': 45,
            'arxiv.org': 40,
            'scholar.google': 40,
            'pubmed.ncbi.nlm.nih.gov': 45,
            'researchgate.net': 35,
            # Reputable news sources
            'nytimes.com': 35,
            'wsj.com': 35,
            'bbc.com': 35,
            'reuters.com': 40,
            'apnews.com': 40,
            # Technical documentation
            'mozilla.org': 40,
            'w3.org': 45,
            'ietf.org': 45,
        }

    def validate(self, citation: Dict[str, str]) -> Dict[str, Any]:
        """
        Validate a citation and calculate credibility score

        Args:
            citation: Dictionary with citation details (title, url, author, date, etc.)

        Returns:
            Validation results with credibility score
        """
        result = {
            'valid': True,
            'credibility_score': 0,
            'max_score': 100,
            'checks': [],
            'warnings': [],
            'errors': []
        }

        # Check URL
        if 'url' in citation and citation['url']:
            url_check = self._validate_url(citation['url'])
            result['credibility_score'] += url_check['score']
            result['checks'].append(url_check)

            if not url_check['valid']:
                result['valid'] = False
                result['errors'].append(url_check['message'])
        else:
            result['warnings'].append('No URL provided')

        # Check author
        if 'author' in citation and citation['author']:
            author_check = self._validate_author(citation['author'])
            result['credibility_score'] += author_check['score']
            result['checks'].append(author_check)
        else:
            result['warnings'].append('No author provided')

        # Check date
        if 'date' in citation and citation['date']:
            date_check = self._validate_date(citation['date'])
            result['credibility_score'] += date_check['score']
            result['checks'].append(date_check)

            if not date_check['valid']:
                result['warnings'].append(date_check['message'])
        else:
            result['warnings'].append('No publication date provided')

        # Check title
        if 'title' in citation and citation['title']:
            title_check = self._validate_title(citation['title'])
            result['credibility_score'] += title_check['score']
            result['checks'].append(title_check)
        else:
            result['warnings'].append('No title provided')

        # Check publisher
        if 'publisher' in citation and citation['publisher']:
            result['credibility_score'] += 10
            result['checks'].append({
                'check': 'publisher',
                'valid': True,
                'score': 10,
                'message': 'Publisher provided'
            })

        # Calculate percentage
        result['percentage'] = round((result['credibility_score'] / result['max_score']) * 100)

        # Add overall assessment
        result['assessment'] = self._get_assessment(result['percentage'])

        return result

    def _validate_url(self, url: str) -> Dict[str, Any]:
        """Validate and score URL"""
        check = {
            'check': 'url',
            'valid': True,
            'score': 0,
            'message': ''
        }

        # Check URL format
        url_pattern = r'^https?://.+'
        if not re.match(url_pattern, url, re.IGNORECASE):
            check['valid'] = False
            check['message'] = 'Invalid URL format'
            return check

        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Check against authoritative domains
            score = 10  # Base score for valid URL

            for auth_domain, domain_score in self.authoritative_domains.items():
                if auth_domain in domain:
                    score = domain_score
                    check['message'] = f'Authoritative source: {auth_domain}'
                    break

            if not check['message']:
                check['message'] = 'Valid URL from standard domain'

            # Bonus for HTTPS
            if parsed.scheme == 'https':
                score += 5
                check['message'] += ' (secure)'

            check['score'] = score

        except Exception as e:
            check['valid'] = False
            check['message'] = f'URL parsing error: {str(e)}'

        return check

    def _validate_author(self, author: str) -> Dict[str, Any]:
        """Validate and score author"""
        check = {
            'check': 'author',
            'valid': True,
            'score': 0,
            'message': ''
        }

        # Check if author is not empty and has reasonable length
        if len(author.strip()) < 2:
            check['valid'] = False
            check['message'] = 'Author name too short'
            return check

        # Score based on author format
        if ',' in author or ' and ' in author.lower():
            # Multiple authors or formal format (Last, First)
            check['score'] = 20
            check['message'] = 'Multiple authors or formal format'
        elif len(author.split()) >= 2:
            # Full name
            check['score'] = 20
            check['message'] = 'Full author name provided'
        else:
            # Single name
            check['score'] = 10
            check['message'] = 'Author name provided'

        return check

    def _validate_date(self, date_str: str) -> Dict[str, Any]:
        """Validate and score publication date"""
        check = {
            'check': 'date',
            'valid': True,
            'score': 0,
            'message': ''
        }

        # Try to parse date
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y',
            '%B %d, %Y',
            '%b %d, %Y'
        ]

        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str.strip(), fmt)
                break
            except ValueError:
                continue

        if not parsed_date:
            check['valid'] = False
            check['message'] = 'Invalid date format'
            return check

        # Score based on recency
        current_year = datetime.now().year
        publication_year = parsed_date.year

        years_old = current_year - publication_year

        if years_old < 0:
            check['valid'] = False
            check['message'] = 'Future date not allowed'
            return check

        if years_old <= 1:
            check['score'] = 20
            check['message'] = 'Very recent (< 1 year)'
        elif years_old <= 3:
            check['score'] = 15
            check['message'] = 'Recent (1-3 years)'
        elif years_old <= 5:
            check['score'] = 10
            check['message'] = 'Moderately recent (3-5 years)'
        elif years_old <= 10:
            check['score'] = 5
            check['message'] = 'Older (5-10 years)'
        else:
            check['score'] = 2
            check['message'] = f'Old ({years_old} years)'

        return check

    def _validate_title(self, title: str) -> Dict[str, Any]:
        """Validate and score title"""
        check = {
            'check': 'title',
            'valid': True,
            'score': 0,
            'message': ''
        }

        title_length = len(title.strip())

        if title_length < 5:
            check['valid'] = False
            check['message'] = 'Title too short'
            return check

        if title_length < 20:
            check['score'] = 5
            check['message'] = 'Short but acceptable title'
        elif title_length < 100:
            check['score'] = 10
            check['message'] = 'Good descriptive title'
        else:
            check['score'] = 8
            check['message'] = 'Very long title'

        return check

    def _get_assessment(self, percentage: int) -> str:
        """Get overall assessment based on score"""
        if percentage >= 80:
            return 'Excellent - Highly credible source'
        elif percentage >= 60:
            return 'Good - Credible source'
        elif percentage >= 40:
            return 'Fair - Moderately credible'
        elif percentage >= 20:
            return 'Poor - Low credibility'
        else:
            return 'Very Poor - Unreliable source'

    def validate_multiple(self, citations: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Validate multiple citations

        Args:
            citations: List of citation dictionaries

        Returns:
            Summary of validation results
        """
        results = {
            'total': len(citations),
            'valid': 0,
            'invalid': 0,
            'average_score': 0,
            'citations': []
        }

        total_score = 0

        for citation in citations:
            validation = self.validate(citation)
            results['citations'].append(validation)

            if validation['valid']:
                results['valid'] += 1
            else:
                results['invalid'] += 1

            total_score += validation['percentage']

        if results['total'] > 0:
            results['average_score'] = round(total_score / results['total'], 2)

        return results

    def format_citation(self, citation: Dict[str, str], style: str = 'APA') -> str:
        """
        Format citation in specified style

        Args:
            citation: Citation dictionary
            style: Citation style (APA, MLA, Chicago, IEEE)

        Returns:
            Formatted citation string
        """
        if style.upper() == 'APA':
            return self._format_apa(citation)
        elif style.upper() == 'MLA':
            return self._format_mla(citation)
        elif style.upper() == 'CHICAGO':
            return self._format_chicago(citation)
        elif style.upper() == 'IEEE':
            return self._format_ieee(citation)
        else:
            return self._format_apa(citation)  # Default to APA

    def _format_apa(self, citation: Dict[str, str]) -> str:
        """Format in APA style"""
        parts = []

        if citation.get('author'):
            parts.append(f"{citation['author']}.")

        year = 'n.d.'
        if citation.get('date'):
            try:
                date_obj = datetime.strptime(citation['date'], '%Y-%m-%d')
                year = str(date_obj.year)
            except:
                year = citation['date']
        parts.append(f"({year}).")

        if citation.get('title'):
            parts.append(f"{citation['title']}.")

        if citation.get('publisher'):
            parts.append(f"{citation['publisher']}.")

        if citation.get('url'):
            parts.append(f"Retrieved from {citation['url']}")

        return ' '.join(parts)

    def _format_mla(self, citation: Dict[str, str]) -> str:
        """Format in MLA style"""
        parts = []

        if citation.get('author'):
            parts.append(f"{citation['author']}.")

        if citation.get('title'):
            parts.append(f'"{citation["title"]}."')

        if citation.get('publisher'):
            parts.append(f"{citation['publisher']},")

        if citation.get('date'):
            parts.append(f"{citation['date']}.")

        if citation.get('url'):
            parts.append(f"{citation['url']}.")

        return ' '.join(parts)

    def _format_chicago(self, citation: Dict[str, str]) -> str:
        """Format in Chicago style"""
        return self._format_mla(citation)  # Similar to MLA for basic implementation

    def _format_ieee(self, citation: Dict[str, str]) -> str:
        """Format in IEEE style"""
        parts = []

        if citation.get('author'):
            parts.append(f"{citation['author']},")

        if citation.get('title'):
            parts.append(f'"{citation["title"]},"')

        if citation.get('publisher'):
            parts.append(f"{citation['publisher']},")

        if citation.get('date'):
            parts.append(f"{citation['date']}.")

        if citation.get('url'):
            parts.append(f"[Online]. Available: {citation['url']}")

        return ' '.join(parts)
