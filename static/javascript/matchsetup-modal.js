function addMatch(P1Name, P2Name, ScoreLimit, MatchType, NumbersOfSets, NumberOfLegs, Official, MatchName,Location,DateOfMatch)
{ 
    data = {Player1Name: P1Name, Player2Name: P2Name, Score:ScoreLimit, MatchType:MatchType, SetNumber:NumbersOfSets.toString(), NumberOfLegs:NumberOfLegs.toString(), MatchOfficial:Official, NameofMatch: MatchName, Location:Location, DateOfMatch:DateOfMatch}
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
    document.getElementById("ScoreSelect").selectedIndex = 0;
    document.getElementById("MatchTypeSelect").selectedIndex = 0;
    document.getElementById("NumberOfSets").value = 0;
    document.getElementById("NumberOfLegs").value = 0;
    document.getElementById("Official").value = "";
    document.getElementById("MatchName").value = "";
    document.getElementById("MatchLocation").value = "";
    document.getElementById("MatchDate").value = ""; ///////////////////////////////////

}

async function closeMatchModal(){
    //Variable initialize
    submit = true;
    var popup = document.getElementById('MatchSetupModal');
    var notification = document.getElementById("NotificationModal");
    var Player1 = document.getElementById("ChoosePlayerDropdown2").innerHTML;
    var Player2 = document.getElementById("ChoosePlayerDropdown3").innerHTML;
    var Score = document.getElementById("ScoreSelect").value;
    var MatchType = document.getElementById("MatchTypeSelect").value;
    var NumberOfLegs = document.getElementById("NumberOfLegs").value;
    var OfficialMatch = document.getElementById("Official").value;
    var Match_Name = document.getElementById("MatchName").value;
    var Location = document.getElementById("MatchLocation").value;
    var Date = document.getElementById("MatchDate").value; 
    var NumberOfSets = document.getElementById("NumberOfSets").value;

    if(MatchType.trim() == "Game"){
        NumberOfSets = document.getElementById('NumberOfSets').value = 0;
    }
    
    if(NumberOfSets.value <= "-1")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number of Sets";
        $(notification).modal('toggle');
        return
    }
    
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

    if(Player2.trim() == Player1.trim())
    {
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Players are the same";
        $(notification).modal('toggle');
        return
    }

    if(Score.trim() == "Score")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Score";
        $(notification).modal('toggle');
        return
    }

    if(MatchType.trim() == "Match Type")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Match Type";
        $(notification).modal('toggle');
        return
    }


    if(NumberOfLegs.trim() == "0")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Number of Legs";
        $(notification).modal('toggle');
        return
    }

    if(OfficialMatch.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Official Name";
        $(notification).modal('toggle');
        return
    }

    if(Match_Name.trim() == "")
    {   
        submit = false;
        resetSetupMatch();
        document.getElementById('ErrorText').innerHTML = "Invalid Input: Match Name";
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
        let response = await addMatch(Player1, Player2, Score, MatchType, NumberOfSets, NumberOfLegs, OfficialMatch, Match_Name, Location, Date);
        if(response == "True")
        {
            resetSetupMatch();
            //$(popup).modal('toggle');
        }
        else //if matchname is in system throw notification
        {
            resetSetupMatch();
            document.getElementById('ErrorText').innerHTML = "Match Name is already in system";
            $(notification).modal('toggle');
        }
    }
}

function toggleSets(val){
    if(val == "Game") {
        hideSets();

    }
    else {
        showSets();
    }
}

//display sets selector for championship play
function showSets() {
    $("#setsPicker").show();
}

//hide sets selector for normal play
function hideSets() {
    $("#setsPicker").hide();
}
