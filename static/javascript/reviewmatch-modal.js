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
    data = {"ReviewMatch":{}}
    data["ReviewMatch"]["NameOfMatch"] = id
    sendData2(data)
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

function togglePlayerDropdown(val){
    if (val != null){
        showPlayer()
    }
    else{
        hidePlayer()
    }

}

//display sets selector for championship play
function showPlayer() {
    $("#ChoosePlayerDropdown4").show();
}

//hide sets selector for normal play
function hidePlayer() {
    $("#ChoosePlayerDropdown4").hide();
}

//The purpose of this function is to call the function getPlayers in the server and return a dictionary
function getPlayersListFromMatch(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayersMatch');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function changeDisplayPlayer(id, num){
    var element = document.getElementById("ChoosePlayerDropdown" + num);
    element.innerHTML = id
}

//Input num (String): The dynamic dropdown number that needs to be changed
//The purpose of this function is to give the dynamic dropdown elements
async function getPlayersFromMatch(num)
{
    //calls to get the players and waits til they are recieved
    window.alert("Working?")
    let players = await getPlayersListFromMatch();

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
        element.setAttribute("onClick","javascript:changeDisplayPlayer('" + players[key] + "','"+ num + "')");
        element.href = "#";
        var node = document.createTextNode(players[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }

}

function sendData2(data) {
    const request = new XMLHttpRequest();
    request.open('POST', '/receiveData');
    request.send(JSON.stringify(data));
}
