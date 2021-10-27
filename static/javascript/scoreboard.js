//game data: json object following this scheme:

let example_game_data = {
    "player1": {
        "score": "301",
        "leagueStats": "League Win Rate: 50%",
        "matchStats": "T20s in Match: 2",
        "perfectLeg": true,
        "possibleOuts": ""
    },
    "player2": {
        "score": "301",
        "leagueStats": "League Win Rate: 50%",
        "matchStats": "T20s in Match: 2",
        "perfectLeg": true,
        "possibleOuts": ""
    }
}

updateGameState();

async function updateGameState() {
    let game_data = await requestGameState();

    let player1 = game_data["player1"]
    $("#p1-score").text(player1["score"]);
    $("#p1-league-stats").text(player1["leagueStats"]);
    $("#p1-match-stats").text(player1["matchStats"]);
    $("#p1-outs").text(player1["possibleOuts"]);

    let player2 = game_data["player2"]
    $("#p2-score").text(player2["score"]);
    $("#p2-league-stats").text(player2["leagueStats"]);
    $("#p2-match-stats").text(player2["matchStats"]);
    $("#p2-outs").text(player2["possibleOuts"]);
}

function requestGameState() {
    const request = new XMLHttpRequest();
    request.open('POST', '/updateScoreboard');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function winState(player) {
    
}
