// GET is the default method, so we don't need to set it
fetch('/hello')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); // Print the greeting as text
    });





// Send the same request
fetch('/hello')
    .then(function (response) {
        return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
    })




// POST
fetch('/hello', {

   // Declare what type of data we're sending
   headers: {
     'Content-Type': 'application/json'
   },

   // Specify the method
   method: 'POST',

   // A JSON payload
   body: JSON.stringify({
       "greeting": "Hello from the browser!"
   })
}).then(function (response) { // At this point, Flask has printed our JSON
   return response.text();
}).then(function (text) {

   console.log('POST response: ');

   // Should be 'OK' if everything was successful
   console.log(text);
});



// /* JavaScript
//    Try this out in your developer console! */

//    const person = {"name":"Andrew", "loves":"Open Source"};
//    const asJSON = JSON.stringify(person);
   
//    // `person` is of type 'object'
//    console.log(`person is of type ${typeof person}`);
   
//    // `asJSON` is of type 'string'
//    console.log(`asJSON is of type ${typeof asJSON}`);
   
//    // We can convert it back to an object by parsing it
//    // `asObject` is of type 'object'
//    const asObject = JSON.parse(asJSON);
//    console.log(`asObject is of type ${typeof asObject}`);