//scores are sent to db at the end of each turn
let throws = [[],[]] //array of two lists of strings to represent throws in turn, ex: [["20", "D19", "B"], ["DB", "D20", "17"]]
//throws[0] = player1's throws, throws[1] = player2

// Player 1 always throws first
let current_player = 0; //player1 = 0, player2 = 1

initial();

function initial() {
    registerImageMap();
    $("#previous-button").click(undo);
    $("#bounceout-button").click( function(e) {
        registerThrow("BO");
    })
}

function registerThrow(user_throw) {
    //alert("Throw: " + user_throw)
    console.log("Throw: " + user_throw)
    throws[current_player].push(user_throw)

    //prepare for next throw
    if(current_player == 0) current_player = 1; //toggle current player
    else current_player = 0;

    if(throws[1].length == 3) {
        sendThrows();
    }
    turnUpdate();
    console.log(throws);
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

function sendThrows() { //send scores to db after both players complete their throws
    alert(JSON.stringify(throws))
    
    //reset variables
    throws = [[],[]]
}

function undo() { //undo last entered score
    //pop the previous player's recent throw
    //toggle current player
    if(throws[0].length != 0) {
        if(current_player == 0) current_player = 1; //toggle current player
        else current_player = 0;

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
}

function updateMatchStats(new_stats) {
    $("#matchStatsDropdown").text(new_stats)
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
        registerThrow("B");
    })
    $(".B").mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard("B");
    })

    $(".DB").click(function(e) {
        e.preventDefault();
        registerThrow("DB");
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
        registerThrow(num);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(num);
    })

    num_class = ".T" + num;
    var t_num = "T" + num;
    $(num_class).click(function(e) {
        e.preventDefault();
        registerThrow(t_num);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(t_num);
    })
    
    num_class = ".D" + num;
    var d_num = "D" + num;
    $(num_class).click(function(e) {
        e.preventDefault();
        registerThrow(d_num);
    })
    $(num_class).mouseover(function(e) {
        e.preventDefault();
        mouseoverBoard(d_num);
    })
}
