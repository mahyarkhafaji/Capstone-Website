<?php
session_start();
if(!isset($_SESSION['token'])){
  header('Location: homepage.php');
  exit;
}
require('config.php');

$client->setAccessToken($_SESSION['token']);

if($client->isAccessTokenExpired()){
  header('Location: logout.php');
  exit;
}
$google_oauth = new Google_Service_Oauth2($client);
$user_info = $google_oauth->userinfo->get();

$myfile = fopen("user.txt", "w") or die("Unable to open file!");
$name = $user_info['givenName'] . "_" .  $user_info['familyName'];
fwrite($myfile, $name);
fclose($myfile);
?>

<!DOCTYPE html>
<html lang="en">
<head>
<title>IT 445 Capstone</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
body,h1,h2,h3,h4,h5,h6 {font-family: "Lato", sans-serif}
.w3-bar,h1,button {font-family: "Montserrat", sans-serif}
.fa-anchor,.fa-coffee {font-size:200px}
</style>
</head>
<body>

  <!-- Navbar -->
<div class="w3-top">
  <div class="w3-bar w3-card w3-left-align w3-large" style="background-color:rgb(69, 0, 132);color:white">
    <a href="students.php" class="w3-bar-item w3-button w3-padding-large w3-white"><img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" alt="buttonpng" width="25"/></a>
    <a href="syllabus.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Upload Syllabus</a>
    <a href="calendar.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Calender</a>
    <a href="textbook.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Find Textbook</a>
    <a href="logout.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white w3-display-topright">Logout</a>
</div>

<!-- Header -->
<header class="w3-container w3-center" style="background-color:rgb(69, 0, 132);color:white;padding:128px 16px">
  <h1 class="w3-margin w3-jumbo">Welcome <?=$user_info['givenName'];?> <?=$user_info['familyName'];?>!</h1>
</header>

<!-- First Grid -->
<div class="w3-row-padding w3-padding-64 w3-container">
  <div class="w3-content">
    <div class="w3-twothird">
      <h3>Select an option from the menu on the top!</h1>
    </div>
  </div>
</div>

</body>
</html>