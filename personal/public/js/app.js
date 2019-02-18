function seach(){
  val = document.getElementById("value").value
  url = "http://10.86.1.6:5000/getBlock"

  trans = document.getElementById("transaction").checked
  if (val == "")
    return false
  if (trans && val.length == 64){
      url = "http://10.86.1.6:5000/getTransaction"
  }
  else if (val.length == 64)
    url = "http://10.86.1.6:5000/getBlockHash"
  else if (val.length > 26 && val.length < 37)
    url = "http://10.86.1.6:5000/getBlockAddress"
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);
      if (url == "http://10.86.1.6:5000/getBlockHash" || url == "http://10.86.1.6:5000/getBlock")
        block_detail(obj)
      else if (url == "http://10.86.1.6:5000/getTransaction"){
        trans_detail(obj)
      }
      else if (url == "http://10.86.1.6:5000/getBlockAddress"){
        addr_detail(obj)
      }
    }
  };
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("data=" + val);
  return false
}

function appendIndex(){
  var myNode = document.getElementById("root");

  myNode.style.display = "inline";
  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }

  var newLi = document.createElement('input');
  newLi.id = "value"
  newLi.placeholder = "Transaction, address, height, block hash"
  newLi.type = "text"
  myNode.appendChild(newLi)

  var newLi = document.createElement('label');
  var inp = document.createElement('input');
  var spn = document.createElement('span');
  spn.innerHTML = "Transaction"
  inp.className = "with-gap"
  inp.id = "transaction"
  inp.type = "checkbox"
  newLi.appendChild(inp)
  newLi.appendChild(spn)
  myNode.appendChild(newLi)

  var newLi = document.createElement('a');
  newLi.className = "waves-effect waves-light btn"
  newLi.onclick = seach
  newLi.innerHTML = "Search"
  myNode.appendChild(newLi)

  myNode.appendChild(newLi)
}


function block_detail(obj){
  var myNode = document.getElementById("root");

  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }
  if (obj.hasOwnProperty('status')){
    var newLi = document.createElement('h2');
    newLi.innerHTML = "Sorry!!! No data in blockchain"
    newLi.className = "error"
    myNode.appendChild(newLi)
    var newLi = document.createElement('a');
    newLi.className = "waves-effect waves-light btn"
    newLi.onclick = appendIndex
    newLi.innerHTML = "Back"
    myNode.appendChild(newLi)
    return ;
  }
  var newDiv = document.createElement('div');
  newDiv.className = "summory"
  newDiv.innerHTML = "Block Summary:"
  myNode.appendChild(newDiv)
  var newLi = document.createElement('table');

  makeTd("Previous Block Hash", obj['Block Header']['Previous Block Hash'], newLi)
  makeTd("Merkle Root", obj['Block Header']['Merkle Root'], newLi)
  makeTd("Time", new Date(obj['Block Header']['Timestamp'] * 1000), newLi)
  makeTd("Number of transaction", obj['Transaction Counter'], newLi)
  for (var prop in obj['Transaction Data']) {
    tmp = parseInt(prop) + 1
    makeTd("Transaction " + tmp, obj['Transaction Data'][prop], newLi)
  }
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
  if (col1 == "Previous Block Hash"){
    var tmp4 = document.createElement('td');
    let clk = ' onclick="findHash' + "('" + col2 + '\')" '
    tmp4.innerHTML = '<i style="font-size:32px;"'+ clk +'  class="fa fa-search search"></i>'
  }
  else if (col1 == "Transaction 1" || col1 == "Transaction 2" || col1 == "Transaction 3"){
    var tmp4 = document.createElement('td');
    let clk = ' onclick="findTrans' + "('" + col2 + '\')" '
    tmp4.innerHTML = '<i style="font-size:32px;"'+ clk +'  class="fa fa-search search"></i>'
  }
  tmp.appendChild(tmp2)
  tmp.appendChild(tmp3)
  if (col1 == "Previous Block Hash" || col1 == "Transaction 1" || col1 == "Transaction 2" || col1 == "Transaction 3"){
    tmp.appendChild(tmp4)
  }
  newLi.appendChild(tmp)
}

function trans_detail(obj){
  var myNode = document.getElementById("root");

  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }
  if (obj.hasOwnProperty('status')){
    var newLi = document.createElement('h2');
    newLi.innerHTML = "Sorry!!! No data in blockchain"
    newLi.className = "error"
    myNode.appendChild(newLi)
    var newLi = document.createElement('a');
    newLi.className = "waves-effect waves-light btn"
    newLi.onclick = appendIndex
    newLi.innerHTML = "Back"
    myNode.appendChild(newLi)
    return ;
  }

  var newDiv = document.createElement('div');
  newDiv.className = "summory"
  newDiv.innerHTML = "Transaction summary:"
  myNode.appendChild(newDiv)
  var newLi = document.createElement('table');
  makeTd("Vertion", obj['vertion'], newLi)
  makeTd("Locktime", new Date(obj['lock_time'] * 1000), newLi)
  makeTd("Tx_in counter", obj['tx_in count'], newLi)
  for (var prop in obj['tx_in']) {
    makeTd("Previous txid", obj['tx_in'][prop]['Previous txid'], newLi)
    makeTd("Previous Tx Index", obj['tx_in'][prop]['Previous Tx Index'], newLi)
  }
  makeTd("Tx_out counter", obj['tx_out count'], newLi)
  for (var prop in obj['tx_out']) {
    makeTd("Value", obj['tx_out'][prop]['value'], newLi)
    makeTd("Public Script", obj['tx_out'][prop]['Public Script'], newLi)
  }

  myNode.appendChild(newLi)
  var newLi = document.createElement('a');
  newLi.className = "waves-effect waves-light btn"
  newLi.onclick = appendIndex
  newLi.innerHTML = "Back"
  myNode.appendChild(newLi)
}

function findHash(hash){
  url = "http://10.86.1.6:5000/getBlockHash"

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);
      block_detail(obj)
    }
  };
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("data=" + hash);
  return false
}

function findTrans(trans){
  url = "http://10.86.1.6:5000/getTransaction"

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);
      console.log(obj)
      trans_detail(obj)
    }
  };
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("data=" + trans);
  return false
}

function addr_detail(obj){
  var myNode = document.getElementById("root");

  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }
  if (obj.hasOwnProperty('status')){
    var newLi = document.createElement('h2');
    newLi.innerHTML = "Sorry!!! No data in blockchain"
    newLi.className = "error"
    myNode.appendChild(newLi)
    var newLi = document.createElement('a');
    newLi.className = "waves-effect waves-light btn"
    newLi.onclick = appendIndex
    newLi.innerHTML = "Back"
    myNode.appendChild(newLi)
    return ;
  }

  var newDiv = document.createElement('div');
  newDiv.className = "summory"
  newDiv.innerHTML = "Address summary(out only):"
  myNode.appendChild(newDiv)
  var newLi = document.createElement('table');
  for (var prop in obj['out']) {
    makeTd(obj['out'][prop]['addr'], obj['out'][prop]['value'], newLi)
  }
  myNode.appendChild(newLi)
  var newLi = document.createElement('a');
  newLi.className = "waves-effect waves-light btn"
  newLi.onclick = appendIndex
  newLi.innerHTML = "Back"
  myNode.appendChild(newLi)
}
