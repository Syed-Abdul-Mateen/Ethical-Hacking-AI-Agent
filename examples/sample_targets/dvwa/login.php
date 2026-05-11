<?php
// Vulnerable login page - SQL Injection
$username = $_POST['username'];
$password = $_POST['password'];

// VULNERABLE: Direct string concatenation in SQL query
$query = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "'";
$result = mysqli_query($conn, $query);

// VULNERABLE: No CSRF protection, no rate limiting
if (mysqli_num_rows($result) > 0) {
    session_start();
    $_SESSION['user'] = $username;
    header("Location: dashboard.php");
}
?>
<html>
<head><title>Login</title></head>
<body>
<form method="POST" action="login.php">
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Login</button>
</form>
</body>
</html>
