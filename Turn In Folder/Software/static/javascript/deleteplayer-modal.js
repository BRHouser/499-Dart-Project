//Contains all functions for delete player modal
//Author: Marshall Rosenhoover
//Created 10/18/21

//The purpose of this function is to call the function getPlayers in the server and return a dictionary
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

//Input id (String): Name of the Player
//Input num (String): The dynamic dropdown number that needs to be changed
//The purpose of this function is to change the name of the dynamic dropdown display name of the given dropdown
function changeDisplayName(id, num){
    var element = document.getElementById("ChoosePlayerDropdown" + num);
    element.innerHTML = id
}

//Input name (String): the name of the dynamic dropdown to change
//The purpose of this function is to reset the dynamic dropdown to its original display
function resetDynamicDropdown(name){
    document.getElementById(name).innerHTML = "CHOOSE PLAYER"
}


//Input num (String): The dynamic dropdown number that needs to be changed
//The purpose of this function is to call deletePlayer in the server 
function deletePlayer(num){
    //Get Player name
    var playerName = document.getElementById("ChoosePlayerDropdown" + num ).innerHTML;
    
    //Check to see if player has been chosen, if player has not been chosen then display error in notification modal
    if(playerName.trim() == "CHOOSE PLAYER")
    {
        var notification = document.getElementById("NotificationModal");
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player is not in System";
        $(notification).modal('toggle');
        return
    }

    //calls the server
    const request = new XMLHttpRequest();
    request.open("POST", '/deletePlayer');
    playerName = playerName.split(" ");
    data = {firstname : playerName[0], lastname: playerName[1]}
    request.send(JSON.stringify(data));

    //resets the dropdown
    resetDynamicDropdown("ChoosePlayerDropdown" + num)
}

//Input num (String): The dynamic dropdown number that needs to be changed
//The purpose of this function is to give the dynamic dropdown elements
async function getPlayers(num)
{
    //calls to get the players and waits til they are recieved
    let players = await getPlayersList();

    var dropdown = document.getElementById("dynamic-dropdown" + num);

    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    //repopulates the dropdown with the current players in the database
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