//The purpose of this function is to call the function getMatches in the server and return a dictionary
function getMatchList(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getMatches');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function changeDisplay(id, num){
    var element = document.getElementById("MatchDrop" + num);
    element.innerHTML = id
}

function resetReviewMatch(){
    document.getElementById("MatchDrop1").innerHTML = "Choose Match"
}

async function getMatch(num)
{
    //calls to get the players and waits til they are recieved
    let match = await getMatchList();

    var dropdown = document.getElementById("MatchDropdown" + num);

    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    //repopulates the dropdown with the current players in the database
    for(var key in match)
    {
        var element = document.createElement("a")
        element.id = match[key] + "-dropdown"
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeDisplay('" + match[key] + "','"+ num + "')");
        element.href = "#";
        var node = document.createTextNode(match[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }

}

//The purpose of this function is to call the function getPlayers in the server and return a dictionary
function getMatchInformation(MatchName){
    const request = new XMLHttpRequest();
    request.open('POST', '/getMatchInformation');
    data = {matchname: MatchName}
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    }); 
}


async function displaySelectPlayerTable(){
    //table initialize
    var insertTable = document.getElementById("ReviewMatch-ModalBody");
    var footer = document.getElementById("ReviewMatch-ModalFooter")
    var table = document.createElement("table")
    table.id = "TABLE-HEAD"
    var tablehead = document.createElement("thead")
    var tablebody = document.createElement("tbody")
    var tr = document.createElement("tr")
    var MatchName = document.getElementById("MatchDrop1").innerHTML;
    

    //Check to see if  has been chosen
    if(MatchName.trim() == "Choose Match")
    {
        var notification = document.getElementById("NotificationModal");
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Match is not in System";
        $(notification).modal('toggle');
        return
    }


    data = {matchname: MatchName}

    
    var information = await getMatchInformation(data["matchname"])

    //creates the headers of the table
    var tr = document.createElement("tr")
    tr.classList.add("d-flex")
    for(var key in information)
    {
        if(key == "id")
            continue
        var element = document.createElement("th")
        element.id = key + "-col"
        element.classList.add("col")
        var node = document.createTextNode(key)
        element.appendChild(node)
        tr.appendChild(element)
        tablehead.appendChild(tr)
    }


    //creates the rows of the table
    var tr = document.createElement("tr")
    tr.classList.add("d-flex")
    window.alert(information)
    for(key in information)
    {
        if(key == "id")
            continue
        var input = document.createElement("input")
        input.value = information[key]
        input.id = key + "-row"
        key = key.trim()
        if(key == "Player"){
            input.setAttribute("type","text")
        }
        else{
            input.setAttribute("type", "number")
        }
        input.classList.add("form-control")
        var element = document.createElement("td")
        element.classList.add("col")
        element.appendChild(input)
        tr.appendChild(element)
        tablebody.appendChild(tr)

    }
    //append the information to table
    table.appendChild(tablehead)
    table.appendChild(tablebody)

    //table features
    table.classList.add("table")
    table.classList.add("table-dark")

    //location of table
    insertTable.insertBefore(table, footer);
}

function resetReviewPlayer(){
    review = document.getElementById("Review-Button")
    review.innerHTML = "Review Match"
    review.setAttribute("onClick", "javascript:displaySelectPlayerTable()")
    document.getElementById("MatchDrop1").innerHTML = "Choose Match"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }

}