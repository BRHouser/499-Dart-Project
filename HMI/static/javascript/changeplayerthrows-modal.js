function getPlayersList(){
    const request = new XMLHttpRequest();
    request.open('POST', '/getPlayers');
    request.send();
    return new Promise((resolve) => {
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            console.log(response)
            resolve(response);
        }; 
    });
}

async function getPlayers()
{
    let players = await getPlayersList();
    var dropdown = document.getElementById("dynamic-dropdown");
    console.log(dropdown.childNodes.length)

    while(dropdown.childNodes[0] != null)
    {
        console.log(dropdown.childNodes[0])
        dropdown.removeChild(dropdown.childNodes[0]);
    }

    for(var key in players)
    {
        var element = document.createElement("a")
        element.classList.add("dropdown-item")
        element.href = "#"
        var node = document.createTextNode(players[key])
        element.appendChild(node)
        dropdown.appendChild(element)
    }

}