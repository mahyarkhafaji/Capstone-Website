<?php

define("server_name", "localhost");
define("username", "root");
define("password","");
define("database_name","questionnaire");

$conn = mysqli_connect(server_name, username, password, database_name);
// $conn = new mysqli(server_name, username, password, database_name);

if (!$conn) {
    die("Connection Failed:" . mysqli_connect_error());
}

if(isset($_POST["save"])){
    $Q1 = $_POST["Q1"];
    $Q2 = $_POST["Q2"];
    $Q3 = $_POST["Q3"];
    $Q4 = $_POST["Q4"];
    $Q5 = $_POST["Q5"];
    $Q6 = $_POST["Q6"];
    $Q7 = $_POST["Q7"];
    $Q8 = $_POST["Q8"];
    $Q9 = $_POST["Q9"];
    $Q10 = $_POST["Q10"];
    $Q11 = $_POST["Q11"];
    $Q12 = $_POST["Q12"];
    $Q13 = $_POST["Q13"];
    $Q14 = $_POST["Q14"];
    $Q15 = $_POST["Q15"];
    $Q16 = $_POST["Q16"];
    $Q17 = $_POST["Q17"];
    $Q18 = $_POST["Q18"];
    $Q19 = $_POST["Q19"];
    $Q20 = $_POST["Q20"];
    $Q21 = $_POST["Q21"];
    $Q22 = $_POST["Q22"];
    $Q23 = $_POST["Q23"];
    $Q24 = $_POST["Q24"];
    $Q25 = $_POST["Q25"];
    $Q26 = $_POST["Q26"];
    $Q27 = $_POST["Q27"];
    $Q28 = $_POST["Q28"];
    $Q29 = $_POST["Q29"];
    $Q30 = $_POST["Q30"];
    $Q31 = $_POST["Q31"];
    $Q32 = $_POST["Q32"];
    $Q33 = $_POST["Q33"];
    $Q34 = $_POST["Q34"];
    $Q35 = $_POST["Q35"];
    $Q36 = $_POST["Q36"];
    $Q37 = $_POST["Q37"];
    $Q38 = $_POST["Q38"];
    $Q39 = $_POST["Q39"];
    $Q40 = $_POST["Q40"];
    $Q41 = $_POST["Q41"];
    $Q42 = $_POST["Q42"];
    $Q43 = $_POST["Q43"];
    $Q44 = $_POST["Q44"];
    $Q45 = $_POST["Q45"];
    $Q46 = $_POST["Q46"];
    $Q47 = $_POST["Q47"];
    $Q48 = $_POST["Q48"];
    $Q49 = $_POST["Q49"];
    $Q50 = $_POST["Q50"];
    $Q51 = $_POST["Q51"];
    $Q52 = $_POST["Q52"];
    $Q53 = $_POST["Q53"];
    $Q54 = $_POST["Q54"];
    $Q55 = $_POST["Q55"];
    $Q56 = $_POST["Q56"];
    $Q57 = $_POST["Q57"];
    $Q58 = $_POST["Q58"];

    $query = "INSERT INTO answers (Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q42, Q43, Q44, Q45, Q46, Q47, Q48, Q49, Q50, Q51, Q52, Q53, Q54, Q55, Q56, Q57, Q58) VALUES('$Q1', '$Q2', '$Q3', '$Q4', '$Q5', '$Q6', '$Q7', '$Q8', '$Q9', '$Q10', '$Q11', '$Q12', '$Q13', '$Q14', '$Q15', '$Q16', '$Q17', '$Q18', '$Q19', '$Q20', '$Q21', '$Q22', '$Q23', '$Q24', '$Q25', '$Q26', '$Q27', '$Q28', '$Q29', '$Q30', '$Q31', '$Q32', '$Q33', '$Q34', '$Q35', '$Q36', '$Q37', '$Q38', '$Q39', '$Q40', '$Q41', '$Q42', '$Q43', '$Q44', '$Q45', '$Q46', '$Q47', '$Q48', '$Q49', '$Q50', '$Q51', '$Q52', '$Q53', '$Q54', '$Q55', '$Q56', '$Q57', '$Q58')";

    $query2 = "SELECT * FROM answers ORDER BY id DESC LIMIT 1";

    if (mysqli_query($conn, $query)) {
      echo "New Details Entry inserted successfully !";
    } else {
      echo "Error: " . $sql . "" . mysqli_error($conn);
    }

    // Create an empty array
    $my_array = array();

    $result = mysqli_query($conn, $query2);

    // Loop through the result set and add the values to the array
    while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
      $my_array[] = $row['Q1'];
      $my_array[] = $row['Q2'];
      $my_array[] = $row['Q3'];
      $my_array[] = $row['Q4'];
      $my_array[] = $row['Q5'];
      $my_array[] = $row['Q6'];
      $my_array[] = $row['Q7'];
      $my_array[] = $row['Q8'];
      $my_array[] = $row['Q9'];
      $my_array[] = $row['Q10'];
      $my_array[] = $row['Q11'];
      $my_array[] = $row['Q12'];
      $my_array[] = $row['Q13'];
      $my_array[] = $row['Q14'];
      $my_array[] = $row['Q15'];
      $my_array[] = $row['Q16'];
      $my_array[] = $row['Q17'];
      $my_array[] = $row['Q18'];
      $my_array[] = $row['Q19'];
      $my_array[] = $row['Q20'];
      $my_array[] = $row['Q21'];
      $my_array[] = $row['Q22'];
      $my_array[] = $row['Q23'];
      $my_array[] = $row['Q24'];
      $my_array[] = $row['Q25'];
      $my_array[] = $row['Q26'];
      $my_array[] = $row['Q27'];
      $my_array[] = $row['Q28'];
      $my_array[] = $row['Q29'];
      $my_array[] = $row['Q30'];
      $my_array[] = $row['Q31'];
      $my_array[] = $row['Q32'];
      $my_array[] = $row['Q33'];
      $my_array[] = $row['Q34'];
      $my_array[] = $row['Q35'];
      $my_array[] = $row['Q36'];
      $my_array[] = $row['Q37'];
      $my_array[] = $row['Q38'];
      $my_array[] = $row['Q39'];
      $my_array[] = $row['Q40'];
      $my_array[] = $row['Q41'];
      $my_array[] = $row['Q42'];
      $my_array[] = $row['Q43'];
      $my_array[] = $row['Q44'];
      $my_array[] = $row['Q45'];
      $my_array[] = $row['Q46'];
      $my_array[] = $row['Q47'];
      $my_array[] = $row['Q48'];
      $my_array[] = $row['Q49'];
      $my_array[] = $row['Q50'];
      $my_array[] = $row['Q51'];
      $my_array[] = $row['Q52'];
      $my_array[] = $row['Q53'];
      $my_array[] = $row['Q54'];
      $my_array[] = $row['Q55'];
      $my_array[] = $row['Q56'];
      $my_array[] = $row['Q57'];
      $my_array[] = $row['Q58'];
    }

    if ($result) {
      print_r($my_array);
      $json = json_encode($my_array);
      file_put_contents('qa.txt', $json);
    } else {
      echo "Error: " . $sql . "" . mysqli_error($conn);
    }

    echo shell_exec("python generateSyllabus.py");

    mysqli_close($conn);
}

?>