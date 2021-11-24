let data = {"first_read": true}
let current_game = false
initial()

//check for current_game_state
async function initial() {
    let game_data = await requestGameState();
    if(Object.keys(game_data).length != 0) { // if current game data exists
        var element = document.getElementById("ResumeGame");
        element.classList.remove("disabled"); //remove disabled class from button
        current_game = true
    }
}

function requestGameState() { //request gamestate from server (server returns empty {} object if no current game)
    const request = new XMLHttpRequest();
    request.open('POST', '/updateScoreboard');
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            //data["first_read"] = false;
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function resumeGame() {
    if(current_game) {
        console.log("resume")
        window.open("/scorekeeper", '_blank').focus();
        window.open("/scoreboard", '_blank').focus();
    }
}