
function getPlayerInformation(firstName, lastName){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayerInformation');
    data = {firstname: firstName, lastname: lastName}
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });  
}

async function displayEditTable(){

    var insertTable = document.getElementById("editPlayer-ModalBody");
    var footer = document.getElementById("editPlayer-ModalFooter")
    var table = document.createElement("table")
    var tablehead = document.createElement("thead")
    var tablebody = document.createElement("tbody")
    var tr = document.createElement("tr")

    var playerName = document.getElementById("ChoosePlayerDropdown1").innerHTML;
    
    if(playerName.trim() == "CHOOSE PLAYER")
    {
        var notification = document.getElementById("NotificationModal");
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player is not in System";
        $(notification).modal('toggle');
        return
    }

    playerName = playerName.split(" ");
    data = {firstname : playerName[0], lastname: playerName[1]}
    var information = await getPlayerInformation(data["firstname"], data["lastname"])


    var tr = document.createElement("tr")
    for(var key in information)
    {
        var element = document.createElement("th")
        element.id = information[key] + "-col"
        element.scope = "col-sm"
        var node = document.createTextNode(key)
        element.appendChild(node)
        tr.appendChild(element)
        tablehead.appendChild(tr)

    }
    var tr = document.createElement("tr")
    x = 0
    for(var key in information)
    {
        var input = document.createElement("input") 
        input.setAttribute("placeholder", 5)
        input.setAttribute("type", "text")
        input.classList.add("form-control")
        if(x == 0)
        {
            var element = document.createElement("th")
            element.scope = "row" 
            x = 5
        }
        else
            var element = document.createElement("td")
        element.appendChild(input)
        tr.appendChild(element)
        tablebody.appendChild(tr)
    }

    table.appendChild(tablehead)
    table.appendChild(tablebody)
    table.classList.add("table")
    table.classList.add("table-dark")
    insertTable.insertBefore(table, footer);


}