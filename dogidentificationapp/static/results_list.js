function toggleResults() {
    var resultsContainer = document.getElementById('results-container');
    var resultsToggle = document.querySelector('.results-toggle');
    
    // Toggle the visibility of the results container
    resultsContainer.classList.toggle('hidden');
    
    // Toggle the appearance of the results toggle button
    if (resultsContainer.classList.contains('hidden')) {
        resultsContainer.style.right = '-20em';
        resultsToggle.innerHTML = '&#x25C4;';
        
        // Prevent horizontal scrolling when the results list is hidden
        document.body.style.overflowX = 'hidden';
    } else {
        resultsContainer.style.right = '0';
        resultsToggle.innerHTML = '&#x25BA;';
        
        // Allow horizontal scrolling when the results list is visible
        document.body.style.overflowX = '';
    }
}
