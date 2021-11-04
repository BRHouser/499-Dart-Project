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
