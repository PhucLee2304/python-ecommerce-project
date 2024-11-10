document.addEventListener('click', (event) => {
    if (event.target.matches('.remove-item-btn')) {
        const cartItemId = event.target.dataset.cartitemId;
        console.log(cartItemId);
        removeCartItem(cartItemId);
    }
});
document.addEventListener('DOMContentLoaded', () => {
    // Handle size change event
    document.querySelectorAll('.size').forEach(select => {
        select.addEventListener('change', (event) => {
            const sizeID = event.target.value;
            const cartItemID = event.target.dataset.cartitemId;
            
            // Update the cart item size via AJAX
            updateCartItemSize(cartItemID, sizeID);
        });
    });

    // Handle quantity change events (increase and decrease)
    document.querySelectorAll('.btn-plus, .btn-minus').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const cartItemID = event.target.closest('button').dataset.cartitemId;

            const action = event.target.closest('button').dataset.action;

            let quantityInput = document.querySelector(`input[data-cartitem-id="${cartItemID}"]`);
            let currentQuantity = parseInt(quantityInput.value);

            // Handle increase and decrease actions
            if (action === 'increase') {
                // currentQuantity++;
            } else if (action === 'decrease' && currentQuantity > 1) {
                // currentQuantity--;
            }
            else{
                currentQuantity = 1;
            }

            quantityInput.value = currentQuantity;
            console.log(cartItemID);

            // Update the cart item quantity on the server (via AJAX)
            updateCartItemQuantity(cartItemID, currentQuantity);
        });
    });

 

    // document.addEventListener('click', (event) => {
    //     if (event.target.matches('.remove-item-btn')) {
    //         const cartItemId = event.target.dataset.cartitemId;
    //         console.log('Cart item ID:', cartItemId);
    //         removeCartItem(cartItemId);
    //     }
    // });
    

    // Handle remove item event
    // document.querySelectorAll('.remove-item-btn').forEach(button => {
    //     button.addEventListener('click', (event) => {
    //         // const cartItemID = event.target.dataset.cartitemId;

    //         console.log("remove");
    //     });
    // });

    // Handle form submission to update all cart items
    // document.querySelector('form').addEventListener('submit', function(event) {
    //     event.preventDefault();  // Prevent form from submitting the traditional way
        
    //     const formData = new FormData(this);
    //     const cartItems = [...document.querySelectorAll('tr[data-cartitem-id]')];
        
    //     const updatedCartItems = cartItems.map(cartItem => {
    //         const cartItemID = cartItem.dataset.cartitemId;
    //         const size = formData.get(`size[${cartItemID}]`);
    //         const quantity = formData.get(`quantity[${cartItemID}]`);
    //         return { cartItemID, size, quantity };
    //     });
        
    //     // Send data to update cart (via AJAX)
    //     updateCart(updatedCartItems);
    // });
});

// Function to update the cart item size
function updateCartItemSize(cartItemID, sizeID) {
    fetch('http://127.0.0.1:8000/update-cart-item-size/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({ cartItemID, sizeID })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart item size updated:', data);
    })
    .catch(error => {
        console.error('Error updating cart item size:', error);
    });
}

// Function to update the cart item quantity
function updateCartItemQuantity(cartItemID, quantity) {
    fetch('http://127.0.0.1:8000/update-cart-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({ cartItemID, quantity })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart item quantity updated:', data);
        document.getElementById('totalAmount').innerText = `${data.newTotal} $`;
        // window.location.href = 'http://127.0.0.1:8000/cart/';
    })
    .catch(error => {
        console.error('Error updating cart item quantity:', error);
    });
}

// Function to remove an item from the cart
function removeCartItem(cartItemID) {
    
    fetch('http://127.0.0.1:8000/remove-cart-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({ cartItemID })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart item removed:', data);
        // Optionally, remove the item from the DOM
        document.querySelector(`tr[data-cartitem-id="${cartItemID}"]`).remove();
    })
    .catch(error => {
        console.error('Error removing cart item:', error);
    });
    return redirect('cart.html')
}

// Function to update the entire cart (on form submit)
function updateCart(updatedCartItems) {
    fetch('http://127.0.0.1:8000/update-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({ updatedCartItems })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cart updated:', data);
        window.location.href = 'http://127.0.0.1:8000/cart/';
        // Optionally, update the DOM to reflect new cart totals
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    });
}

