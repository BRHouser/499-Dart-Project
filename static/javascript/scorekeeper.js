//scores are sent to db at the end of each turn
let throws = [[],[]] //array of two lists of strings to represent throws in turn, ex: [["20", "D19", "B"], ["DB", "D20", "17"]]
//throws[0] = player1's throws, throws[1] = player2
let throw_icons = [];

// Player 1 always throws first
let current_player = 0; //player1 = 0, player2 = 1

initial();

function initial() {
    registerImageMap();
    $("#previous-button").click(undo);
    $("#bounceout-button").click( function(e) {
        registerThrow("BO");
    })
    $("#nextturn-button").click( function(e) {
        nextTurn();
    })
}

function sendData(data) {
    const request = new XMLHttpRequest();
    request.open('POST', '/receiveData');
    request.send(JSON.stringify(data));
}

function registerThrow(user_throw, e) {
    if(throws[current_player].length < 3) {

        if(e != undefined) {
            var sidebar_width = $("#side-menu").outerWidth();
            var header_height = $("#header").height();

            //alert("clientX: " + (e.clientX-sidebar_width) + " - clientY: " + (e.clientY - header_height))
            //alert("Throw: " + user_throw)
            var new_icon = document.createElement("div");
            new_icon.className = "throw-icon";
            new_icon.style.left = e.clientX-sidebar_width-7.5;
            new_icon.style.top = e.clientY - header_height-7.5;

            $("#throw-icon-container").append(new_icon);
            throw_icons.push(new_icon);
        }
        else {
            throw_icons.push(undefined);
        }
        console.log("Throw: " + user_throw)
        throws[current_player].push(user_throw)

        //prepare for next throw
        if(throws[current_player].length < 3)
            turnUpdate();
        console.log(throws);
    }
}

function nextTurn() {
    if(throws[current_player].length == 3) {
        $("#throw-icon-container").empty();
        sendThrow();
        if(current_player == 0) current_player = 1; //toggle current player
        else current_player = 0;
        turnUpdate();        
    }
}

function turnUpdate() {
    var label_str = "Player " + (current_player + 1) + ", Throw " + (throws[current_player].length + 1);
    $("#player-label").text(label_str);

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
    throws = [[],[]]
}

function undo() { //undo last entered score
    //pop the previous player's recent throw
    //toggle current player
    if(throws[current_player].length != 0) {

        let icon = throw_icons.pop();
        if(icon != undefined)
            icon.remove();
        throws[current_player].pop();
        turnUpdate();
        console.log(throws)
    }
}

function knockOut(throw_num) { //replace throw at throw_num with 0 to represent knocked out dart
    console.log("knock out")
    throws[current_player][throw_num] = "KO";
    //disable dropdown after knockOut set (reset after throw)
}

// Update displayed stats on scoreboard. new_stats is string representing the stat to be displayed
function updatePlayerStats(new_stats) {
    $("#playerStatsDropdown").text(new_stats)
    data = {"new_league_stats": new_stats}
    sendData(data)
}

function updateMatchStats(new_stats) {
    $("#matchStatsDropdown").text(new_stats)
    data = {"new_match_stats": new_stats}
    sendData(data)
}

//Functions to add content to throw review tables
function newTable(leg, turn) {
    var template = document.querySelector("#throw-header")
    var clone = template.content.cloneNode(true)

    //add turn header
    var b = clone.querySelector("b")
    b.textContent = "Turn " + turn;
    if(leg != null) {
        var b = clone.querySelector("h4")
        b.textContent = "Leg " + leg;
    }

    var tbody = clone.querySelector("tbody")
    tbody.id = "tbody" + leg + turn

    document.querySelector("#reviewThrows").appendChild(clone)
}

function appendTableRow(label, player1, player2, tbody_id) { //tbody_id is "tbody" followed by the leg and turn. ex: "tbody13" for the third throw of first turn
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
