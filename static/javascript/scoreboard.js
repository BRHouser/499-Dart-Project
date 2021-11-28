//game data: json object following this scheme:

let won = false;
let received = false;

let data = {"first_read": true}

mainLoop();

async function mainLoop() {
    while(!won) {
        await updateGameState();
    }
}

async function updateGameState() {
    received = false;
    let game_data = await requestGameState();

    if(Object.keys(game_data).length != 0) {
        //TODO: display match location, date, and game info in header

        let player1 = game_data["player1"]
        $("#p1-score").text(player1["score"]);
        $('#p1-legs-won').text("Legs: " + player1["legsWon"] + " / " +  game_data["game"]["legs"] + ", Sets: " + player1["setsWon"] + " / " + game_data["game"]["sets"])
        $("#p1-league-stats").text(player1["leagueStats"]);
        $("#p1-match-stats").text(player1["matchStats"]);
        $("#p1-outs").text(player1["possibleOuts"]);
        $("#p1-name").text(player1["name"]);
        if(player1["perfectLeg"]) {
            $("#p1-perfect-leg").text("On track for perfect leg");
        }
        else {
            $("#p1-perfect-leg").text("");
        }

        let player2 = game_data["player2"]
        $("#p2-score").text(player2["score"]);
        $('#p2-legs-won').text("Legs: " + player2["legsWon"] + " / " +  game_data["game"]["legs"] + ", Sets: " + player2["setsWon"] + " / " + game_data["game"]["sets"])
        $("#p2-league-stats").text(player2["leagueStats"]);
        $("#p2-match-stats").text(player2["matchStats"]);
        $("#p2-outs").text(player2["possibleOuts"]);
        $("#p2-name").text(player2["name"]);
        if(player2["perfectLeg"]) {
            $("#p2-perfect-leg").text("On track for perfect leg");
        }
        else {
            $("#p2-perfect-leg").text("");
        }

        $("#main-header").text(player1["name"] + " vs. " + player2["name"])
        //$("#leg-header").text("Best of " + game_data["game"]["legs"] + "legs")
        //$("#set-header").text("Best of " + game_data["game"]["sets"] + "sets")

        if(game_data["game"]["current_turn"] == 0) {
            $("#p1-throwing").text("Now throwing")
            $("#p2-throwing").text("")
        }
        else {
            $("#p2-throwing").text("Now throwing")
            $("#p1-throwing").text("")
        }

        if(game_data["game"]["won"]) {
            //alert(game_data["game"]["winner"])
            let winner = game_data["game"]["winner"]

            $("#p1-score").text("");
            $('#p1-legs-won').text("");
            $("#p1-league-stats").text("");
            $("#p1-match-stats").text("");
            $("#p1-outs").text("");
            $("#p1-perfect-leg").text("");
            $("#p1-throwing").text("");
            
            $("#p2-score").text("");
            $('#p2-legs-won').text("");
            $("#p2-league-stats").text("");
            $("#p2-match-stats").text("");
            $("#p2-outs").text("");
            $("#p2-perfect-leg").text("");
            $("#p2-throwing").text("");


            if(winner == "player1") {
                $("#p1-score").text("Win!");
            }
            else {
                $("#p2-score").text("Win!");
            }

        }
        
    }
    received = true
}

function requestGameState() {
    const request = new XMLHttpRequest();
    request.open('POST', '/updateScoreboard');
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            data["first_read"] = false;
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function winState(player) {
    
}
