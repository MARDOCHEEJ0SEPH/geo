"""
NLP Processor
Natural Language Processing for GEO content analysis
"""

import re
from typing import Dict, List, Any
from collections import Counter


class NLPProcessor:
    """Natural Language Processing for content analysis"""

    def __init__(self):
        # Common stop words to filter out
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
            'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
            'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
            'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
            'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
            'were', 'said', 'did', 'having', 'may', 'should', 'could', 'would'
        }

    def process(self, content: str, tasks: List[str] = None) -> Dict[str, Any]:
        """
        Process content with specified NLP tasks

        Args:
            content: Text content to process
            tasks: List of tasks to perform ['entities', 'sentiment', 'keywords']

        Returns:
            Dictionary of NLP results
        """
        if tasks is None:
            tasks = ['entities', 'keywords']

        results = {}

        if 'entities' in tasks:
            results['entities'] = self.extract_entities(content)

        if 'keywords' in tasks:
            results['keywords'] = self.extract_keywords(content)

        if 'sentiment' in tasks:
            results['sentiment'] = self.analyze_sentiment(content)

        if 'topics' in tasks:
            results['topics'] = self.extract_topics(content)

        return results

    def extract_entities(self, content: str) -> Dict[str, List[str]]:
        """
        Extract named entities from content

        Returns:
            Dictionary with entity types and their instances
        """
        entities = {
            'people': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'numbers': [],
            'emails': [],
            'urls': []
        }

        # Extract dates
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}\b'  # Just year
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities['dates'].extend(matches)

        entities['dates'] = list(set(entities['dates']))

        # Extract numbers and statistics
        number_patterns = [
            r'\b\d+\.?\d*%\b',  # Percentages
            r'\b\d+\.?\d*\s*(?:million|billion|trillion|thousand)\b',  # Large numbers
            r'\$\d+\.?\d*\b'  # Currency
        ]

        for pattern in number_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities['numbers'].extend(matches)

        entities['numbers'] = list(set(entities['numbers']))

        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = re.findall(email_pattern, content)

        # Extract URLs
        url_pattern = r'https?://[^\s<>"]+'
        entities['urls'] = re.findall(url_pattern, content)

        # Extract capitalized words (potential proper nouns)
        capitalized_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        capitalized = re.findall(capitalized_pattern, content)

        # Filter out common words and sentence starters
        common_words = {'The', 'A', 'An', 'This', 'That', 'These', 'Those', 'Here', 'There'}
        potential_names = [name for name in capitalized if name not in common_words]

        # Simple heuristic: 2+ capitalized words = organization, 1-2 words = could be person
        for name in potential_names:
            word_count = len(name.split())
            if word_count >= 2:
                entities['organizations'].append(name)
            else:
                entities['people'].append(name)

        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))

        return entities

    def extract_keywords(self, content: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Extract important keywords from content

        Args:
            content: Text content
            top_n: Number of top keywords to return

        Returns:
            List of keywords with frequency and relevance scores
        """
        # Tokenize and clean
        words = re.findall(r'\b[a-z]+\b', content.lower())

        # Filter stop words and short words
        filtered_words = [
            word for word in words
            if word not in self.stop_words and len(word) > 3
        ]

        # Count frequency
        word_freq = Counter(filtered_words)

        # Get top keywords
        top_keywords = word_freq.most_common(top_n)

        # Calculate relevance score (frequency / total words)
        total_words = len(filtered_words)
        keywords = []

        for word, freq in top_keywords:
            relevance = (freq / total_words) * 100
            keywords.append({
                'word': word,
                'frequency': freq,
                'relevance': round(relevance, 2)
            })

        return keywords

    def analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """
        Analyze sentiment of content
        Note: This is a basic implementation. For production, use NLTK or spaCy

        Returns:
            Sentiment analysis results
        """
        # Simple sentiment word lists
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'positive', 'best', 'better', 'love', 'like', 'happy', 'success',
            'successful', 'win', 'winner', 'effective', 'efficient', 'improve',
            'benefit', 'advantage', 'helpful', 'useful'
        }

        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'worse', 'hate',
            'dislike', 'sad', 'fail', 'failure', 'lose', 'loser', 'ineffective',
            'inefficient', 'problem', 'issue', 'disadvantage', 'harmful', 'useless'
        }

        # Tokenize
        words = re.findall(r'\b[a-z]+\b', content.lower())

        # Count sentiment words
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        neutral_count = len(words) - positive_count - negative_count

        # Calculate scores
        total = len(words)
        sentiment = {
            'positive': {
                'count': positive_count,
                'percentage': round((positive_count / total) * 100, 2) if total > 0 else 0
            },
            'negative': {
                'count': negative_count,
                'percentage': round((negative_count / total) * 100, 2) if total > 0 else 0
            },
            'neutral': {
                'count': neutral_count,
                'percentage': round((neutral_count / total) * 100, 2) if total > 0 else 0
            }
        }

        # Determine overall sentiment
        if positive_count > negative_count:
            sentiment['overall'] = 'positive'
        elif negative_count > positive_count:
            sentiment['overall'] = 'negative'
        else:
            sentiment['overall'] = 'neutral'

        # Calculate polarity score (-1 to 1)
        sentiment['polarity'] = round(
            (positive_count - negative_count) / total if total > 0 else 0,
            2
        )

        return sentiment

    def extract_topics(self, content: str, num_topics: int = 5) -> List[Dict[str, Any]]:
        """
        Extract main topics from content
        Note: Basic implementation. For production, use LDA or similar

        Returns:
            List of topics with relevance
        """
        # Get keywords
        keywords = self.extract_keywords(content, top_n=20)

        # Group keywords into potential topics
        # For this basic implementation, we'll use the top keywords as topics
        topics = []

        for i, keyword_data in enumerate(keywords[:num_topics]):
            topics.append({
                'topic_id': i + 1,
                'main_term': keyword_data['word'],
                'relevance': keyword_data['relevance'],
                'related_terms': self._find_related_terms(
                    keyword_data['word'],
                    content
                )
            })

        return topics

    def _find_related_terms(self, term: str, content: str, context_window: int = 5) -> List[str]:
        """
        Find terms that appear near the given term

        Args:
            term: Main term to find context for
            content: Full content
            context_window: Number of words to check before/after

        Returns:
            List of related terms
        """
        # Tokenize
        words = re.findall(r'\b[a-z]+\b', content.lower())

        related = []

        # Find all occurrences of the term
        for i, word in enumerate(words):
            if word == term:
                # Get context window
                start = max(0, i - context_window)
                end = min(len(words), i + context_window + 1)
                context = words[start:end]

                # Add non-stop words
                for ctx_word in context:
                    if (ctx_word != term and
                        ctx_word not in self.stop_words and
                        len(ctx_word) > 3):
                        related.append(ctx_word)

        # Return top 3 most common related terms
        if related:
            related_freq = Counter(related)
            return [word for word, _ in related_freq.most_common(3)]

        return []

    def calculate_readability_score(self, content: str) -> Dict[str, Any]:
        """
        Calculate various readability metrics

        Returns:
            Dictionary of readability scores
        """
        # Count sentences, words, syllables
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = re.findall(r'\b[a-z]+\b', content.lower())
        word_count = len(words)
        sentence_count = len(sentences)

        # Estimate syllables (rough approximation)
        syllable_count = sum(self._count_syllables(word) for word in words)

        # Calculate metrics
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0

        # Flesch Reading Ease Score
        # Formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        flesch_score = (
            206.835 -
            1.015 * avg_words_per_sentence -
            84.6 * avg_syllables_per_word
        )

        # Flesch-Kincaid Grade Level
        # Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        fk_grade = (
            0.39 * avg_words_per_sentence +
            11.8 * avg_syllables_per_word -
            15.59
        )

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'flesch_reading_ease': round(flesch_score, 2),
            'flesch_kincaid_grade': round(fk_grade, 2),
            'difficulty': self._get_difficulty_level(flesch_score)
        }

    def _count_syllables(self, word: str) -> int:
        """
        Estimate syllable count for a word
        Note: This is a rough approximation
        """
        word = word.lower()
        vowels = 'aeiou'
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1

        # Ensure at least one syllable
        return max(1, syllable_count)

    def _get_difficulty_level(self, flesch_score: float) -> str:
        """Get difficulty level from Flesch score"""
        if flesch_score >= 90:
            return 'Very Easy'
        elif flesch_score >= 80:
            return 'Easy'
        elif flesch_score >= 70:
            return 'Fairly Easy'
        elif flesch_score >= 60:
            return 'Standard'
        elif flesch_score >= 50:
            return 'Fairly Difficult'
        elif flesch_score >= 30:
            return 'Difficult'
        else:
            return 'Very Difficult'
