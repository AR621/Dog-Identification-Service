function submitFeedback(isCorrect) {
    if (isCorrect) {
        sendFeedback(isCorrect, null);
    } else {
        var correctBreedForm = document.getElementById('correct-breed-form');
        correctBreedForm.style.display = 'block';
    }
}

function submitCorrectBreed() {
    var correctBreedInput = document.getElementById('correct-breed-input');
    var correctBreed = correctBreedInput.value;
    if (correctBreed) {
        sendFeedback(false, correctBreed);
    } else {
        alert('Please enter the correct breed.');
    }
}

function sendFeedback(isCorrect, correctBreed) {
    var save_feedback = false;
    // First check if the form is about already saved photo or not
    if (photoId === "None") {
        save_feedback = askForConfirmation();
    } else
        save_feedback = true;
    // Then save the photo or do nothing if user does nota agree to using his data
    if (save_feedback) {
        var xml_http_req = new XMLHttpRequest();
        xml_http_req.open('POST', '/submit_feedback/', true);
        xml_http_req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xml_http_req.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        var data = JSON.stringify({ 'is_correct': isCorrect, 'correct_breed': correctBreed });
        xml_http_req.send(data);
    }
    var feedbackForm = document.getElementById('feedback-container');
    // assign feedback_subbmitted to true

    feedbackForm.style.display = 'none';
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    // JavaScript function to display confirmation popup
    function askForConfirmation() {
        if (confirm("Would you like for your data to be saved for potential improvment of the model?")) {
            alert("Data saved, thank you!")
            return true
        } else {
            // Send a request to the server to update the session variable
            var xml_http_req = new XMLHttpRequest();
            xml_http_req.open('POST', '/refuse_saving_of_data/', true);  // Specify the URL to update the session variable
            xml_http_req.setRequestHeader('Content-Type', 'application/json');
            xml_http_req.onreadystatechange = function () {
                if (xml_http_req.readyState === XMLHttpRequest.DONE) {
                    if (xml_http_req.status === 200) {
                        console.log("feedback_submitted session variable updated successfully");
                    } else {
                        // Error handling
                        console.error("Error updating session variable");
                    }
                }
            };
            // Send the request with the data you want to update the session variable with
            xml_http_req.send(JSON.stringify({key: 'feedback_submitted', value: true}));

            return false;
        }
    }