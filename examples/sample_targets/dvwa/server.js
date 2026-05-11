const express = require('express');
const app = express();
const mysql = require('mysql');

// VULNERABLE: Hardcoded database credentials
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password123',
    database: 'webapp'
});

// VULNERABLE: SQL Injection in Node.js
app.get('/user', (req, res) => {
    const id = req.query.id;
    const query = "SELECT * FROM users WHERE id = " + id;
    db.query(query, (err, results) => {
        res.json(results);
    });
});

// VULNERABLE: DOM-based XSS
app.get('/profile', (req, res) => {
    const name = req.query.name;
    res.send(`<h1>Welcome ${name}</h1><script>document.write(location.hash)</script>`);
});

// VULNERABLE: Command injection
app.get('/ping', (req, res) => {
    const host = req.query.host;
    const { exec } = require('child_process');
    exec('ping ' + host, (err, stdout) => {
        res.send(stdout);
    });
});

// VULNERABLE: Missing security headers, debug mode
app.listen(3000, () => {
    console.log('Server running - DEBUG MODE');
});
