function addMatch(P1Name, P2Name, ScoreLimit, NumberOfLegs, NumbersOfSets, Location, DateOfMatch, MatchType)
{
    data = {Player1Name: P1Name, Player2Name: P2Name, Score:ScoreLimit, NumberOfLegs:NumberOfLegs, NumbersOfSets:NumbersOfSets, Location:Location, DateOfMatch:DateOfMatch, MatchType:MatchType}
    const request = new XMLHttpRequest();
    request.open('POST', '/addMatch');
    request.send(JSON.stringify(data));
    return new Promise((resolve) => {
        request.onload = () => {
            const response = request.responseText;
            resolve(response);
        }; 
    });
}

//The purpose of this function is to reset the elements in the Setup Match modal
function resetSetupMatch()
{
    document.getElementById("ChoosePlayerDropdown2").innerHTML = "Select Player 1"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }
    document.getElementById("ChoosePlayerDropdown3").innerHTML = "Select Player 2"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }
    document.getElementById("ScoreSetUpDropdown").innerHTML = "Score"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }
    document.getElementById("MatchType").innerHTML = "Match Type"
    try{
    document.getElementById("TABLE-HEAD").remove()
    } catch(error) {
        console.log("No table")
    }
    document.getElementById("NumberOfSets").value = 0;
    document.getElementById("NumberOfLegs").value = 0;
    document.getElementById("MatchLocation").value = "";
    document.getElementById("MatchLocation").value = "";
    document.getElementById("MatchDate").value = ""; ///////////////////////////////////

}

async function closeMatchModal(){
    //Variable initialize
    submit = true;
    var popup = document.getElementById('MatchSetupModal');
    var notification = document.getElementById("NotificationModal");
    var Player1 = document.getElementById("ChoosePlayerDropdown2").value;
    var Player2 = document.getElementById("ChoosePlayerDropdown3").value;
    var Score = document.getElementById("ScoreSetUpDropdown").value;
    var MatchType = document.getElementById("MatchType").value;
    var NumberOfSets = document.getElementById("NumberOfSets").value;
    var NumberOfLegs = document.getElementById("NumberOfLegs").value;
    var Location = document.getElementById("MatchLocation").value;
    var Date = document.getElementById("MatchDate").value;


    if(Player1.trim() == "Select Player 1")
    {
        submit = false;
        resetSetupMatch();                
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player 1 Name";
        $(notification).modal('toggle');
        return
    }


    if(Player2.trim() == "Select Player 2")
    {
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Player 2 Name";
        $(notification).modal('toggle');
        return
    }

    if(Score.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Score";
        $(notification).modal('toggle');
        return
    }

    if(MatchType.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Match Type";
        $(notification).modal('toggle');
        return
    }

    if(NumberOfSets.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number of Sets";
        $(notification).modal('toggle');
        return
    }

    if(NumberOfLegs.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number of Legs";
        $(notification).modal('toggle');
        return
    }

    if(Location.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Location";
        $(notification).modal('toggle');
        return
    }

    if(Date.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Date";
        $(notification).modal('toggle');
        return
    }

    //if everything is correct then submit the information
    if(submit)
    {
        let response = await addMatch(Player1Name, Player2Name, Score, NumberOfLegs, NumberOfSets, Location, Date, MatchType);
        if(response == "True")
        {
            resetSetupMatch();
            $(popup).modal('toggle');
        }
        //else //if player is in system throw notification
        //{
        //    resetAddPlayer();
         //   document.getElementById('ErrorText').innerHTML = " is already in system";
          //  $(notification).modal('toggle');
        //}
    }
}

function changeScoreName(score){
    var element = document.getElementById("ScoreSetUpDropdown");
    element.innerHTML = score
}

function ScoreDropdown()
{
    let list = ['301','501','801']

    var dropdown = document.getElementById("ScoreSetUpDropdown");
    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    for (var i in list)
    {
        var element = document.createElement("a");
        element.id = list[i] +"-dropdown";
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeScoreName('" + list[i] + "')");
        element.href = "#";
        var node = document.createTextNode(list[i]);
        element.appendChild(node);
        dropdown.appendChild(element);
    }

}

function changeMatchType(type){
    var element = document.getElementById("MatchType");
    element.innerHTML = type
}

function MatchTypeDropdown()
{
    let list = ['Tournament','Match']

    var dropdown = document.getElementById("MatchType");
    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    for (var i in list)
    {
        var element = document.createElement("a")
        element.id = list[i] +"-dropdown"
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeMatchType('" + list[i] + "')");
        element.href = "#";
        var node = document.createTextNode(list[i])
        element.appendChild(node)
        dropdown.appendChild(element)
    }
}

