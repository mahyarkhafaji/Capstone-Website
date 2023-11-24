<?php

require_once 'vendor/autoload.php';

//https://www.youtube.com/watch?v=HIMGOHtsEkQ
//https://www.devbabu.com/how-to-login-with-google-account-using-php/

//session_start();

// init configuration
$clientID = '549061950732-mletu705f02nhekufek7tv4ktf5tuahl.apps.googleusercontent.com';
$clientSecret = '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';
$redirectUri = 'http://localhost/web/homepage.php';

// create Client Request to access Google API
$client = new Google_Client();
$client->setClientId($clientID);
$client->setClientSecret($clientSecret);
$client->setRedirectUri($redirectUri);
//define('GOOGLE_OAUTH_SCOPE', 'https://www.googleapis.com/auth/calendar'); 
$client->addScope("email");
$client->addScope("profile");
//$client->addScope(Google\Service\Drive::DRIVE_METADATA_READONLY);
//$client->setAccessType('offline');
// Using "consent" will prompt the user for consent
//$client->setPrompt('consent');
//$client->setIncludeGrantedScopes(true);
?>