<?php
require_once 'config.php';

$login_url = $client->createAuthUrl();

if (isset($_GET['code'])):

  session_start();
  $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
  if(isset($token['error'])){
    header('Location: homepage.php');
    exit;
  }
  $_SESSION['token'] = $token;

 /* -- Inserting the user data into the database -- */

  # Fetching the user data from the google account
  $client->setAccessToken($token);
  $google_oauth = new Google_Service_Oauth2($client);
  $user_info = $google_oauth->userinfo->get();

  $google_id = trim($user_info['id']);
  $f_name = trim($user_info['given_name']);
  $l_name = trim($user_info['family_name']);
  $email = trim($user_info['email']);
  $gender = trim($user_info['gender']);
  $local = trim($user_info['local']);
  $picture = trim($user_info['picture']);

  # Database connection
  require('./db_connection.php');

  # Checking whether the email already exists in our database.
  $check_email = $conn->prepare("SELECT `email` FROM `users` WHERE `email`=?");
  $check_email->bind_param("s", $email);
  $check_email->execute();
  $check_email->store_result();
  
    if($check_email->num_rows === 0){
      # Inserting the new user into the database
      $query_template = "INSERT INTO `users` (`oauth_uid`, `first_name`, `last_name`,`email`,`profile_pic`,`gender`,`local`) VALUES (?,?,?,?,?,?,?)";
      $insert_stmt = $conn->prepare($query_template);
      $insert_stmt->bind_param("sssssss", $google_id, $f_name, $l_name, $email, $gender, $local, $picture);
      if(!$insert_stmt->execute()){
        echo "Failed to insert user.";
        exit;
      }
    }
    header('Location: students.php');
    exit;
endif;
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
        /* Style for the buttons container */
        .buttons-container {
            display: flex;           /* Enable Flexbox */
            justify-content: center; /* Center buttons horizontally */
            gap: 10px;               /* Add some space between buttons */
        }

        /* Style for individual buttons */
        .w3-button {
            margin-top: 0;           /* Remove margin-top from individual buttons */
        }
    </style>
</head>
<body>

<!-- Header -->
<header class="w3-container w3-center" style="background-color:rgb(69, 0, 132);color:white;padding:10px 16px">
  <img src="JMU-Logo-white.png" alt="JMU Logo" style="height:300px;">
  <h1 class="w3-margin">Welcome to the IT 445 Capstone Website!</h1>
</header>

<!-- First Grid -->
<div class="w3-row-padding w3-padding-64 w3-container">
  <div class="w3-content">
    <div class="w3-twothird">
      <h1>Are you a student or a professor?</h1>
      <h3>For students, you will need to have an google account and sign in through Google.</h3>
      <div class="buttons-container">
        <button class="w3-button w3-black w3-padding-large w3-large" onclick="window.location.href='professor.html'">Professor</button>
        <a href="<?= $login_url ?>">
          <button class="w3-button w3-black w3-padding-large w3-large">Students</button>
        </a>
      </div>
    </div>
  </div>
</div>

</body>
</html>
