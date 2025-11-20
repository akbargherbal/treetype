// PATTERN: DOM Manipulation

const submitButton = document.querySelector('#submitButton');

if (submitButton) {
  console.log('Button text:', submitButton.textContent);
  submitButton.style.backgroundColor = 'lightblue';
}

// PATTERN: DOM Manipulation

const listItems = document.querySelectorAll('.product-item');

listItems.forEach(item => {
  console.log('Product ID:', item.id);
  item.style.border = '1px solid #ccc';
});

// PATTERN: DOM Manipulation

const actionButton = document.querySelector('#actionButton');

if (actionButton) {
  actionButton.addEventListener('click', () => {
    alert('Action button was clicked!');
    console.log('Button click event fired.');
  });
}

// PATTERN: DOM Manipulation

const newParagraph = document.createElement('p');
newParagraph.textContent = 'This is a dynamically created paragraph.';
newParagraph.classList.add('dynamic-content');

const contentArea = document.querySelector('#contentArea');
if (contentArea) {
  contentArea.appendChild(newParagraph);
}

// PATTERN: DOM Manipulation

const themeToggleButton = document.querySelector('#themeToggle');
const bodyElement = document.body;

if (themeToggleButton) {
  themeToggleButton.addEventListener('click', () => {
    bodyElement.classList.toggle('dark-theme');
    console.log('Dark theme toggled:', bodyElement.classList.contains('dark-theme'));
  });
}

// PATTERN: DOM Manipulation

const userAvatar = document.querySelector('#userAvatar');

if (userAvatar) {
  const currentSrc = userAvatar.getAttribute('src');
  console.log('Current avatar source:', currentSrc);

  userAvatar.setAttribute('src', 'https://example.com/new-avatar.jpg');
  userAvatar.setAttribute('alt', 'New User Profile Picture');
}

// PATTERN: DOM Manipulation

const htmlDisplay = document.querySelector('#htmlDisplay');
const textDisplay = document.querySelector('#textDisplay');

if (htmlDisplay) {
  htmlDisplay.innerHTML = '<strong>Important</strong> message!';
}

if (textDisplay) {
  textDisplay.textContent = '<strong>Important</strong> message!';
}

// PATTERN: DOM Manipulation

const productCard = document.querySelector('#productCard123');

if (productCard) {
  const productId = productCard.dataset.productId;
  const productCategory = productCard.dataset.category;
  console.log(`Product ID: ${productId}, Category: ${productCategory}`);

  productCard.dataset.status = 'available';
  console.log('New status:', productCard.dataset.status);
}

// PATTERN: DOM Manipulation

const productList = document.querySelector('#productList');

if (productList) {
  productList.addEventListener('click', (event) => {
    const clickedItem = event.target.closest('.product-item');
    if (clickedItem) {
      console.log('Clicked product:', clickedItem.textContent);
      clickedItem.style.backgroundColor = '#e0e0e0';
    }
  });
}