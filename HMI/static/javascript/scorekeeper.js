registerImageMap();

function registerThrow(user_throw) {
    alert("Throw: " + user_throw)
}

function mouseoverBoard(board_section) {
    //console.log(board_section)
    $("#score-preview").text(board_section)
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
