//scores are sent to db at the end of each turn
let throws = [[],[]] //array of two lists of strings to represent throws in turn, ex: [["20", "D19", "B"], ["DB", "D20", "17"]]
//throws[0] = player1's throws, throws[1] = player2
let throw_icons = [];

let previous_state = [[],[],[],[]];
let previous_icons = [[],[],[],[]];

// Player 1 always throws first
let current_player = 0; //player1 = 0, player2 = 1
let won = false

let request_data = {"first_read": true}

let last_leg_wins = 0
let loop = true

initial();

async function initial() {
    registerImageMap();
    $("#previous-button").click(undo);
    $("#bounceout-button").click( function(e) {
        registerThrow("BO");
    })
    $("#nextturn-button").click( function(e) {
        nextTurn();
    })

    while(loop) {
        received = false;
        // sync with server
        let game_data = await requestGameState();

        if(Object.keys(game_data).length === 0) {
            //alert("no game");
            //TODO: popup that prompts return to home screen
            $("#noGameModal").modal("show");
            won = true;
        }
        else {
            //console.log(JSON.stringify(game_data["throwHistory"]))
            
            // fill in throw history with server data

            $("#reviewThrows").empty()

            var current_set = game_data["game"]["current_set"]

            for(var i = 0; i < current_set+1; i++) { // set loop
                if(game_data["throwHistory"][i] != null) {
                    for(var j = 0; j < game_data["throwHistory"][i].length; j++) { // leg loop   
                        if(game_data["throwHistory"][i][j] != null) {
                            temp_length = game_data["throwHistory"][i][j].length
                            for(var k = 0; k < temp_length; k++) { // turn loop
                                //console.log(temp_length)
                                if(k % 2 != 0) {
                                    buildTable(game_data["throwHistory"][i][j][k-1],
                                            game_data["throwHistory"][i][j][k],
                                            i, j, (k+1)/2);
                                }
                                else {
                                    //check for win
                                    if(game_data["throwHistory"][i][j][k]["score"] == 0) {
                                        console.log("leg win " + game_data["throwHistory"][i][j][k]["player"])

                                        var empty = {"throws":["","",""], "score": game_data["throwHistory"][i][j][k-1]["score"]}

                                        if(game_data["throwHistory"][i][j][k]["player"] == "player1") {
                                            buildTable(game_data["throwHistory"][i][j][k], empty, i, j, (k/2)+1);
                                        }
                                        else {
                                            buildTable(empty, game_data["throwHistory"][i][j][k], i, j, (k/2)+1);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // if turn is out of sync or a new leg has begun
        if(current_player != game_data["game"]["current_turn"] || last_leg_wins != game_data["player1"]["legsWon"] + game_data["player2"]["legsWon"]) {
            current_player = game_data["game"]["current_turn"]
            throws = [[],[]]
            throw_icons = [];
            previous_state = [[],[],[],[]];
            previous_icons = [[],[],[],[]];
            turnUpdate();
        }
        received = true;
        last_leg_wins = game_data["player1"]["legsWon"] + game_data["player2"]["legsWon"]
    }
}

function sendData(data) {
    const request = new XMLHttpRequest();
    request.open('POST', '/receiveData');
    request.send(JSON.stringify(data));
}

function registerThrow(user_throw, e) {
    if(throws[current_player].length < 3 && !won) {

        if(e != undefined) {
            var sidebar_width = $("#side-menu").outerWidth();
            var header_height = $("#header").height();

            //alert("clientX: " + (e.clientX-sidebar_width) + " - clientY: " + (e.clientY - header_height))
            //alert("Throw: " + user_throw)
            var new_icon = document.createElement("div");
            new_icon.className = "throw-icon";
            new_icon.style.left = e.clientX-sidebar_width-7.5;
            new_icon.style.top = e.clientY - header_height-7.5;

            previous_icons[throws[current_player].length] = throw_icons.slice(0);

            $("#throw-icon-container").append(new_icon);
            throw_icons.push(new_icon);
        }
        else {
            previous_icons[throws[current_player].length] = throw_icons.slice(0);
            throw_icons.push(undefined);
        }
        previous_state[throws[current_player].length] = throws[current_player].slice(0);
        //console.log(previous_state)

        //console.log("Throw: " + user_throw)
        throws[current_player].push(user_throw);

        //update throw display
        throwDisplayUpdate();

        //prepare for next throw
        if(throws[current_player].length < 3)
            turnUpdate();
        //console.log(throws);
    }
    if(throws[current_player].length == 3) {
        //console.log("remove disabled")
        $("#nextturn-button").removeClass("disabled")
    }
}

function throwDisplayUpdate() {
    let t = throws[current_player];
    

    if(t.length == 0) {
        
        $("#throwsDisplayHeader").css("display", "none");
    }
    else {
        $("#throwsDisplayHeader").css("display", "block");
    }

    let text = t.join(", ");
    console.log(text)
    $("#throwsDisplay").text(text);
}

function nextTurn() {
    if(throws[current_player].length == 3) {
        $("#throw-icon-container").empty();
        $("#nextturn-button").addClass("disabled")
        sendThrow();   
    }
}

function turnUpdate() {
    var label_str = "Player " + (current_player + 1) + ", Throw " + (throws[current_player].length + 1);
    $("#player-label").text(label_str);

    if(throws[current_player].length < 3) {
        $("#nextturn-button").addClass("disabled")
    } //re-disable next turn button

    //update knock out dropdown for next player
    $("#knockoutDropdownContainer").empty();

    for(let i = 0; i < throws[current_player].length; i++) {
        var element = document.createElement("a");
        element.className = "dropdown-item";
        element.textContent = "Throw " + (i + 1) + ": " + throws[current_player][i];
        element.href = "javascript:knockOut(" + i + ")";
        $("#knockoutDropdownContainer").append(element)
    }

}

function mouseoverBoard(board_section) {
    //console.log(board_section)
    $("#score-preview").text(board_section)
}

function sendThrow() { //send scores to server after one player completes their throws
    //alert(JSON.stringify(throws[current_player]))

    data = {"throws":{}}
    if(current_player == 0) {
        data["throws"]["player1"] = throws[current_player]
    }
    else {
        data["throws"]["player2"] = throws[current_player]
    }
    
    sendData(data);
    //reset variables

}

function undo() { //undo last entered score
    //pop the previous player's recent throw
    if(throws[current_player].length != 0) {

        throw_icons = previous_icons[throws[current_player].length-1].slice(0);
        //let icon = throw_icons.pop();
        //if(icon != undefined)
        //    icon.remove();
        $("#throw-icon-container").empty();
        throw_icons.forEach(icon => $("#throw-icon-container").append(icon));
               
        throws[current_player] = previous_state[throws[current_player].length-1].slice(0);

        //reupdate throw display
        throwDisplayUpdate();

        turnUpdate();
        //console.log(throws)
    }
}

function knockOut(throw_num) { //replace throw at throw_num with 0 to represent knocked out dart
    console.log("knock out")
    throws[current_player][throw_num] = "KO";
    icon = throw_icons[throw_num];
    if(icon != undefined)
        icon.remove();
    throw_icons[throw_num] = undefined;
    
    //disable dropdown after knockOut set (reset after throw)
}

// Update displayed stats on scoreboard. new_stats is string representing the stat to be displayed
function updatePlayerStats(new_stats) {
    $("#matchStatsDropdown").text(new_stats)
    data = {"new_match_stats": new_stats}
    sendData(data)
}

function updateMatchStats(new_stats) {
    $("#leagueStatsDropdown").text(new_stats)
    data = {"new_league_stats": new_stats}
    sendData(data)
}

function requestGameState() {
    const request = new XMLHttpRequest();
    request.open('POST', '/updateScoreboard');
    request.send(JSON.stringify(request_data));
    return new Promise((resolve) => {
        request.onload = () => {
            request_data["first_read"] = false;
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

//Input: player1 throw data and player2 throw data. runs after both players throw
function buildTable(player1, player2, set, leg, turn) {
    console.log("Build table")
    console.log(player1)
    console.log(player2)

    newTable(set, leg, turn)
    var id = "tbody" + set + leg + turn

    for(var i = 0; i < 3; i++) {
        if(player1["throws"].length < i) { //player 1 did not complete 3 throws
            appendTableRow(i+1, "", player2["throws"][i], id)
        }
        else if(player2["throws"].length < i) {  //player 2 did not complete 3 throws
            appendTableRow(i+1, player1["throws"][i], "", id)
        }
        else {
            appendTableRow(i+1, player1["throws"][i], player2["throws"][i], id) 
        }
    }
    appendTableRow("Final Score", player1["score"], player2["score"], id)
    endTableRow()
    //newTable()
}

//Functions to add content to throw review tables
function newTable(set, leg, turn) {
    var template = document.querySelector("#throw-header")
    var clone = template.content.cloneNode(true)

    //add turn header
    var h = clone.querySelector("h4")
    h.textContent = "Set " + set + ", Leg " + leg + ", Turn " + turn;

    var tbody = clone.querySelector("tbody")
    tbody.id = "tbody" + set + leg + turn

    document.querySelector("#reviewThrows").appendChild(clone)
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
    document.querySelector("#reviewThrows").appendChild(clone)
}

function registerImageMap() { //register events for the entire board
    for(let i = 1; i <= 20; i++) {
        registerNum(i)
    }

    $(".B").click(function(e) {
        e.preventDefault();
        registerThrow("B", e);
    })
    $(".B").mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard("B");
    })

    $(".DB").click(function(e) {
        e.preventDefault();
        registerThrow("DB", e);
    })
    $(".DB").mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard("DB");
    })
}

function registerNum(num) { //register onclick events for one section of the board
    var num_class = "." + num;
    $(num_class).click(function(e) {
        e.preventDefault();
        registerThrow(num, e);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(num);
    })

    num_class = ".T" + num;
    var t_num = "T" + num;
    $(num_class).click(function(e) {
        e.preventDefault();
        registerThrow(t_num, e);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(t_num);
    })
    
    num_class = ".D" + num;
    var d_num = "D" + num;
    $(num_class).click(function(e) {
        e.preventDefault();
        registerThrow(d_num, e);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(d_num);
    })
}
