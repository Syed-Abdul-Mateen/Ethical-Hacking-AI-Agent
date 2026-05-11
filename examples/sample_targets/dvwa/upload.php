<?php
// Vulnerable file upload - Path Traversal and Command Injection
$filename = $_POST['filename'];

// VULNERABLE: Path traversal - no sanitization of file path
$filepath = "/uploads/" . $filename;
move_uploaded_file($_FILES['file']['tmp_name'], $filepath);

// VULNERABLE: Command injection - unsanitized input passed to shell
$cmd = "file " . $_GET['path'];
$output = shell_exec($cmd);
echo "<pre>" . $output . "</pre>";

// VULNERABLE: eval() with user input
$code = $_GET['code'];
eval($code);

// VULNERABLE: Hardcoded credentials
$db_password = "admin123";
$api_key = "sk-proj-ABCDEFGHIJKLMNOP1234567890";
$secret = "MySuperSecretKey2024!";

// VULNERABLE: Weak encryption
$encrypted = base64_encode($password);
$hash = md5($password);

// VULNERABLE: Debug code left in production
error_reporting(E_ALL);
ini_set('display_errors', 1);
phpinfo();
?>
