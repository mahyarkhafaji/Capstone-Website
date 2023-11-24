<?php
$target_dir = "D:/wamp64/www/Web/";  // Directory to save the uploaded files
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

if (isset($_POST["submit"])) {
    // Check if file is a Word document
    $fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
    if($fileType != "doc" && $fileType != "docx") {
        echo "Sorry, only DOC & DOCX files are allowed.";
        exit;
    }

    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        //echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
        //$command = escapeshellcmd('python D:/wamp64/www/Web/textbook.py');
        //$output = shell_exec($command);
        //echo $output;
        echo shell_exec("python textbook.py");
        header("Location: http://localhost/web/finalText.html");
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
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

<!--<script>
  fetch("url.txt")
  .then((res) => res.text())
  .then((text) => {
    // do something with "text"
    window.open(text, "_blank"); // will open new tab on window.onload
   })
  .catch((e) => console.error(e));
    //window.onload = function(){
        // window.open(client.responseText, "_blank"); // will open new tab on window.onload
    //}
</script>-->

<!-- Header 
<header class="w3-container w3-center" style="background-color:rgb(69, 0, 132);color:white;padding:128px 16px">
  <h1 class="w3-margin w3-jumbo">Find your Textbook!</h1>
</header>-->

<!-- First Grid 
<div class="w3-row-padding w3-padding-64 w3-container">
  <div class="w3-content">
    <p><//?=$output;?></p>
  </div>
</div>-->

</body>
</html>