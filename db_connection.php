<?php
//https://www.devbabu.com/how-to-login-with-google-account-using-php/
// Connect to database
$hostname = "localhost";
$username = "root";
$password = "";
$database = "google-account";

$conn = mysqli_connect($hostname, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

?>