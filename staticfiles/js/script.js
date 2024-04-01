// Limits input expresion to alphabetics and spaces only
// Taken and altered from https://stackoverflow.com/questions/13607278/html5-restricting-input-characters/74549710#74549710
// FWDekker answer
const input = document.getElementById("id_cast");
const regex = new RegExp("^[a-zA-Z ,]*$");

input.addEventListener("beforeinput", (event) => {
  if (event.data != null && !regex.test(event.data)) 
    event.preventDefault();
});