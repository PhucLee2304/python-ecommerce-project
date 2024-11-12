$(':radio').change(function() {
    console.log('New star rating: ' + this.value);
  });



    document.getElementById('submit').addEventListener('click', function () {
        // Collect data from the rating form
        const ratingForm = document.querySelector('.rating');
        const selectedRating = ratingForm.querySelector('input[name="stars"]:checked');
        const rating = selectedRating ? selectedRating.value : null;

        // Collect data from the comment form
        const comment = document.querySelector('textarea[name="comment"]').value;
        const product_id = document.getElementById('product_id').value;
        // Prepare data for POST request
        const formData = {
            rating: rating,
            comment: comment,
            product_id: product_id
        };
        console.log(formData);

        // Send data to the API
        fetch('http://127.0.0.1:8000/api/submit-feedback/', { // Replace with your Django API endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Ensure you send CSRF token
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Feedback submitted successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to submit feedback.');
        });
    });

    // Function to get CSRF token from the cookie
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name + '='));
        return cookieValue ? cookieValue.split('=')[1] : null;
    }

