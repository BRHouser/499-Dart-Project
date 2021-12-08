//Contains all functions for add player modal
//Author: Marshall Rosenhoover
//Created 10/11/21, edited 11/30/21

//Input FirstName (String): The first name of the Player
//Input LastName (String): The last name of the Player
//The purpose of this function is to add the changed player in the database by calling the server function addPlayer
async function addPlayer(FirstName, LastName)
{
    data = {firstname: FirstName, lastname: LastName, LastWin: 'None', Average_League_Score: 0, Lifetime_180s: 0, Number_of_wins: 0}
    const request = new XMLHttpRequest();
    request.open('POST', '/addPlayer');
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = request.responseText;
            resolve(response);
        }; 
    });
}


//The purpose of this function is to call the function getPlayers in the server and return a dictionary
function getPlayersListForAddPlayer(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayers');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}
//The purpose of this function is to reset the elements in the addplayer modal
function resetAddPlayer()
{
    document.getElementById("FirstName").value = "";
    document.getElementById("LastName").value = "";
}


//The purpose of this function is to check to see if the input is correct within addplayer, and if it is
//then submit the information to be added to the database by calling the function addPlayer
async function closeModal(){
    //Variable initialize
    submit = true;
    var popup = document.getElementById('AddPlayerModal');
    var notification = document.getElementById("NotificationModal");
    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;

    //Checks to see if the firstname is valid
    if(FirstName.trim() == "")
    {
        submit = false;
        resetAddPlayer();                
        document.getElementById('ErrorText').innerHTML = "Invalid Input: First Name";
        $(notification).modal('toggle');
        return
    }

    //Checks to see if the lastname is valid
    if(LastName.trim() == "")
    {
        submit = false;
        resetAddPlayer();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Last Name";
        $(notification).modal('toggle');
        return
    }

    //if everything is correct then submit the information
    if(submit)
    {
        //checks to see if player is already in system
        //if not then add player
        let response = await addPlayer(FirstName, LastName);
        if(response == "True")
        {
            resetAddPlayer();
            $(popup).modal('toggle');
        }
        else //if player is in system throw notification
        {
            resetAddPlayer();
            document.getElementById('ErrorText').innerHTML = "Player is already in system";
            $(notification).modal('toggle');
        }
    }
}
