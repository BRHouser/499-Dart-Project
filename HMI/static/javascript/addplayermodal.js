
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

function resetAddPlayer()
{
    document.getElementById("FirstName").value = "";
    document.getElementById("LastName").value = "";
    document.getElementById("NumberOfThrows").value = 0;
    document.getElementById("Bullseyes").value = 0;
}

async function closeModal(){
    submit = true;
    var popup = document.getElementById('AddPlayerModal');
    var notification = document.getElementById("NotificationModal");
    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;
    var NumberOfThrows = document.getElementById("NumberOfThrows").value;
    var NumberOfBullseyes = document.getElementById("Bullseyes").value;
    if(FirstName.trim() == "")
    {
        submit = false;
        resetAddPlayer();                
        document.getElementById('ErrorText').innerHTML = "Invalid Input: First Name";
        $(notification).modal('toggle');
        return
    }
    if(LastName.trim() == "")
    {
        submit = false;
        resetAddPlayer();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Last Name";
        $(notification).modal('toggle');
        return
    }
    if(NumberOfBullseyes > NumberOfThrows)
    {   
        submit = false;
        resetAddPlayer();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number Of BullsEyes";
        $(notification).modal('toggle');
        return
    }
    if(submit)
    {
        let response = await addPlayer(FirstName, LastName, NumberOfThrows, NumberOfBullseyes);
        if(response == "True")
        {
            $(popup).modal('toggle');
        }
        else
        {
            resetAddPlayer();
            document.getElementById('ErrorText').innerHTML = "Player is already in system";
            $(notification).modal('toggle');
        }
    }
}
