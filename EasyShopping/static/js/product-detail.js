// Define the URL of the API
const url = 'http://127.0.0.1:8000/api/cart-item/';

// Define the function to retrieve a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Retrieve CSRF token from cookies
const csrfToken = getCookie('csrftoken');

// Function to make a POST request
async function postData(url = '', data = {}) {
    try {
        // Make the POST request
        const response = await fetch(url, {
            method: 'POST', // Specify the HTTP method
            headers: {
                'Content-Type': 'application/json', // Set the request headers
                'X-CSRFToken': csrfToken, // CSRF token in the header
            },
            body: JSON.stringify(data) // Convert data to JSON string
        });

        // Check if the response is ok (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Your work has been saved",
                showConfirmButton: false,
                timer: 1500
              });
        }
        // Parse the JSON response
        const responseData = await response.json();
        console.log('Response:', responseData);
        return responseData;
    } catch (error) {
        // Handle any errors that occur
        console.error('Error:', error);
    }
}

// Add event listener to the button
document.getElementById("addToCart").addEventListener('click', () => {
    console.log("click");

    // Get the form data and convert it to a plain object
    const formData = new FormData(document.getElementById('productForm'));
    const productData = Object.fromEntries(formData.entries());

    console.log(productData);
    // Call the function with the URL and data
    postData(url, productData);
});

// Select the elements
const minusButton = document.getElementById('button-addon1');
const plusButton = document.getElementById('button-addon2');
const quantityInput = document.getElementById('quantityInput');

// Event listener for the minus button
minusButton.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value) || 1;
    if (quantity > 1) {  // Ensure quantity does not go below 1
        quantityInput.value = quantity - 1;
    }
});

// Event listener for the plus button
plusButton.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value) || 1;
    quantityInput.value = quantity + 1;
});






// Add event listener to the "Buy Now" button
document.getElementById("buyNow").addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default behavior (i.e., following the link)

    // Get the form elements
    const form = document.getElementById('productForm');
    const productID = form.querySelector('input[name="productID"]').value;
    const sizeID = form.querySelector('select[name="size"]').value;
    const quantity = form.querySelector('input[name="quantity"]').value;

    // Get the base checkout URL from the hidden input field
    const checkoutURL = document.getElementById('checkoutURL').value;

    // Construct the URL with query parameters
    const fullURL = `${checkoutURL}?pid=${productID}&sid=${sizeID}&quantity=${quantity}`;

    // Redirect to the checkout page
    window.location.href = fullURL;
});

