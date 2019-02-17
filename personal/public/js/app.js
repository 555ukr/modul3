function seach(){
  val = document.getElementById("value").value
  url = "http://localhost:7000/getBlock"
  if (val == "")
    return false
  if (val.length == 64)
    url = "http://localhost:7000/getBlockHash"
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);
      console.log(obj)
      block_detail(obj)
    }
  };
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("data=" + val);
  return false
}

function appendIndex(){
  var myNode = document.getElementById("root");

  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }

  var newLi = document.createElement('input');
  newLi.id = "value"
  newLi.placeholder = "Transaction, address, height"
  newLi.type = "text"
  myNode.appendChild(newLi)

  var newLi = document.createElement('a');
  newLi.className = "waves-effect waves-light btn"
  newLi.onclick = seach
  newLi.innerHTML = "Search"
  myNode.appendChild(newLi)
}


function block_detail(obj){
  var myNode = document.getElementById("root");

  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }
  if (obj.hasOwnProperty('status')){
    var newLi = document.createElement('h2');
    newLi.innerHTML = "Wrong input"
    newLi.className = "error"
    myNode.appendChild(newLi)
    var newLi = document.createElement('a');
    newLi.className = "waves-effect waves-light btn"
    newLi.onclick = appendIndex
    newLi.innerHTML = "Back"
    myNode.appendChild(newLi)
    return ;
  }
  var newLi = document.createElement('table');

  makeTd("Previous Block Hash", obj['Block Header']['Previous Block Hash'], newLi)
  makeTd("Merkle Root", obj['Block Header']['Merkle Root'], newLi)
  makeTd("Time", new Date(obj['Block Header']['Timestamp'] * 1000), newLi)
  makeTd("Number of transaction", obj['Transaction Counter'], newLi)
  makeTd("Nonce", obj['Block Header']['Nonce'], newLi)

  myNode.appendChild(newLi)
  var newLi = document.createElement('a');
  newLi.className = "waves-effect waves-light btn"
  newLi.onclick = appendIndex
  newLi.innerHTML = "Back"
  myNode.appendChild(newLi)
}

function makeTd(col1, col2, newLi){
  var tmp = document.createElement('tr');
  var tmp2 = document.createElement('td');
  tmp2.innerHTML = col1
  var tmp3 = document.createElement('td');
  tmp3.innerHTML = col2
  tmp.appendChild(tmp2)
  tmp.appendChild(tmp3)
  newLi.appendChild(tmp)
}
