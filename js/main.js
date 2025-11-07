/**
 * Main Application Logic
 * Coordinates between different modules and handles UI interactions
 */

// Initialize modules
const geoAnalyzer = new GEOAnalyzer();
const citationManager = new CitationManager();
const semanticOptimizer = new SemanticOptimizer();

// Application state
const appState = {
    currentAnalysis: null,
    selectedPrinciple: null
};

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('GEO Principles Application Initialized');

    // Set up event listeners
    setupEventListeners();

    // Load example content if needed
    loadExampleContent();
});

/**
 * Set up event listeners for interactive elements
 */
function setupEventListeners() {
    // Analyzer form submission
    const analyzeButton = document.querySelector('.btn-analyze');
    if (analyzeButton) {
        analyzeButton.addEventListener('click', analyzeContent);
    }

    // Content input auto-save
    const contentInput = document.getElementById('content-input');
    if (contentInput) {
        contentInput.addEventListener('input', debounce(saveContentDraft, 1000));
    }
}

/**
 * Analyze content based on user input
 */
async function analyzeContent() {
    const contentInput = document.getElementById('content-input');
    const content = contentInput.value.trim();

    if (!content) {
        alert('Please enter some content to analyze');
        return;
    }

    // Get analysis options
    const options = {
        checkSemantic: document.getElementById('check-semantic').checked,
        checkCitations: document.getElementById('check-citations').checked,
        checkReadability: document.getElementById('check-readability').checked,
        checkKeywords: document.getElementById('check-keywords').checked
    };

    // Show loading state
    const resultsDiv = document.getElementById('analysis-results');
    const resultsContent = document.getElementById('results-content');
    resultsDiv.style.display = 'block';
    resultsContent.innerHTML = '<p>Analyzing content... Please wait.</p>';

    try {
        // Perform analysis
        const results = await geoAnalyzer.analyzeContent(content, options);
        appState.currentAnalysis = results;

        // Display results
        displayAnalysisResults(results);
    } catch (error) {
        console.error('Analysis error:', error);
        resultsContent.innerHTML = `<p style="color: var(--danger-color);">Error analyzing content: ${error.message}</p>`;
    }
}

/**
 * Display analysis results in the UI
 * @param {Object} results - Analysis results
 */
function displayAnalysisResults(results) {
    const resultsContent = document.getElementById('results-content');

    let html = `
        <div class="analysis-summary">
            <h4>Overall Score: ${results.percentage}%</h4>
            <div class="score-bar">
                <div class="score-fill" style="width: ${results.percentage}%; background-color: ${getScoreColor(results.percentage)}"></div>
            </div>
        </div>

        <div class="analysis-details">
    `;

    // Display each check result
    results.checks.forEach(check => {
        const checkPercentage = Math.round((check.score / check.maxScore) * 100);

        html += `
            <div class="check-result">
                <h5>${check.name} - ${checkPercentage}%</h5>

                ${check.passed.length > 0 ? `
                    <div class="passed-checks">
                        <strong style="color: var(--success-color);">✓ Passed:</strong>
                        <ul>
                            ${check.passed.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${check.failed.length > 0 ? `
                    <div class="failed-checks">
                        <strong style="color: var(--danger-color);">✗ Needs Improvement:</strong>
                        <ul>
                            ${check.failed.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    });

    html += '</div>';

    // Display recommendations
    if (results.recommendations.length > 0) {
        html += `
            <div class="recommendations">
                <h4>Recommendations</h4>
        `;

        results.recommendations.forEach(rec => {
            const priorityColor = rec.priority === 'high' ? 'var(--danger-color)' : 'var(--warning-color)';
            html += `
                <div class="recommendation-item">
                    <h5 style="color: ${priorityColor}">
                        ${rec.category}
                        <span class="priority-badge" style="background-color: ${priorityColor}">
                            ${rec.priority.toUpperCase()}
                        </span>
                    </h5>
                    <ul>
                        ${rec.suggestions.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>
            `;
        });

        html += '</div>';
    }

    resultsContent.innerHTML = html;
}

/**
 * Get color based on score
 * @param {number} score - Score percentage
 * @returns {string} - CSS color
 */
function getScoreColor(score) {
    if (score >= 80) return 'var(--success-color)';
    if (score >= 60) return 'var(--warning-color)';
    return 'var(--danger-color)';
}

/**
 * Show detailed information about a principle
 * @param {string} principle - Principle identifier
 */
function showPrincipleDetails(principle) {
    // This would open a modal or expand section with detailed information
    console.log(`Showing details for principle: ${principle}`);
    appState.selectedPrinciple = principle;

    // For now, just alert - could be enhanced with a modal
    const principleInfo = {
        semantic: 'Semantic structure uses HTML5 elements to convey meaning and hierarchy, making it easier for AI to understand your content.',
        citations: 'Authoritative citations establish credibility and help AI verify information accuracy.',
        quality: 'High-quality content provides comprehensive, accurate information that answers user queries effectively.',
        nlp: 'Natural language optimization ensures your content aligns with how people ask questions.',
        multimodal: 'Multi-modal content includes properly described images, videos, and other media.',
        hierarchy: 'Information hierarchy presents the most important information first with clear organization.',
        context: 'Contextual relevance ensures content matches user intent and provides necessary background.',
        technical: 'Technical SEO makes your content easily accessible and understandable to AI crawlers.'
    };

    alert(principleInfo[principle] || 'Information not available');
}

/**
 * Scroll to analyzer section
 */
function scrollToAnalyzer() {
    const analyzerSection = document.getElementById('analyzer');
    if (analyzerSection) {
        analyzerSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Scroll to principles section
 */
function scrollToPrinciples() {
    const principlesSection = document.getElementById('principles');
    if (principlesSection) {
        principlesSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Save content draft to localStorage
 */
function saveContentDraft() {
    const contentInput = document.getElementById('content-input');
    if (contentInput) {
        localStorage.setItem('geo-content-draft', contentInput.value);
        console.log('Draft saved');
    }
}

/**
 * Load example content for demonstration
 */
function loadExampleContent() {
    const contentInput = document.getElementById('content-input');

    // Check if there's a saved draft
    const savedDraft = localStorage.getItem('geo-content-draft');
    if (savedDraft && contentInput && !contentInput.value) {
        contentInput.value = savedDraft;
    }
}

/**
 * Debounce function for performance optimization
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Export analysis results as JSON
 */
function exportResults() {
    if (!appState.currentAnalysis) {
        alert('No analysis results to export');
        return;
    }

    const dataStr = JSON.stringify(appState.currentAnalysis, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'geo-analysis-results.json';
    link.click();

    URL.revokeObjectURL(url);
}

/**
 * Generate Schema.org markup from current content
 */
function generateSchemaMarkup() {
    const contentInput = document.getElementById('content-input');
    const content = contentInput.value.trim();

    if (!content) {
        alert('Please enter content first');
        return;
    }

    // Extract basic information
    const lines = content.split('\n');
    const title = lines[0] || 'Untitled';
    const description = lines.slice(1, 3).join(' ') || '';

    const schema = semanticOptimizer.generateSchema('Article', {
        title,
        description,
        author: 'Author Name',
        datePublished: new Date().toISOString(),
        url: window.location.href
    });

    // Display schema in alert (could be enhanced with modal)
    alert('Generated Schema.org markup:\n\n' + JSON.stringify(schema, null, 2));
}

/**
 * Add citation to content
 */
function addCitation() {
    const citation = {
        title: prompt('Citation title:'),
        author: prompt('Author:'),
        url: prompt('URL:'),
        date: prompt('Publication date (YYYY-MM-DD):')
    };

    if (citation.title) {
        const id = citationManager.addCitation(citation);
        const formatted = citationManager.formatCitation(id, 'APA');

        // Append citation to content
        const contentInput = document.getElementById('content-input');
        if (contentInput) {
            contentInput.value += `\n\n${formatted}`;
        }

        alert('Citation added successfully!');
    }
}

// Add CSS for analysis results
const style = document.createElement('style');
style.textContent = `
    .score-bar {
        width: 100%;
        height: 20px;
        background-color: var(--bg-light);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }

    .score-fill {
        height: 100%;
        transition: width 0.3s ease;
    }

    .analysis-details {
        margin-top: 2rem;
    }

    .check-result {
        background-color: var(--bg-light);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    .check-result h5 {
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }

    .passed-checks, .failed-checks {
        margin: 0.5rem 0;
    }

    .passed-checks ul, .failed-checks ul {
        margin-left: 1.5rem;
        margin-top: 0.5rem;
    }

    .recommendations {
        margin-top: 2rem;
        padding: 1rem;
        background-color: var(--bg-light);
        border-radius: 0.5rem;
    }

    .recommendation-item {
        margin-bottom: 1rem;
        padding: 1rem;
        background-color: var(--bg-white);
        border-radius: 0.5rem;
    }

    .priority-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        color: white;
        margin-left: 0.5rem;
    }
`;
document.head.appendChild(style);

console.log('Main.js loaded successfully');
