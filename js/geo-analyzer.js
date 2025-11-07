/**
 * GEO Analyzer Module
 * Analyzes content for Generative Engine Optimization compliance
 */

class GEOAnalyzer {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
    }

    /**
     * Analyze content for GEO compliance
     * @param {string} content - Content to analyze
     * @param {Object} options - Analysis options
     * @returns {Promise<Object>} - Analysis results
     */
    async analyzeContent(content, options = {}) {
        try {
            // For now, perform client-side analysis
            // In production, this would call the Python backend
            const results = {
                score: 0,
                maxScore: 100,
                checks: [],
                recommendations: []
            };

            // Check 1: Semantic Structure
            if (options.checkSemantic) {
                const semanticResult = this.checkSemanticStructure(content);
                results.checks.push(semanticResult);
                results.score += semanticResult.score;
            }

            // Check 2: Citations
            if (options.checkCitations) {
                const citationResult = this.checkCitations(content);
                results.checks.push(citationResult);
                results.score += citationResult.score;
            }

            // Check 3: Readability
            if (options.checkReadability) {
                const readabilityResult = this.checkReadability(content);
                results.checks.push(readabilityResult);
                results.score += readabilityResult.score;
            }

            // Check 4: Keywords
            if (options.checkKeywords) {
                const keywordResult = this.checkKeywords(content);
                results.checks.push(keywordResult);
                results.score += keywordResult.score;
            }

            // Calculate percentage
            results.percentage = Math.round((results.score / results.maxScore) * 100);

            // Generate recommendations
            results.recommendations = this.generateRecommendations(results.checks);

            return results;

        } catch (error) {
            console.error('Analysis error:', error);
            throw error;
        }
    }

    /**
     * Check semantic structure of content
     * @param {string} content - Content to check
     * @returns {Object} - Check result
     */
    checkSemanticStructure(content) {
        const result = {
            name: 'Semantic Structure',
            score: 0,
            maxScore: 25,
            passed: [],
            failed: []
        };

        // Check for headings
        const hasHeadings = /#{1,6}\s+.+|<h[1-6]>.+<\/h[1-6]>/i.test(content);
        if (hasHeadings) {
            result.score += 10;
            result.passed.push('Contains heading structure');
        } else {
            result.failed.push('Missing heading structure (H1-H6)');
        }

        // Check for paragraphs
        const hasParagraphs = content.split('\n\n').length > 1 || /<p>.+<\/p>/i.test(content);
        if (hasParagraphs) {
            result.score += 10;
            result.passed.push('Contains paragraph structure');
        } else {
            result.failed.push('Missing clear paragraph breaks');
        }

        // Check for lists
        const hasLists = /[-*]\s+.+|<[uo]l>.+<\/[uo]l>/i.test(content);
        if (hasLists) {
            result.score += 5;
            result.passed.push('Contains lists for structured information');
        } else {
            result.failed.push('Consider using lists for better structure');
        }

        return result;
    }

    /**
     * Check for citations and sources
     * @param {string} content - Content to check
     * @returns {Object} - Check result
     */
    checkCitations(content) {
        const result = {
            name: 'Citations & Sources',
            score: 0,
            maxScore: 25,
            passed: [],
            failed: []
        };

        // Check for URLs
        const urlPattern = /(https?:\/\/[^\s]+)/g;
        const urls = content.match(urlPattern) || [];
        if (urls.length > 0) {
            result.score += 10;
            result.passed.push(`Found ${urls.length} external link(s)`);
        } else {
            result.failed.push('No external citations or sources found');
        }

        // Check for citation markers
        const hasCitations = /\[[\d]+\]|<cite>|Source:/i.test(content);
        if (hasCitations) {
            result.score += 10;
            result.passed.push('Contains citation markers');
        } else {
            result.failed.push('Missing citation markers or source attribution');
        }

        // Check for dates
        const hasDate = /\d{4}|\d{1,2}\/\d{1,2}\/\d{2,4}/g.test(content);
        if (hasDate) {
            result.score += 5;
            result.passed.push('Contains dates for context');
        } else {
            result.failed.push('Consider adding dates for temporal context');
        }

        return result;
    }

    /**
     * Check readability and natural language
     * @param {string} content - Content to check
     * @returns {Object} - Check result
     */
    checkReadability(content) {
        const result = {
            name: 'Readability & Natural Language',
            score: 0,
            maxScore: 25,
            passed: [],
            failed: []
        };

        // Calculate average sentence length
        const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const words = content.split(/\s+/).filter(w => w.length > 0);
        const avgSentenceLength = words.length / sentences.length;

        if (avgSentenceLength < 20) {
            result.score += 10;
            result.passed.push('Good average sentence length (concise)');
        } else {
            result.failed.push('Sentences are too long (average > 20 words)');
        }

        // Check for question format
        const hasQuestions = /\?/g.test(content);
        if (hasQuestions) {
            result.score += 5;
            result.passed.push('Uses question-answer format');
        } else {
            result.failed.push('Consider using Q&A format for better GEO');
        }

        // Check for active voice indicators
        const passiveIndicators = /\b(was|were|been|being)\s+\w+ed\b/gi;
        const passiveCount = (content.match(passiveIndicators) || []).length;
        if (passiveCount < sentences.length * 0.3) {
            result.score += 10;
            result.passed.push('Mostly uses active voice');
        } else {
            result.failed.push('Too much passive voice detected');
        }

        return result;
    }

    /**
     * Check keyword optimization
     * @param {string} content - Content to check
     * @returns {Object} - Check result
     */
    checkKeywords(content) {
        const result = {
            name: 'Keyword Optimization',
            score: 0,
            maxScore: 25,
            passed: [],
            failed: []
        };

        // Check content length
        const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
        if (wordCount >= 300) {
            result.score += 10;
            result.passed.push(`Good content length (${wordCount} words)`);
        } else {
            result.failed.push(`Content too short (${wordCount} words, aim for 300+)`);
        }

        // Check for keyword density (basic analysis)
        const words = content.toLowerCase().split(/\s+/);
        const wordFreq = {};
        words.forEach(word => {
            if (word.length > 4) { // Only count significant words
                wordFreq[word] = (wordFreq[word] || 0) + 1;
            }
        });

        const topWords = Object.entries(wordFreq)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        if (topWords.length > 0) {
            result.score += 10;
            result.passed.push(`Top keywords identified: ${topWords.map(w => w[0]).join(', ')}`);
        }

        // Check for numbers/statistics
        const hasNumbers = /\d+%|\d+\s+(percent|million|billion|thousand)/i.test(content);
        if (hasNumbers) {
            result.score += 5;
            result.passed.push('Contains statistical data');
        } else {
            result.failed.push('Consider adding statistics or data points');
        }

        return result;
    }

    /**
     * Generate recommendations based on check results
     * @param {Array} checks - Array of check results
     * @returns {Array} - Array of recommendations
     */
    generateRecommendations(checks) {
        const recommendations = [];

        checks.forEach(check => {
            if (check.failed.length > 0) {
                recommendations.push({
                    category: check.name,
                    priority: check.score < check.maxScore * 0.5 ? 'high' : 'medium',
                    suggestions: check.failed
                });
            }
        });

        return recommendations;
    }

    /**
     * Call Python backend API for advanced analysis
     * @param {string} content - Content to analyze
     * @param {Object} options - Analysis options
     * @returns {Promise<Object>} - Analysis results
     */
    async callBackendAPI(content, options) {
        try {
            const response = await fetch(`${this.apiUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content, options })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.warn('Backend API not available, using client-side analysis:', error);
            return null;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GEOAnalyzer;
}
