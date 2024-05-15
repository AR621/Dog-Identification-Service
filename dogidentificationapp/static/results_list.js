function toggleResults() {

    var resultsContainer = document.getElementById('results-container');
    var resultsToggle = document.querySelector('.results-toggle');
    resultsContainer.classList.toggle('hidden');
    if (resultsContainer.classList.contains('hidden')) {
        resultsContainer.style.right = '-20em';
        resultsToggle.innerHTML = '&#x25C4;';
    } else {
        resultsContainer.style.right = '0';
        resultsToggle.innerHTML = '&#x25BA;';
    }
}