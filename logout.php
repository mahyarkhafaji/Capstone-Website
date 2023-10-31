<?php

session_start();

if(!isset($_SESSION['token'])){
  header('Location: homepage.php');
  exit;
}

require('./config.php');
$client = new Google\Client();
$client->setAccessToken($_SESSION['token']);
# Revoking the google access token
$client->revokeToken();

# Deleting the session that we stored
$_SESSION = array();

if (ini_get("session.use_cookies")) {
  $params = session_get_cookie_params();
  setcookie(session_name(), '', time() - 42000,
      $params["path"], $params["domain"],
      $params["secure"], $params["httponly"]
  );
}

session_destroy();
header("Location: homepage.php");
exit;
?>