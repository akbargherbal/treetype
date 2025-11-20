// PATTERN: DOM Manipulation

// Assume an HTML element like <button id="submitButton">Submit</button> exists
const submitButton = document.querySelector('#submitButton');

if (submitButton) {
  console.log('Submit button found:', submitButton);
  submitButton.style.backgroundColor = 'lightblue';
}

// PATTERN: DOM Manipulation

// Assume HTML elements like <li class="task-item">Task 1</li>
const taskItems = document.querySelectorAll('.task-item');

taskItems.forEach(item => {
  console.log('Task:', item.textContent);
  item.style.color = 'blue';
});

// PATTERN: DOM Manipulation

// Assume an HTML element like <button id="actionButton">Click Me</button>
const actionButton = document.querySelector('#actionButton');

if (actionButton) {
  actionButton.addEventListener('click', () => {
    console.log('Button was clicked!');
    alert('Hello from the event listener!');
  });
}

// PATTERN: DOM Manipulation

// Assume an HTML element like <div id="container"></div>
const container = document.querySelector('#container');

if (container) {
  const newParagraph = document.createElement('p');
  newParagraph.textContent = 'This is a dynamically created paragraph.';
  newParagraph.style.color = 'green';
  container.appendChild(newParagraph);
}

// PATTERN: DOM Manipulation

// Assume an HTML element like <div id="statusBox" class="inactive"></div>
const statusBox = document.querySelector('#statusBox');

if (statusBox) {
  statusBox.classList.add('active'); // Adds 'active' class
  statusBox.classList.remove('inactive'); // Removes 'inactive' class
  statusBox.classList.toggle('highlight'); // Toggles 'highlight' class
  console.log('Current classes:', statusBox.classList);
}

// PATTERN: DOM Manipulation

// Assume an HTML element like <a id="myLink" href="https://example.com">Visit Example</a>
const myLink = document.querySelector('#myLink');

if (myLink) {
  const currentHref = myLink.getAttribute('href');
  console.log('Current Href:', currentHref);

  myLink.setAttribute('target', '_blank'); // Sets target attribute
  myLink.setAttribute('title', 'Opens in a new tab'); // Sets title attribute
}

// PATTERN: DOM Manipulation

// Assume an HTML element like <div id="contentArea"></div>
const contentArea = document.querySelector('#contentArea');

if (contentArea) {
  // innerHTML interprets HTML tags
  contentArea.innerHTML = '<b>Hello</b> <em>World!</em>';
  console.log('innerHTML set.');

  // textContent treats everything as plain text
  // contentArea.textContent = '<b>Hello</b> <em>World!</em>';
  // console.log('textContent set.');
}

// PATTERN: DOM Manipulation

// Assume an HTML element like <div id="productCard" data-product-id="123" data-category="electronics"></div>
const productCard = document.querySelector('#productCard');

if (productCard) {
  const productId = productCard.dataset.productId; // Accesses data-product-id
  const category = productCard.dataset.category;   // Accesses data-category

  console.log('Product ID:', productId);
  console.log('Category:', category);

  productCard.dataset.status = 'available'; // Sets data-status="available"
}

// PATTERN: DOM Manipulation

// Assume HTML like <ul id="taskList"><li class="task">Task 1</li><li class="task">Task 2</li></ul>
const taskList = document.querySelector('#taskList');

if (taskList) {
  taskList.addEventListener('click', (event) => {
    if (event.target.classList.contains('task')) {
      console.log('Clicked task:', event.target.textContent);
      event.target.style.textDecoration = 'line-through';
    }
  });
}