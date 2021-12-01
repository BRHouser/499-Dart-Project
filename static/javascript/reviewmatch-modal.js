//The purpose of this function is to call the function getMatches in the server and return a dictionary
function getMatchList(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getMatches');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            resolve(response);
        }; 
    });
}

function changeDisplay(id, num){
    var element = document.getElementById("MatchDrop" + num);
    element.innerHTML = id
    window.alert(id)
}

function resetReviewMatch(){
    document.getElementById("MatchDrop0").innerHTML = "Choose Match"
}

async function getMatch(num)
{
    //calls to get the players and waits til they are recieved
    let match = await getMatchList();

    var dropdown = document.getElementById("MatchDropdown" + num);

    //deletes all previous elements in the dropdown
    while(dropdown.childNodes[0] != null)
    {
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    //repopulates the dropdown with the current players in the database
    for(var key in match)
    {
        var element = document.createElement("a")
        element.id = match[key] + "-dropdown"
        element.classList.add("dropdown-item");
        element.setAttribute("onClick","javascript:changeDisplay('" + match[key] + "','"+ num + "')");
        element.href = "#";
        var node = document.createTextNode(match[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }

}