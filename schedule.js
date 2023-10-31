//columns of the table
const col1 = [];
const col2 = [];
const col3 = [];
const col4 = [];
const col5 = [];
const col6 = [];
const col7 = [];


function addRow() {
    var date = document.getElementById("date").value;
    var topic = document.getElementById("topic").value;
    var assignment = document.getElementById("assignment").value;
    var lab = document.getElementById("lab").value;
    var discussion = document.getElementById("discussion").value;
    var quiz = document.getElementById("quiz").value;
    var exam = document.getElementById("exam").value;

    var table = document.getElementById("schedule");
    var row = table.insertRow(-1);

    //push data into the array
    col1.push(date);
    col2.push(topic);
    col3.push(assignment);
    col4.push(lab);
    col5.push(discussion);
    col6.push(quiz);
    col7.push(exam);

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);
    var cell7 = row.insertCell(6);

    cell1.innerHTML = date;
    cell2.innerHTML = topic;
    cell3.innerHTML = assignment;
    cell4.innerHTML = lab;
    cell5.innerHTML = discussion;
    cell6.innerHTML = quiz;
    cell7.innerHTML = exam;

    document.getElementById("date").value = "";
    document.getElementById("topic").value = "";
    document.getElementById("assignment").value = "";
    document.getElementById("lab").value = "";
    document.getElementById("discussion").value= "";
    document.getElementById("quiz").value= "";
    document.getElementById("exam").value= "";
  }

function removeRow() {
    document.getElementById("schedule").deleteRow(-1);
}

function toExcel(type){
  var data = document.getElementById('schedule');
  var excelFile = XLSX.utils.table_to_book(data, {sheet: "sheet1"});
  XLSX.write(excelFile, { bookType: type, bookSST: true, type: 'base64' });
  XLSX.writeFile(excelFile, 'schedule.' + type);
 }