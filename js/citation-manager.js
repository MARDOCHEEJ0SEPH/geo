/**
 * Citation Manager Module
 * Manages citations and source validation for GEO
 */

class CitationManager {
    constructor() {
        this.citations = [];
        this.citationFormats = {
            APA: 'apa',
            MLA: 'mla',
            CHICAGO: 'chicago',
            IEEE: 'ieee'
        };
    }

    /**
     * Add a citation to the manager
     * @param {Object} citation - Citation details
     * @returns {number} - Citation ID
     */
    addCitation(citation) {
        const id = this.citations.length + 1;
        const citationEntry = {
            id,
            title: citation.title || '',
            author: citation.author || '',
            url: citation.url || '',
            date: citation.date || new Date().toISOString().split('T')[0],
            publisher: citation.publisher || '',
            accessed: new Date().toISOString().split('T')[0],
            credibilityScore: 0
        };

        // Calculate credibility score
        citationEntry.credibilityScore = this.calculateCredibilityScore(citationEntry);

        this.citations.push(citationEntry);
        return id;
    }

    /**
     * Calculate credibility score for a citation
     * @param {Object} citation - Citation object
     * @returns {number} - Credibility score (0-100)
     */
    calculateCredibilityScore(citation) {
        let score = 0;

        // Check if URL is from authoritative domain
        if (citation.url) {
            const authoritativeDomains = [
                '.edu', '.gov', '.org',
                'nature.com', 'science.org', 'ieee.org',
                'arxiv.org', 'scholar.google'
            ];

            const isAuthoritative = authoritativeDomains.some(domain =>
                citation.url.includes(domain)
            );

            if (isAuthoritative) {
                score += 40;
            } else {
                score += 10;
            }
        }

        // Check if author is provided
        if (citation.author && citation.author.length > 0) {
            score += 20;
        }

        // Check if date is recent (within 5 years)
        if (citation.date) {
            const citationYear = new Date(citation.date).getFullYear();
            const currentYear = new Date().getFullYear();
            if (currentYear - citationYear <= 5) {
                score += 20;
            } else if (currentYear - citationYear <= 10) {
                score += 10;
            }
        }

        // Check if publisher is provided
        if (citation.publisher && citation.publisher.length > 0) {
            score += 10;
        }

        // Check if title is descriptive (> 10 characters)
        if (citation.title && citation.title.length > 10) {
            score += 10;
        }

        return Math.min(score, 100);
    }

    /**
     * Format citation in specified format
     * @param {number} id - Citation ID
     * @param {string} format - Citation format (APA, MLA, etc.)
     * @returns {string} - Formatted citation
     */
    formatCitation(id, format = 'APA') {
        const citation = this.citations.find(c => c.id === id);
        if (!citation) {
            return '';
        }

        switch (format.toUpperCase()) {
            case 'APA':
                return this.formatAPA(citation);
            case 'MLA':
                return this.formatMLA(citation);
            case 'CHICAGO':
                return this.formatChicago(citation);
            case 'IEEE':
                return this.formatIEEE(citation);
            default:
                return this.formatAPA(citation);
        }
    }

    /**
     * Format citation in APA style
     * @param {Object} citation - Citation object
     * @returns {string} - APA formatted citation
     */
    formatAPA(citation) {
        const year = citation.date ? new Date(citation.date).getFullYear() : 'n.d.';
        let formatted = '';

        if (citation.author) {
            formatted += `${citation.author}. `;
        }
        formatted += `(${year}). `;
        if (citation.title) {
            formatted += `${citation.title}. `;
        }
        if (citation.publisher) {
            formatted += `${citation.publisher}. `;
        }
        if (citation.url) {
            formatted += `Retrieved from ${citation.url}`;
        }

        return formatted;
    }

    /**
     * Format citation in MLA style
     * @param {Object} citation - Citation object
     * @returns {string} - MLA formatted citation
     */
    formatMLA(citation) {
        let formatted = '';

        if (citation.author) {
            formatted += `${citation.author}. `;
        }
        if (citation.title) {
            formatted += `"${citation.title}." `;
        }
        if (citation.publisher) {
            formatted += `${citation.publisher}, `;
        }
        if (citation.date) {
            formatted += `${citation.date}. `;
        }
        if (citation.url) {
            formatted += `${citation.url}. `;
        }
        formatted += `Accessed ${citation.accessed}.`;

        return formatted;
    }

    /**
     * Format citation in Chicago style
     * @param {Object} citation - Citation object
     * @returns {string} - Chicago formatted citation
     */
    formatChicago(citation) {
        let formatted = '';

        if (citation.author) {
            formatted += `${citation.author}. `;
        }
        if (citation.title) {
            formatted += `"${citation.title}." `;
        }
        if (citation.publisher) {
            formatted += `${citation.publisher}. `;
        }
        if (citation.date) {
            const date = new Date(citation.date);
            formatted += `${date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}. `;
        }
        if (citation.url) {
            formatted += `${citation.url}.`;
        }

        return formatted;
    }

    /**
     * Format citation in IEEE style
     * @param {Object} citation - Citation object
     * @returns {string} - IEEE formatted citation
     */
    formatIEEE(citation) {
        let formatted = `[${citation.id}] `;

        if (citation.author) {
            formatted += `${citation.author}, `;
        }
        if (citation.title) {
            formatted += `"${citation.title}," `;
        }
        if (citation.publisher) {
            formatted += `${citation.publisher}, `;
        }
        if (citation.date) {
            formatted += `${new Date(citation.date).getFullYear()}. `;
        }
        if (citation.url) {
            formatted += `[Online]. Available: ${citation.url}`;
        }

        return formatted;
    }

    /**
     * Validate URL accessibility
     * @param {string} url - URL to validate
     * @returns {Promise<Object>} - Validation result
     */
    async validateURL(url) {
        try {
            // Note: This is a client-side check, full validation would require backend
            const urlPattern = /^https?:\/\/.+/i;
            if (!urlPattern.test(url)) {
                return {
                    valid: false,
                    reason: 'Invalid URL format'
                };
            }

            return {
                valid: true,
                url: url
            };
        } catch (error) {
            return {
                valid: false,
                reason: error.message
            };
        }
    }

    /**
     * Get all citations
     * @returns {Array} - All citations
     */
    getAllCitations() {
        return this.citations;
    }

    /**
     * Get citation by ID
     * @param {number} id - Citation ID
     * @returns {Object|null} - Citation object or null
     */
    getCitationById(id) {
        return this.citations.find(c => c.id === id) || null;
    }

    /**
     * Remove citation by ID
     * @param {number} id - Citation ID
     * @returns {boolean} - Success status
     */
    removeCitation(id) {
        const index = this.citations.findIndex(c => c.id === id);
        if (index !== -1) {
            this.citations.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Generate bibliography in specified format
     * @param {string} format - Citation format
     * @returns {string} - Formatted bibliography
     */
    generateBibliography(format = 'APA') {
        let bibliography = '# Bibliography\n\n';

        this.citations
            .sort((a, b) => (a.author || '').localeCompare(b.author || ''))
            .forEach(citation => {
                bibliography += `${this.formatCitation(citation.id, format)}\n\n`;
            });

        return bibliography;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CitationManager;
}
