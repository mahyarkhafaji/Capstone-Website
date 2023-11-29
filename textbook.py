from typing import Text
import docx
import re
import requests
from bs4 import BeautifulSoup

def find_isbns(docx_path):
    # Open the Word document
    doc = docx.Document(docx_path)

    isbns = []

    # Iterate through paragraphs in the document
    for paragraph in doc.paragraphs:
        text = paragraph.text
        # You'll need to implement a regular expression pattern
        isbn_pattern = r'ISBN-13:\s(\d{13})'
        isbns.extend(re.findall(isbn_pattern, text))

    return isbns

def textbook():
	# Set file path
  doc_path = "D:/XAMPP/htdocs/Web/syllabus-generated.docx"
  isbns = find_isbns(doc_path)
  nav = """<!DOCTYPE html>
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
    <a href="calendar.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Calender</a>
    <a href="textbook.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Find Textbook</a>
    <a href="logout.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white w3-display-topright">Logout</a>
</div>"""
  if isbns:
        for isbn in isbns:
            # Construct the URL using each ISBN-13
            url = 'https://www.cheapesttextbooks.com/IM/?keyval=' + isbn
            data = requests.get(url)
            html = BeautifulSoup(data.text, 'html.parser')
            with open("finalText.html", "w") as file:
              # Write the string into the file
              file.write(nav)
              file.write(str(html.prettify()))
  else:
      print("Error: No ISBN")

textbook()