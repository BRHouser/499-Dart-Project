//Input FirstName (String): The first name of the Player
//Input LastName (String): The last name of the Player
//Input NumberOfThrows (String): The total number of thrown darts by the player
//Input NumberOfBullseyes (String): The total number of bullseyes by the player
//The purpose of this function is to add the changed player in the database by calling the server function addPlayer
function addPlayer(FirstName, LastName, NumberOfThrows, NumberOfBullseyes)
{
    data = {firstname: FirstName, lastname: LastName, totalthrows: NumberOfThrows.toString(), totalbullseyes: NumberOfBullseyes.toString()}
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


//The purpose of this function is to reset the elements in the addplayer modal
function resetAddPlayer()
{
    document.getElementById("FirstName").value = "";
    document.getElementById("LastName").value = "";
    document.getElementById("NumberOfThrows").value = 0;
    document.getElementById("Bullseyes").value = 0;
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
    var NumberOfThrows = document.getElementById("NumberOfThrows").value;
    var NumberOfBullseyes = document.getElementById("Bullseyes").value;

    //checks to see if input was put for the throws
    if(NumberOfThrows.trim() == "")
        NumberOfThrows = 0
    if(NumberOfBullseyes.trim() == "")
        NumberOfBullseyes = 0

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

    //Checks to see if the throws are valid
    if(parseInt(NumberOfBullseyes) > parseInt(NumberOfThrows))
    {   
        submit = false;
        resetAddPlayer();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number Of BullsEyes";
        $(notification).modal('toggle');
        return
    }

    //if everything is correct then submit the information
    if(submit)
    {
        //checks to see if player is already in system
        //if not then add player
        let response = await addPlayer(FirstName, LastName, NumberOfThrows, NumberOfBullseyes);
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
