function addPlayer()
{
    //MORE INFORMATION WILL PROBABLY BE ADDED TO THIS BUT IT IS JUST THE BASICS FOR NOW
    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;
    var NumberOfThrows = document.getElementById("NumberOfThrows").value;
    var NumberOfBullseyes = document.getElementById("Bullseyes").value;

    data = {firstname: FirstName, lastname: LastName, totalthrows: NumberOfThrows.toString(), totalbullseyes: NumberOfBullseyes.toString()}
    const request = new XMLHttpRequest();
    request.open('POST', '/addPlayer');
    request.send(JSON.stringify(data));
}