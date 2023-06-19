// const inputElement = document.getElementById("chatbot-input");
// const submitButton = document.querySelector(".submit");
// const output = document.querySelector(".output");

// submitButton.addEventListener("click", function() {
//   const userInput = inputElement.value;
//   output.innerHTML += "<div>" + userInput + "</div>";
//   inputElement.value = "";

//   // fetch('/completion', {
//   //   method: 'POST',
//   //   headers: {
//   //     'Content-Type': 'application/json'
//   //   },
//   //   body: JSON.stringify({ message: userInput })
//   // }).then(res => res.text())
//   //   .then(data => {
//   //     output.innerHTML += "<div>" + data + "</div>";
//   //   })
//   //   .catch(err => console.log(err));
// });

const inputElement = document.getElementById("chatbot-input");
const submitButton = document.querySelector(".submit");
const output = document.querySelector(".output");

submitButton.addEventListener("click", function() {
  const userInput = inputElement.value;
  output.innerHTML += "<div>" + userInput + "</div>";
  inputElement.value = "";

  fetch('/completion', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ messages: [{ content: userInput }] })
  })
    .then(res => res.json())
    .then(data => {
      const response = data.choices[0].message.content;
      output.innerHTML += "<div>" + response + "</div>";
    })
    .catch(err => console.log(err));
});
