/**
 * ShoppingCart Module
 * Handles all shopping cart operations for UrbanVibe
 */
const ShoppingCart = (function() {
    // Private variables
    let _cart = {
        items: [],
        subtotal: 0,
        tax: 0,
        discount: 0,
        total: 0,
        voucherCode: ""
    };
    
    // DOM Elements
    let elements = {};
    
    // Constants
    const NOTIFICATION_DURATION = 1500; // Shortened animation duration (1.5s)
    const TAX_RATE = 0.10; // 10% tax
    
    /**
     * Initialize the shopping cart
     */
    function init() {
        // Cache DOM elements
        elements = {
            cartItemsContainer: document.getElementById('cart-items-container'),
            subtotalElement: document.getElementById('subtotal'),
            discountElement: document.getElementById('discount'),
            taxElement: document.getElementById('tax'),
            totalElement: document.getElementById('total'),
            checkoutButton: document.getElementById('checkout-button'),
            voucherInput: document.getElementById('voucherCode'),
            applyVoucherButton: document.getElementById('apply-voucher'),
            emptyCartMessage: document.getElementById('empty-cart-message')
        };
        
        // Check if user is authenticated
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (!isAuthenticated) {
            // For non-authenticated users, load cart from localStorage
            loadCartFromStorage();
            renderClientCart();
            calculateTotals();
            updateCartUI();
        }
        
        // Setup event listeners
        if (elements.applyVoucherButton) {
            elements.applyVoucherButton.addEventListener('click', applyVoucher);
        }
        
        if (elements.checkoutButton) {
            elements.checkoutButton.addEventListener('click', proceedToCheckout);
        }
        
        // Remove any existing notifications that might be lingering
        const existingNotificationContainer = document.getElementById('notification-container');
        if (existingNotificationContainer) {
            existingNotificationContainer.remove();
        }
    }
    
    /**
     * Load cart data from localStorage
     */
    function loadCartFromStorage() {
        const savedCart = localStorage.getItem('cartData');
        if (savedCart) {
            try {
                const parsedCart = JSON.parse(savedCart);
                if (parsedCart && Array.isArray(parsedCart.items)) {
                    _cart = parsedCart;
                }
            } catch (e) {
                console.error("Error parsing cart data:", e);
            }
        }
        
        // Check for saved voucher
        const savedVoucher = localStorage.getItem('voucherCode');
        if (savedVoucher && elements.voucherInput) {
            elements.voucherInput.value = savedVoucher;
            _cart.voucherCode = savedVoucher;
        }
    }
    
    /**
     * Save cart data to localStorage
     */
    function saveCartToStorage() {
        localStorage.setItem('cartData', JSON.stringify(_cart));
        if (_cart.voucherCode) {
            localStorage.setItem('voucherCode', _cart.voucherCode);
        }
    }
    
    /**
     * Calculate cart totals
     */
    function calculateTotals() {
        // Calculate subtotal
        _cart.subtotal = _cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        // Calculate tax (10%)
        _cart.tax = Math.round(_cart.subtotal * TAX_RATE);
        
        // Apply discount if voucher code exists
        if (_cart.voucherCode === "ibusesar") {
            _cart.discount = 50000;
        } else if (_cart.voucherCode === "URBAN25") {
            _cart.discount = Math.round(_cart.subtotal * 0.25);
        }
        
        // Calculate total
        _cart.total = _cart.subtotal + _cart.tax - _cart.discount;
    }
    
    /**
     * Update the cart UI
     */
    function updateCartUI() {
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (!isAuthenticated) {
            renderClientCart();
        }
        
        // Update summary totals
        if (elements.subtotalElement) {
            elements.subtotalElement.textContent = `Rp. ${_cart.subtotal.toLocaleString()}`;
        }
        
        if (elements.discountElement) {
            elements.discountElement.textContent = `Rp. ${_cart.discount.toLocaleString()}`;
        }
        
        if (elements.taxElement) {
            elements.taxElement.textContent = `Rp. ${_cart.tax.toLocaleString()}`;
        }
        
        if (elements.totalElement) {
            elements.totalElement.textContent = `Rp. ${_cart.total.toLocaleString()}`;
        }
        
        // Toggle empty cart message
        if (elements.emptyCartMessage) {
            if (_cart.items.length === 0) {
                elements.emptyCartMessage.style.display = 'block';
            } else {
                elements.emptyCartMessage.style.display = 'none';
            }
        }
        
        // Save cart to localStorage for non-authenticated users
        if (!isAuthenticated) {
            saveCartToStorage();
        }
    }
    
    /**
     * Render cart items for non-authenticated users
     */
    function renderClientCart() {
        if (!elements.cartItemsContainer) return;
        
        // Only render for non-authenticated users
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        if (isAuthenticated) return;
        
        // Clear container
        const clientItemsContainer = document.getElementById('client-items');
        if (clientItemsContainer) {
            clientItemsContainer.innerHTML = '';
            
            _cart.items.forEach((item, index) => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('flex', 'items-center', 'border', 'rounded-lg', 'p-4', 'shadow');
                itemElement.dataset.itemId = item.id;
                
                itemElement.innerHTML = `
                    <img src="https://i.pinimg.com/736x/be/0e/95/be0e95ca27bdf6de0c06406b8fc13d48.jpg" 
                         alt="${item.name}" class="w-24 h-24 object-cover rounded-md">
                    <div class="ml-4">
                        <h3 class="text-lg font-semibold">${item.name}</h3>
                        ${item.color ? `<p>Colour: ${item.color}</p>` : ''}
                        ${item.size ? `<p>Size: ${item.size}</p>` : ''}
                        <p class="text-pink-600 font-semibold">Rp. ${item.price.toLocaleString()}</p>
                        <div class="mt-2 flex items-center">
                            <button onclick="ShoppingCart.updateItemQuantity('${item.id}', 'decrease')" class="px-3 py-1 bg-gray-300 rounded">-</button>
                            <span class="px-4">${item.quantity}</span>
                            <button onclick="ShoppingCart.updateItemQuantity('${item.id}', 'increase')" class="px-3 py-1 bg-gray-300 rounded">+</button>
                            <button onclick="ShoppingCart.updateItemQuantity('${item.id}', 'remove')" class="px-3 py-1 bg-red-500 text-white rounded ml-3">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `;
                
                clientItemsContainer.appendChild(itemElement);
            });
            
            // Toggle empty cart message
            if (_cart.items.length === 0 && elements.emptyCartMessage) {
                elements.emptyCartMessage.style.display = 'block';
            } else if (elements.emptyCartMessage) {
                elements.emptyCartMessage.style.display = 'none';
            }
        }
    }
    
    /**
     * Add an item to the cart
     * @param {Object} product - The product to add
     * @param {number} quantity - The quantity to add
     */
    function addToCart(product, quantity = 1) {
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (isAuthenticated) {
            // For authenticated users, make an AJAX request to the server
            fetch('/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: product.id,
                    product_type: product.type,
                    quantity: quantity,
                    color: product.color,
                    size: product.size
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(`${product.name} added to cart`, 'success');
                    
                    // Refresh the page to update cart
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    showNotification(data.message || 'Error adding to cart', 'error');
                }
            })
            .catch(error => {
                console.error('Error adding to cart:', error);
                showNotification('Error adding to cart', 'error');
            });
        } else {
            // For non-authenticated users, manage cart in localStorage
            const existingItemIndex = _cart.items.findIndex(item => 
                item.id === product.id && 
                item.type === product.type &&
                item.color === product.color &&
                item.size === product.size
            );
            
            if (existingItemIndex !== -1) {
                // Update existing item
                _cart.items[existingItemIndex].quantity += quantity;
            } else {
                // Add new item
                _cart.items.push({
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    type: product.type,
                    color: product.color,
                    size: product.size,
                    quantity: quantity
                });
            }
            
            // Recalculate and update UI
            calculateTotals();
            updateCartUI();
            
            // Show notification
            showNotification(`${product.name} added to cart`, 'success');
        }
    }
    
    /**
     * Update item quantity in cart
     * @param {string} itemId - The item ID
     * @param {string} action - The action to perform (increase, decrease, remove)
     */
    function updateItemQuantity(itemId, action) {
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (isAuthenticated) {
            // For authenticated users, make an AJAX request to the server
            fetch('/update-cart-item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    item_id: itemId,
                    action: action
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.removed) {
                    // Remove item from DOM
                    const itemElement = document.getElementById(`item-${itemId}`);
                    if (itemElement) {
                        itemElement.remove();
                    }
                    
                    // Update cart summary
                    if (elements.subtotalElement) {
                        elements.subtotalElement.textContent = `Rp. ${data.cart_total.toLocaleString()}`;
                    }
                    
                    if (elements.totalElement) {
                        elements.totalElement.textContent = `Rp. ${data.final_total.toLocaleString()}`;
                    }
                    
                    if (elements.taxElement) {
                        elements.taxElement.textContent = `Rp. ${data.tax.toLocaleString()}`;
                    }
                    
                    // Show empty cart message if no items left
                    if (data.cart_items === 0 && elements.emptyCartMessage) {
                        elements.emptyCartMessage.style.display = 'block';
                    }
                    
                    showNotification('Item removed from cart', 'success');
                } else {
                    // Refresh the page to update cart
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error updating cart:', error);
                showNotification('Error updating cart', 'error');
            });
        } else {
            // For non-authenticated users, manage cart in localStorage
            const itemIndex = _cart.items.findIndex(item => item.id == itemId);
            
            if (itemIndex !== -1) {
                if (action === 'increase') {
                    _cart.items[itemIndex].quantity += 1;
                    showNotification('Item quantity increased', 'success');
                } else if (action === 'decrease') {
                    if (_cart.items[itemIndex].quantity > 1) {
                        _cart.items[itemIndex].quantity -= 1;
                        showNotification('Item quantity decreased', 'success');
                    } else {
                        _cart.items.splice(itemIndex, 1);
                        showNotification('Item removed from cart', 'success');
                    }
                } else if (action === 'remove') {
                    _cart.items.splice(itemIndex, 1);
                    showNotification('Item removed from cart', 'success');
                }
                
                // Recalculate and update UI
                calculateTotals();
                updateCartUI();
            }
        }
    }
    
    /**
     * Apply voucher code to the cart
     */
    function applyVoucher() {
        const voucherCode = elements.voucherInput.value.trim();
        
        if (!voucherCode) {
            showNotification('Please enter a voucher code', 'error');
            return;
        }
        
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (isAuthenticated) {
            // For authenticated users, make an AJAX request to the server
            fetch('/apply-voucher/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    voucher_code: voucherCode
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    showNotification(data.message, 'success');
                    
                    // Update discount and total in UI
                    if (elements.discountElement) {
                        elements.discountElement.textContent = `Rp. ${data.discount_amount.toLocaleString()}`;
                    }
                    
                    if (elements.totalElement) {
                        elements.totalElement.textContent = `Rp. ${data.final_total.toLocaleString()}`;
                    }
                    
                    if (elements.taxElement) {
                        elements.taxElement.textContent = `Rp. ${data.tax.toLocaleString()}`;
                    }
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error applying voucher:', error);
                showNotification('Error applying voucher', 'error');
            });
        } else {
            // For non-authenticated users, apply voucher locally
            let discountAmount = 0;
            let valid = false;
            let message = "Invalid voucher code";
            
            if (voucherCode === "ibusesar") {
                discountAmount = 50000;
                valid = true;
                message = "Voucher applied successfully! Discount: Rp. 50.000";
            } else if (voucherCode === "URBAN25") {
                discountAmount = Math.round(_cart.subtotal * 0.25);
                valid = true;
                message = `Voucher applied successfully! Discount: Rp. ${discountAmount.toLocaleString()}`;
            }
            
            if (valid) {
                _cart.voucherCode = voucherCode;
                _cart.discount = discountAmount;
                
                // Recalculate and update UI
                calculateTotals();
                updateCartUI();
                
                // Save voucher to localStorage
                localStorage.setItem('voucherCode', voucherCode);
                
                showNotification(message, 'success');
            } else {
                showNotification(message, 'error');
                
                // Remove invalid voucher
                _cart.voucherCode = "";
                _cart.discount = 0;
                localStorage.removeItem('voucherCode');
                
                // Recalculate and update UI
                calculateTotals();
                updateCartUI();
            }
        }
    }
    
    /**
     * Proceed to checkout
     */
    function proceedToCheckout() {
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        
        if (isAuthenticated) {
            window.location.href = "/checkout/";
        } else {
            // Redirect to login with return URL
            window.location.href = "/login/?next=/checkout/";
        }
    }
    
    /**
     * Show notification
     * @param {string} message - The notification message
     * @param {string} type - The notification type (success, error)
     */
    function showNotification(message, type = 'success') {
        // Remove any existing notifications first
        let existingNotificationContainer = document.getElementById('notification-container');
        if (existingNotificationContainer) {
            existingNotificationContainer.remove();
        }
        
        // Create notification container
        let notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(notificationContainer);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.classList.add('notification');
        notification.style.cssText = `
            background-color: ${type === 'success' ? '#10b981' : '#ef4444'};
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: slideIn 0.3s ease, fadeOut 0.3s ease ${NOTIFICATION_DURATION/1000 - 0.3}s forwards;
            display: flex;
            align-items: center;
        `;
        
        // Add icon based on type
        const icon = type === 'success' ? '✅' : '❌';
        
        notification.innerHTML = `
            <span style="margin-right: 8px;">${icon}</span>
            <span>${message}</span>
        `;
        
        // Add to container
        notificationContainer.appendChild(notification);
        
        // Remove after duration
        setTimeout(() => {
            notification.remove();
            notificationContainer.remove();
        }, NOTIFICATION_DURATION);
    }
    
    /**
     * Get CSRF token from cookies
     * @returns {string} The CSRF token
     */
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        return cookieValue || '';
    }
    
    // Public API
    return {
        init,
        addToCart,
        updateItemQuantity,
        showNotification
    };
})();

// Add keyframe animations for notification
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    /* Remove any default styles that might be causing position issues */
    .notification, #notification-container {
        margin: 0;
        padding: 0;
    }
    
    #notification-container {
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        left: auto !important;
        bottom: auto !important;
        z-index: 9999 !important;
    }
`;
document.head.appendChild(styleSheet);