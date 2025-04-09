document.getElementById('book-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const genre = document.getElementById('genre').value;
    const year = document.getElementById('year').value;

    fetch('http://localhost:3000/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, author, genre, year })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadBooks();
        document.getElementById('book-form').reset();
    })
    .catch(error => console.error('Error:', error));
});

function loadBooks() {
    fetch('http://localhost:3000/books')
        .then(response => response.json())
        .then(books => {
            displayBooks(books);
            populateAuthorFilter(books);
        })
        .catch(error => console.error('Error:', error));
}

function displayBooks(books) {
    const tableBody = document.querySelector('#book-list tbody');
    tableBody.innerHTML = '';
    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${book.Title}</td><td>${book.Author}</td><td>${book.Genre}</td><td>${book.PublishedYear}</td><td>${book.Status == "undefined" ?"Loaned":"Available"}</td>`;
        tableBody.appendChild(row);
    });
}

function populateAuthorFilter(books) {
    const authorFilter = document.getElementById('author-filter');
    const authors = [...new Set(books.map(book => book.Author))];
    authorFilter.innerHTML = '<option value="">All Authors</option>';
    authors.forEach(author => {
        const option = document.createElement('option');
        option.value = author;
        option.textContent = author;
        authorFilter.appendChild(option);
    });
}

document.getElementById('author-filter').addEventListener('change', applyFilters);
document.getElementById('loan-filter').addEventListener('change', applyFilters);

function applyFilters() {
    const author = document.getElementById('author-filter').value;
    const loanStatus = document.getElementById('loan-filter').value;

    fetch('http://localhost:3000/books')
        .then(response => response.json())
        .then(books => {
            let filteredBooks = books;
            if (author) {
                filteredBooks = filteredBooks.filter(book => book.Author === author);
            }
            if (loanStatus) {
                filteredBooks = filteredBooks.filter(book => book.Status === (loanStatus === 'loaned' ? 'Loaned Out' : 'Available'));
            }
            displayBooks(filteredBooks);
        })
        .catch(error => console.error('Error:', error));
}

loadBooks();
