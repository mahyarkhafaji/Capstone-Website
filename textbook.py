from docx import Document
import xlsxwriter
import requests
from bs4 import BeautifulSoup


def textbook():
	# Set file path
    document = Document('D:/wamp64/www/Web/syllabus.docx')

# The filename we want to create
#workbook2 = xlsxwriter.Workbook(r'C:/Users/mahya/Downloads/textbook.xlsx')

#worksheet2 = workbook2.add_worksheet()
    j = 0

    for para in document.paragraphs:
	    if(len(document.paragraphs[j].text)>0):
		    if document.paragraphs[j].text == 'ISBN-13:':
			    isbn = document.paragraphs[j+1].text
	    j +=1

    #indx = 1
    url = 'https://www.cheapesttextbooks.com/IM/?keyval=' + isbn        # Define URL
    data = requests.get(url)

    html = BeautifulSoup(data.text, 'html.parser')
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
    <a href="calender.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Calender</a>
    <a href="textbook.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Find Textbook</a>
    <a href="logout.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white w3-display-topright">Logout</a>
</div>"""
    
    #for link in html.find_all(class_= 'pt-even'):
    #    worksheet2.write('A' + str(indx), link.get_text())
    #    indx+= 1
   
    #for link in html.find_all(class_= 'pt-odd'):
    #    worksheet2.write('B' + str(indx), link.get_text())
    #    indx+=1
    with open("finalText.html", "w") as file:
        # Write the string into the file
        file.write(nav)
        file.write(str(html.prettify()))

textbook()
print(textbook())
    
#workbook2.close()
