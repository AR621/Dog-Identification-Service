document.addEventListener('DOMContentLoaded', function() {
    // Get references to the form and the file input
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
            
            // Submit the form using AJAX
            submitForm();
        }
    }

    // Function to submit form using AJAX
    function submitForm() {
        const formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => {
            // Handle response as needed
            console.log(response);

            // form.setAttribute('data-submitted', 'true');
            // Submit the form after fetch request completes
            form.submit(); 
        })
        .catch(error => {
            // Handle error as needed
            console.error('Error:', error);
        });
    }

    // Add event listeners for drag and drop
    const fileDroppable = document.getElementById('fileDroppable');
    fileDroppable.addEventListener('dragover', (event) => {
        event.preventDefault();
    });
    fileDroppable.addEventListener('drop', handleFileDrop);
    
    // Automatically submit the form when a file is dropped
    // fileInput.addEventListener('change', submitForm);
});