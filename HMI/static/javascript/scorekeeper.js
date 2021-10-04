registerImageMap();

function registerThrow(user_throw) {
    //alert("Throw: " + user_throw)
    console.log("Throw: " + user_throw)
}

function mouseoverBoard(board_section) {
    //console.log(board_section)
    $("#score-preview").text(board_section)
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
