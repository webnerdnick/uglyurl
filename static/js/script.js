/**
 * UglyURL - Client-side JavaScript
 * Handles interactive features like copy button and ugliness slider
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ugliness slider update
    const uglinessSlider = document.getElementById('ugliness');
    const uglinessValue = document.getElementById('ugliness-value');

    if (uglinessSlider && uglinessValue) {
        uglinessSlider.addEventListener('input', function() {
            uglinessValue.textContent = this.value;
        });
    }

    // Copy to clipboard functionality
    const copyBtn = document.getElementById('copy-btn');
    const uglyUrlElement = document.getElementById('ugly-url');

    if (copyBtn && uglyUrlElement) {
        copyBtn.addEventListener('click', function() {
            const uglyUrl = uglyUrlElement.textContent;

            // Modern clipboard API
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(uglyUrl).then(function() {
                    showCopySuccess();
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                    fallbackCopy(uglyUrl);
                });
            } else {
                // Fallback for older browsers
                fallbackCopy(uglyUrl);
            }
        });
    }

    /**
     * Show success feedback when URL is copied
     */
    function showCopySuccess() {
        const copyBtn = document.getElementById('copy-btn');
        const originalText = copyBtn.textContent;

        copyBtn.textContent = 'Copied!';
        copyBtn.classList.add('copied');

        setTimeout(function() {
            copyBtn.textContent = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
    }

    /**
     * Fallback copy method for older browsers
     */
    function fallbackCopy(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showCopySuccess();
            } else {
                console.error('Fallback copy failed');
            }
        } catch (err) {
            console.error('Fallback copy error:', err);
        }

        document.body.removeChild(textArea);
    }
});
