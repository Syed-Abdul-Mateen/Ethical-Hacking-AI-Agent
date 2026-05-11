<?php
// Vulnerable search page - XSS and SQL Injection
$search = $_GET['q'];

// VULNERABLE: Reflected XSS - user input directly echoed
echo "<h1>Search results for: " . $search . "</h1>";

// VULNERABLE: SQL Injection - direct concatenation
$query = "SELECT * FROM products WHERE name LIKE '%" . $search . "%'";
$result = mysqli_query($conn, $query);

// VULNERABLE: Error message exposes database info
if (!$result) {
    echo "Error: " . mysqli_error($conn);
}

while ($row = mysqli_fetch_assoc($result)) {
    // VULNERABLE: Stored XSS - database content printed without encoding
    echo "<div>" . $row['name'] . " - " . $row['description'] . "</div>";
}
?>
