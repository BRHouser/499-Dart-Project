 //Input firstname (String): The first name of the Player
//Input lastname (String): The last name of the Player
//Ouput dictionary of the table of specified person
//The purpose of this function is to call getPlayerStatistics in the server
function getPlayerInformation(firstName, lastName){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayerStatistics');
    data = {firstname: firstName, lastname: lastName}
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });  
}

//The purpose of this function is to call the function getPlayers in the server and return a dictionary
function getPlayersListForEditPlayer(){
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

//The purpose of this function is to delete the changed player in the database by calling server function deletePlayer
function deleteChange(){
    var old_name = document.getElementById("ChoosePlayerDropdown1").innerHTML.trim()
    old_name = old_name.split(" ")
    data = {firstname: old_name[0], lastname: old_name[1]}
    const request = new XMLHttpRequest();
    request.open("POST", "/deletePlayer")
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = request.responseText;
            resolve(response);
        }; 
    }); 
}

//Input firstname (String): The first name of the Player
//Input lastname (String): The last name of the Player
//The purpose of this function is to add the changed player in the database by calling the server function addPlayer
function addChange(firstname, lastname, leaguerank, lastwin, averageLeagueScore, lifetime_180s, Number_of_wins){

    data = {firstname: firstname, lastname: lastname, LeagueRank: leaguerank, LastWin: lastwin, Average_League_Score: averageLeagueScore, Lifetime_180s: lifetime_180s, Number_of_wins: Number_of_wins}
    const request = new XMLHttpRequest();
    request.open("POST", "/addPlayer")
    request.send(JSON.stringify(data))
    return new Promise((resolve) => {
        request.onload = () => {
            const response = request.responseText;
            resolve(response);
        }; 
    }); 
}


//Submit Button changes will call deleteChange and addChange to edit player information
//addChange will not be called until deleteChange is completed
async function submitPlayerChanges(){	    
    var new_firstname = document.getElementById("First_Name-row").value
    var new_lastname = document.getElementById("Last_Name-row").value
    var new_LeagueRank = document.getElementById("League_Rank-row").value
    var new_Last_Win = document.getElementById("Last_Win-row").value
    var new_Average_League_Score = document.getElementById("Average_League_Score-row").value
    var new_Lifetime_180s = document.getElementById("Lifetime_180s-row").value
    var new_Number_of_wins = document.getElementById("Number_of_Wins-row").value
    var notification = document.getElementById("NotificationModal");


    //Checks to see if Information is valid
    if(new_firstname.trim() == "")
    {
        document.getElementById('ErrorText').innerHTML = "Invalid Input: First Name";
        $(notification).modal('toggle');
        return
    }
    if(new_lastname.trim() == "")
    {
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Last Name";
        $(notification).modal('toggle');
        return
    }
    let player_list = await getPlayersListForEditPlayer()
    var old_name = document.getElementById("ChoosePlayerDropdown1").innerHTML.trim()
    if(old_name != new_firstname + " " + new_lastname)
    {    
        for(var key in player_list)
        {
            if(new_firstname + " " + new_lastname == player_list[key]){
                document.getElementById('ErrorText').innerHTML = "Invalid Input: Name Taken";
                $(notification).modal('toggle');
                return
            }
        }
    }

    //if input is valid then save the changed values
    //var button = document.getElementById("Submit-Button")

    button.innerHTML = "Edit Player"
    button.setAttribute("onClick", "javascript:displayEditTable()")
    if(new_Number_of_wins == 0)
        new_Number_of_wins = "None"
    if(new_Average_League_Score == 0)
        new_Average_League_Score = "None"
    if(new_LeagueRank == 0)
        new_LeagueRank = "None"
    
    var popup = document.getElementById('EditPlayerModal');
    $(popup).modal('toggle');
    await deleteChange()
    await addChange(new_firstname, new_lastname, new_LeagueRank, new_Last_Win, new_Average_League_Score, new_Lifetime_180s, new_Number_of_wins)
    resetEditPlayer()

}


function resetEditPlayer(){
    button.innerHTML = "Edit Player"
    button.setAttribute("onClick", "javascript:displayEditTable()")
    document.getElementById("ChoosePlayerDropdown1").innerHTML = "CHOOSE PLAYER"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }

}



var button = document.getElementById("Edit-Button")

//The purpose of this function is to display Player information in table
async function displayEditTable(){
    //table initialize
    var insertTable = document.getElementById("editPlayer-ModalBody");
    var footer = document.getElementById("editPlayer-ModalFooter")
    var table = document.createElement("table")
    table.id = "TABLE-HEAD"
    var tablehead = document.createElement("thead")
    var tablebody = document.createElement("tbody")
    var tr = document.createElement("tr")
    var playerName = document.getElementById("ChoosePlayerDropdown1").innerHTML;
    

    //Check to see if Player has been chosen
    if(playerName.trim() == "CHOOSE PLAYER")
    {
        var notification = document.getElementById("NotificationModal");
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player is not in System";
        $(notification).modal('toggle');
        return
    }


    playerName = playerName.split(" ");
    data = {firstname : playerName[0], lastname: playerName[1]}

    //calls the getPlayerInformation to get specified player information for table
    var information = await getPlayerInformation(data["firstname"], data["lastname"])

    //creates the headers of the table
    var tr = document.createElement("tr")
    tr.classList.add("d-flex")
    for(var key in information)
    {
        if(key == "id")
            continue
        var element = document.createElement("th")
        element.id = key + "-col"
        element.classList.add("col")
        var node = document.createTextNode(key)
        element.appendChild(node)
        tr.appendChild(element)
        tablehead.appendChild(tr)
    }


    //creates the rows of the table
    var tr = document.createElement("tr")
    tr.classList.add("d-flex")
    for(var key in information)
    {
        if(key == "id")
            continue
        var input = document.createElement("input") 
        input.value = information[key]
        input.id = key + "-row"
        key = key.trim()
        if(key == 'League_Rank' || key == 'Average_League_Score' || key == 'Lifetime_180s' || key == 'Number_of_Wins')
            input.setAttribute("type", "number")
        else
            input.setAttribute("type", "text")
        input.classList.add("form-control")
        var element = document.createElement("td")
        element.classList.add("col")
        element.appendChild(input)
        tr.appendChild(element)
        tablebody.appendChild(tr)

    }
    //append the information to table
    table.appendChild(tablehead)
    table.appendChild(tablebody)

    //table features
    table.classList.add("table")
    table.classList.add("table-dark")

    //location of table
    insertTable.insertBefore(table, footer);


    //changes edit player button to submit button
    button = document.getElementById("Edit-Button")
    button.innerHTML = "Submit"
    button.setAttribute("onClick", "javascript:submitPlayerChanges()")
}