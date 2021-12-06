let history = {}
let names = ["", ""]

initial();

async function initial() {
    history = await getMatchList();
}

//The purpose of this function is to call the function getMatches in the server and return a dictionary
function getMatchList(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getMatchesJson');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            //console.log(response)
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
    $("#reviewContainer").empty()
    $("#matchReviewHeader").text("")
    $("#matchReviewSubheader").text("")
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

async function fillDropdown() {

    var dropdown = document.getElementById("MatchDropdown1");
    
    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    console.log(history)
    var matches = Object.keys(history)
    console.log(matches)

    //repopulates the dropdown with the current matches in the database
    for(var key in matches)
    {
        var element = document.createElement("a")
        element.id = matches[key] + "-dropdown"
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeDisplayedMatch('" + matches[key] + "')");
        element.href = "#";
        var node = document.createTextNode(matches[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }
}

function changeDisplayedMatch(id){
    var element = document.getElementById("MatchDrop1");
    element.innerHTML = id

    //update table
    // fill in throw history with server data
    $("#reviewContainer").empty()

    names[0] = history[id]["player1"]
    names[1] = history[id]["player2"]

    $("#matchReviewHeader").text(names[0] + " vs. " + names[1])
    $("#matchReviewSubheader").text(history[id]["date"])

    var throws = history[id]["throws"]
    var sets = throws.length

    //loop through sets, legs, throws to fill in history
    for(var i = 0; i < throws.length; i++) { // set loop
        if(throws[i] != null) {
            for(var j = 0; j < throws[i].length; j++) { // leg loop   
                if(throws[i][j] != null) {
                    temp_length = throws[i][j].length
                    for(var k = 0; k < temp_length; k++) { // turn loop
                        if(k % 2 != 0) { // if on even turn
                            buildTable(throws[i][j][k-1],
                                    throws[i][j][k],
                                    i, j, (k+1)/2, sets);
                        }
                        else {
                            //check for win
                            if(throws[i][j][k]["score"] == 0) {
                                //console.log("leg win " + throws[i][j][k]["player"])

                                var empty = {"throws":["","",""], "score": throws[i][j][k-1]["score"]}

                                if(throws[i][j][k]["player"] == "player1") {
                                    buildTable(throws[i][j][k], empty, i, j, (k/2)+1), sets;
                                }
                                else {
                                    buildTable(empty, throws[i][j][k], i, j, (k/2)+1, sets);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

}

//Following functions copied from scorekeeper.js
//Input: player1 throw data and player2 throw data. runs after both players throw. sets is total number of sets in game
function buildTable(player1, player2, set, leg, turn, sets) {
    //console.log("Build table")
    //console.log(player1)
    //console.log(player2)

    
    //swap player data if out of order
    if(player1["player"] == "player2") {
        let temp = player1
        player1 = player2
        player2 = temp
    }

    newTable(set, leg, turn, sets)
    var id = "tbody" + set + leg + turn;

    for(var i = 0; i < 3; i++) {
        if(player1["throws"].length < i) { //player 1 did not complete 3 throws
            appendTableRow(i+1, "", player2["throws"][i], id);
        }
        else if(player2["throws"].length < i) {  //player 2 did not complete 3 throws
            appendTableRow(i+1, player1["throws"][i], "", id);
        }
        else {
            appendTableRow(i+1, player1["throws"][i], player2["throws"][i], id) ;
        }
    }
    appendTableRow("Final Score", player1["score"], player2["score"], id);
    endTableRow();


    //move table to top of list
    var table = $("#table" + set + leg + turn);
    $("#reviewContainer").prepend(table);

}

//Functions to add content to throw review tables
function newTable(set, leg, turn, sets) {
    var template = document.querySelector("#throw-header")
    var clone = template.content.cloneNode(true)

    var table = clone.querySelector("div")
    table.id = "table" + set + leg + turn

    //add turn header
    var h = clone.querySelector("h4")

    h.textContent = "Set " + (set+1) + ", Leg " + (leg+1) + ", Turn " + turn;


    var th = clone.querySelectorAll("th")
    th[1].textContent = names[0]
    th[2].textContent = names[1]


    var tbody = clone.querySelector("tbody")
    tbody.id = "tbody" + set + leg + turn

    document.querySelector("#reviewContainer").appendChild(clone)
}

function appendTableRow(label, player1, player2, tbody_id) { //tbody_id is "tbody" followed by the set, leg, and turn. ex: "tbody113" for the third turn of first leg of first set
    var template = document.querySelector("#throw-row")
    var clone = template.content.cloneNode(true)
    
    var th = clone.querySelector("th")
    th.textContent = label

    var td = clone.querySelectorAll("td");
    td[0].textContent = player1
    td[1].textContent = player2

    document.querySelector("#" + tbody_id).appendChild(clone)
}

function endTableRow() {
    var template = document.querySelector("#throw-bottom")
    var clone = template.content.cloneNode(true)
    document.querySelector("#reviewContainer").appendChild(clone)
}
