const cart = [];

function updateCart() {
  const cartItems = document.getElementById('cart-items');
  cartItems.innerHTML = '';
  cart.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.name} - $${item.price}`;
    cartItems.appendChild(li);
  });
  document.getElementById('cart-count').textContent = cart.length;
  const total = cart.reduce((sum, item) => sum + item.price, 0);
  document.getElementById('cart-total').textContent = total;
}

document.querySelectorAll('.add-to-cart').forEach(btn => {
  btn.addEventListener('click', () => {
    const product = btn.closest('.product');
    const name = product.dataset.name;
    const price = parseFloat(product.dataset.price);
    cart.push({ name, price });
    updateCart();
  });
});

document.getElementById('cart-button').addEventListener('click', () => {
  const cartSection = document.getElementById('cart');
  cartSection.classList.toggle('hidden');
});
