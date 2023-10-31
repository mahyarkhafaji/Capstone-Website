from docx import Document
import xlsxwriter
import requests
from bs4 import BeautifulSoup

# Set file path
document = Document('D:/wamp64/www/Web/syllabus.docx')

# The filename we want to create
#workbook2 = xlsxwriter.Workbook(r'C:/Users/mahya/Downloads/textbook.xlsx')

def textbook():
    #worksheet2 = workbook2.add_worksheet()
    j = 0

    for para in document.paragraphs:
	    if(len(document.paragraphs[j].text)>0):
		    if document.paragraphs[j].text == 'ISBN-13:':
			    isbn = document.paragraphs[j+1].text
	    j +=1

    #indx = 1
    url = 'https://www.cheapesttextbooks.com/IM/?keyval=' + isbn        # Define URL
    #data = requests.get(url)

    #html = BeautifulSoup(data.text, 'html.parser')
    
    #for link in html.find_all(class_= 'pt-even'):
    #    worksheet2.write('A' + str(indx), link.get_text())
    #    indx+= 1
   
    #for link in html.find_all(class_= 'pt-odd'):
    #    worksheet2.write('B' + str(indx), link.get_text())
    #    indx+=1
    with open("url.txt", "w") as file:
        # Write the string into the file
        file.write(url)
    return url
    
    #workbook2.close()

textbook()
print(textbook())