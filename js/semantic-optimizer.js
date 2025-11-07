/**
 * Semantic Optimizer Module
 * Optimizes content structure and semantic markup for GEO
 */

class SemanticOptimizer {
    constructor() {
        this.schemaTypes = {
            ARTICLE: 'Article',
            BLOG_POSTING: 'BlogPosting',
            FAQ: 'FAQPage',
            HOW_TO: 'HowTo',
            PRODUCT: 'Product',
            ORGANIZATION: 'Organization',
            PERSON: 'Person'
        };
    }

    /**
     * Generate Schema.org JSON-LD markup
     * @param {string} type - Schema type
     * @param {Object} data - Content data
     * @returns {Object} - JSON-LD object
     */
    generateSchema(type, data) {
        const baseSchema = {
            '@context': 'https://schema.org',
            '@type': type
        };

        switch (type) {
            case this.schemaTypes.ARTICLE:
                return this.generateArticleSchema(data);
            case this.schemaTypes.FAQ:
                return this.generateFAQSchema(data);
            case this.schemaTypes.HOW_TO:
                return this.generateHowToSchema(data);
            case this.schemaTypes.PRODUCT:
                return this.generateProductSchema(data);
            default:
                return baseSchema;
        }
    }

    /**
     * Generate Article schema
     * @param {Object} data - Article data
     * @returns {Object} - Article JSON-LD
     */
    generateArticleSchema(data) {
        return {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': data.title || '',
            'description': data.description || '',
            'author': {
                '@type': 'Person',
                'name': data.author || 'Anonymous'
            },
            'datePublished': data.datePublished || new Date().toISOString(),
            'dateModified': data.dateModified || new Date().toISOString(),
            'publisher': {
                '@type': 'Organization',
                'name': data.publisher || '',
                'logo': {
                    '@type': 'ImageObject',
                    'url': data.logo || ''
                }
            },
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': data.url || ''
            }
        };
    }

    /**
     * Generate FAQ schema
     * @param {Object} data - FAQ data
     * @returns {Object} - FAQ JSON-LD
     */
    generateFAQSchema(data) {
        const schema = {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': []
        };

        if (data.questions && Array.isArray(data.questions)) {
            schema.mainEntity = data.questions.map(qa => ({
                '@type': 'Question',
                'name': qa.question,
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': qa.answer
                }
            }));
        }

        return schema;
    }

    /**
     * Generate HowTo schema
     * @param {Object} data - HowTo data
     * @returns {Object} - HowTo JSON-LD
     */
    generateHowToSchema(data) {
        const schema = {
            '@context': 'https://schema.org',
            '@type': 'HowTo',
            'name': data.name || '',
            'description': data.description || '',
            'step': []
        };

        if (data.steps && Array.isArray(data.steps)) {
            schema.step = data.steps.map((step, index) => ({
                '@type': 'HowToStep',
                'position': index + 1,
                'name': step.name || `Step ${index + 1}`,
                'text': step.text || '',
                'url': step.url || ''
            }));
        }

        return schema;
    }

    /**
     * Generate Product schema
     * @param {Object} data - Product data
     * @returns {Object} - Product JSON-LD
     */
    generateProductSchema(data) {
        return {
            '@context': 'https://schema.org',
            '@type': 'Product',
            'name': data.name || '',
            'description': data.description || '',
            'image': data.image || '',
            'brand': {
                '@type': 'Brand',
                'name': data.brand || ''
            },
            'offers': {
                '@type': 'Offer',
                'price': data.price || '0',
                'priceCurrency': data.currency || 'USD',
                'availability': 'https://schema.org/InStock'
            }
        };
    }

    /**
     * Analyze HTML structure for semantic quality
     * @param {string} html - HTML content
     * @returns {Object} - Structure analysis
     */
    analyzeStructure(html) {
        const analysis = {
            score: 0,
            maxScore: 100,
            elements: {
                semantic: [],
                nonSemantic: [],
                missing: []
            },
            suggestions: []
        };

        // Check for semantic HTML5 elements
        const semanticElements = [
            'header', 'nav', 'main', 'article', 'section',
            'aside', 'footer', 'figure', 'figcaption'
        ];

        semanticElements.forEach(element => {
            const regex = new RegExp(`<${element}[^>]*>`, 'gi');
            if (regex.test(html)) {
                analysis.elements.semantic.push(element);
                analysis.score += 5;
            } else {
                analysis.elements.missing.push(element);
            }
        });

        // Check for non-semantic elements that should be replaced
        const nonSemanticPatterns = [
            { pattern: /<div[^>]*class="header"[^>]*>/gi, suggestion: 'Use <header> instead of <div class="header">' },
            { pattern: /<div[^>]*class="nav"[^>]*>/gi, suggestion: 'Use <nav> instead of <div class="nav">' },
            { pattern: /<div[^>]*class="footer"[^>]*>/gi, suggestion: 'Use <footer> instead of <div class="footer">' }
        ];

        nonSemanticPatterns.forEach(({ pattern, suggestion }) => {
            if (pattern.test(html)) {
                analysis.suggestions.push(suggestion);
                analysis.score -= 5;
            }
        });

        // Check heading hierarchy
        const headingAnalysis = this.analyzeHeadingHierarchy(html);
        analysis.headings = headingAnalysis;
        if (headingAnalysis.proper) {
            analysis.score += 20;
        } else {
            analysis.suggestions.push('Fix heading hierarchy - should be sequential (H1 -> H2 -> H3)');
        }

        // Check for ARIA labels
        const hasAriaLabels = /aria-label|aria-labelledby|role=/gi.test(html);
        if (hasAriaLabels) {
            analysis.score += 10;
        } else {
            analysis.suggestions.push('Add ARIA labels for better accessibility');
        }

        // Normalize score
        analysis.score = Math.max(0, Math.min(100, analysis.score));
        analysis.percentage = analysis.score;

        return analysis;
    }

    /**
     * Analyze heading hierarchy
     * @param {string} html - HTML content
     * @returns {Object} - Heading analysis
     */
    analyzeHeadingHierarchy(html) {
        const headingRegex = /<h([1-6])[^>]*>(.*?)<\/h\1>/gi;
        const headings = [];
        let match;

        while ((match = headingRegex.exec(html)) !== null) {
            headings.push({
                level: parseInt(match[1]),
                text: match[2].replace(/<[^>]*>/g, '')
            });
        }

        const analysis = {
            headings,
            proper: true,
            issues: []
        };

        // Check for H1
        if (!headings.some(h => h.level === 1)) {
            analysis.proper = false;
            analysis.issues.push('Missing H1 heading');
        }

        // Check for multiple H1s
        if (headings.filter(h => h.level === 1).length > 1) {
            analysis.proper = false;
            analysis.issues.push('Multiple H1 headings found (should have only one)');
        }

        // Check sequential hierarchy
        for (let i = 1; i < headings.length; i++) {
            const levelDiff = headings[i].level - headings[i - 1].level;
            if (levelDiff > 1) {
                analysis.proper = false;
                analysis.issues.push(`Heading hierarchy skip: H${headings[i - 1].level} to H${headings[i].level}`);
            }
        }

        return analysis;
    }

    /**
     * Generate semantic HTML from plain text
     * @param {string} text - Plain text content
     * @returns {string} - Semantic HTML
     */
    convertToSemanticHTML(text) {
        let html = '';

        // Split into paragraphs
        const paragraphs = text.split('\n\n');

        paragraphs.forEach(para => {
            para = para.trim();
            if (!para) return;

            // Check if it's a heading (lines ending with : or all caps)
            if (para.endsWith(':') || para === para.toUpperCase()) {
                html += `<h2>${para}</h2>\n`;
            }
            // Check if it's a list item
            else if (para.startsWith('-') || para.startsWith('•') || para.startsWith('*')) {
                const items = para.split('\n').filter(line => line.trim());
                html += '<ul>\n';
                items.forEach(item => {
                    const cleanItem = item.replace(/^[-•*]\s*/, '');
                    html += `  <li>${cleanItem}</li>\n`;
                });
                html += '</ul>\n';
            }
            // Regular paragraph
            else {
                html += `<p>${para}</p>\n`;
            }
        });

        return html;
    }

    /**
     * Optimize meta tags for GEO
     * @param {Object} data - Page data
     * @returns {Object} - Optimized meta tags
     */
    generateMetaTags(data) {
        const metaTags = {};

        // Basic meta tags
        metaTags.title = this.optimizeTitle(data.title || '');
        metaTags.description = this.optimizeDescription(data.description || '');

        // Open Graph tags
        metaTags.og = {
            'og:title': metaTags.title,
            'og:description': metaTags.description,
            'og:type': data.type || 'website',
            'og:url': data.url || '',
            'og:image': data.image || ''
        };

        // Twitter Card tags
        metaTags.twitter = {
            'twitter:card': 'summary_large_image',
            'twitter:title': metaTags.title,
            'twitter:description': metaTags.description,
            'twitter:image': data.image || ''
        };

        return metaTags;
    }

    /**
     * Optimize title for GEO
     * @param {string} title - Original title
     * @returns {string} - Optimized title
     */
    optimizeTitle(title) {
        // Ensure title is 50-60 characters
        if (title.length > 60) {
            title = title.substring(0, 57) + '...';
        }
        return title;
    }

    /**
     * Optimize description for GEO
     * @param {string} description - Original description
     * @returns {string} - Optimized description
     */
    optimizeDescription(description) {
        // Ensure description is 150-160 characters
        if (description.length > 160) {
            description = description.substring(0, 157) + '...';
        } else if (description.length < 120) {
            // Description might be too short
            console.warn('Description is shorter than recommended (120-160 characters)');
        }
        return description;
    }

    /**
     * Extract entities from content (basic NLP)
     * @param {string} content - Content text
     * @returns {Object} - Extracted entities
     */
    extractEntities(content) {
        const entities = {
            people: [],
            organizations: [],
            locations: [],
            dates: [],
            numbers: []
        };

        // Extract dates
        const datePattern = /\b\d{1,2}\/\d{1,2}\/\d{2,4}\b|\b\d{4}\b/g;
        entities.dates = [...new Set(content.match(datePattern) || [])];

        // Extract percentages and numbers
        const numberPattern = /\b\d+\.?\d*%?\b/g;
        entities.numbers = [...new Set(content.match(numberPattern) || [])];

        // Extract capitalized words (potential proper nouns)
        const capitalizedPattern = /\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g;
        const capitalized = content.match(capitalizedPattern) || [];
        entities.people = [...new Set(capitalized.filter(word =>
            !['The', 'A', 'An', 'This', 'That'].includes(word)
        ))];

        return entities;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SemanticOptimizer;
}
