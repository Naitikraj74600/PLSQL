// server.js
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// MySQL Database Connection
const db = mysql.createConnection({
    host: 'localhost',       // Update if necessary
    user: 'root',            // Your MySQL username
    password: 'jaishreeram@1', // Your MySQL password
    database: 'librarymanagementsystem' // Your database name
});

db.connect(err => {
    if (err) throw err;
    console.log("MySQL connected.");
});

// Set up API routes
app.get('/books', (req, res) => {
    const sql = 'SELECT * FROM Books';
    db.query(sql, (err, results) => {
        if (err) res.status(500).send(err);
        else res.json(results);
    });
});

app.post('/books', (req, res) => {
    const { title, author, genre, year } = req.body;
    const sql = 'INSERT INTO Books (Title, Author, Genre, PublishedYear) VALUES (?, ?, ?, ?)';
    db.query(sql, [title, author, genre, year], (err, result) => {
        if (err) res.status(500).send(err);
        else res.json({ message: 'Book added', bookId: result.insertId });
    });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
