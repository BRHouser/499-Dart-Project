function getPlayersList(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayers');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function changeDisplayName(id, num){
    var element = document.getElementById("ChoosePlayerDropdown" + num);
    element.innerHTML = id
}

function deletePlayer(num){
    var playerName = document.getElementById("ChoosePlayerDropdown" + num ).innerHTML;
    
    if(playerName.trim() == "CHOOSE PLAYER")
    {
        var notification = document.getElementById("NotificationModal");
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player is not in System";
        $(notification).modal('toggle');
        return
    }
    const request = new XMLHttpRequest();
    request.open("POST", '/deletePlayer');
    playerName = playerName.split(" ");
    data = {firstname : playerName[0], lastname: playerName[1]}
    request.send(JSON.stringify(data));
    document.getElementById("ChoosePlayerDropdown" + num).innerHTML = "CHOOSE PLAYER"
}

async function getPlayers(num)
{
    let players = await getPlayersList();
    var dropdown = document.getElementById("dynamic-dropdown" + num);

    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    for(var key in players)
    {
        var element = document.createElement("a")
        element.id = players[key] + "-dropdown"
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeDisplayName('" + players[key] + "','"+ num + "')");
        element.href = "#";
        var node = document.createTextNode(players[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }

}