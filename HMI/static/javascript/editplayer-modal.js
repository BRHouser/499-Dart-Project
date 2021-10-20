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
//Input throws (String): The total number of thrown darts by the player
//Input bullseyes (String): The total number of bullseyes by the player
//The purpose of this function is to add the changed player in the database by calling the server function addPlayer
function addChange(firstname, lastname, throws, bullseyes){

    data = {firstname: firstname, lastname: lastname, totalthrows: throws.toString(), totalbullseyes: bullseyes.toString()}
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
    var new_totalthrows = document.getElementById("Total_Number_of_Throws-row").value
    var new_totalbullseyes = document.getElementById("Total_Number_of_BullsEyes-row").value
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
    if(parseInt(new_totalbullseyes) > parseInt(new_totalthrows))
    {   
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number Of BullsEyes";
        $(notification).modal('toggle');
        return
    }

    //if input is valid then save the changed values
    var popup = document.getElementById('EditPlayerModal');
    $(popup).modal('toggle');
    await deleteChange()
    await addChange(new_firstname, new_lastname, new_totalthrows, new_totalbullseyes)
    resetEditPlayer()

}


function resetEditPlayer(){
    document.getElementById("ChoosePlayerDropdown1").innerHTML = "CHOOSE PLAYER"
    document.getElementById("TABLE-HEAD").remove()
}

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
        if(key.search("Total") != -1)
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
    button.id = "Submit-button"
    button.setAttribute("onClick", "javascript:submitPlayerChanges()")
}