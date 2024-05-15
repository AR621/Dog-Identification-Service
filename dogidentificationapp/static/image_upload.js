//  for handling the image upload via drag and drop

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.querySelector('input[type="file"]');
    
    // Function to handle file drop event
    function handleFileDrop(event) {
        event.preventDefault();
        const files = event.dataTransfer.files;

        // If there are files dropped
        console.log(files)
        if (files.length > 0) {
            // Assign the dropped file to the file input
            fileInput.files = files;
            form.submit();
        }
    }

    // code for handling the image upload via browse button
    var imageInput = document.querySelector('#id_image_input');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            var uploadForm = document.getElementById('uploadForm');
            if (uploadForm) {
                uploadForm.submit();
            } else {
                console.error("Form with id 'uploadForm' not found.");
            }
        });
    } else {
        console.error("Element with id 'id_image_input' not found.");
    }

    // Function to submit form using AJAX
    function submitForm() {
        const formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => {
            console.log(response);
            // // Submit the form after fetch request completes
            form.submit(); 
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Add event listeners for drag and drop
    const fileDroppable = document.getElementById('fileDroppable');
    fileDroppable.addEventListener('dragover', (event) => {
        event.preventDefault();
    });
    fileDroppable.addEventListener('drop', handleFileDrop);
});