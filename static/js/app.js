// import { quill } from 'quill.js'
// Import the functions you need from the SDKs you need
// import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";

 
document.getElementById("story-form").addEventListener("submit", function(event) {
  event.preventDefault();
  generateText();
  });

document.getElementById("process").addEventListener("click", function() {
    // Call the functions to process the generated story
    processStory();
});

document.getElementById("settings-form").addEventListener("submit", function(event) {
  event.preventDefault();
  saveApiKey();
});

async function saveApiKey() {
  const apiKey = document.getElementById("api-key").value;

  const response = await fetch("/save-api-key", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({"api-key": apiKey}),
  });

  if (response.ok) {
    alert("API key saved successfully.");
  } else {
    alert("An error occurred while saving the API key. Please try again.");
  }
}

async function generateText() {
  const apiKey = document.getElementById("api-key").value;
  const title = document.getElementById("title").value;
  const genre = document.getElementById("genre").value;
  const characters = document.getElementById("characters").value;
  const plot = document.getElementById("plot").value;

  let prompts = [];

  for (let i = 1; i <= 12; i++) {
    const val = document.getElementById(`prompt${i}`).value;
    val ? prompts.push(`Chapter ${i} : ${val}`) : null;
  }

  // const editing_agents = document.getElementById("editing-agents").value;
  const editing_agents = 10;
  // const refinement_agents = document.getElementById("refinement-agents").value;
  const refinement_agents = 10;
  // const gap_agents = document.getElementById("gap-agents").value;
  const gap_agents = 1;
  const num_agents = parseInt(editing_agents) + parseInt(refinement_agents) + parseInt(gap_agents);
  const temperature = document.getElementById("temperature").value / 100;
  const outputContainer = document.getElementById("generated-text");
  const typingSpeed = 10; // adjust this to change the typing speed in milliseconds

  // outputContainer.innerHTML = ""; // clear previous content

  const generatedTexts = [];

    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({apiKey, title, genre, characters, plot, prompts, editing_agents, refinement_agents, gap_agents, temperature})
    });

    if (response.ok) {
      console.log(response)
      const generatedText = await response.json();
      const formattedText = formatText(generatedText);
      if(formattedText) console.log("formattedText-------------------------------", formattedText)
      // add each character of the text to the output container with a delay to simulate typing
      for (let j = 0; j < formattedText.length; j++) {
        setTimeout(() => {
          quill.insertText(j,formattedText.charAt(j));
        }, j * 50);
      }

      generatedTexts.push(generatedText);
    } else {
      alert("An error occurred while generating text. Please try again.");
      return;
    }

  return generatedTexts;
}

function formatText(text) {
  if(text.text)  return text.text;
  else return null;
}

document.addEventListener("DOMContentLoaded", function() {
  // Retrieve saved values from local storage
  const title = localStorage.getItem("title");
  const genre = localStorage.getItem("genre");
  const characters = localStorage.getItem("characters");
  const plot = localStorage.getItem("plot");
  const prompt = localStorage.getItem("prompt");

  // Set input values
document.getElementById("title").value = title;
document.getElementById("genre").value = genre;
document.getElementById("characters").value = characters;
document.getElementById("plot").value = plot;
document.getElementById("prompt").value = prompt;

// Save API key if it exists
const apiKey = localStorage.getItem("api-key");
if (apiKey) {
    document.getElementById("api-key").value = apiKey;
    saveApiKey();
}
});

// document.getElementById("editing-agents").addEventListener("input", function () {
// document.getElementById("editing-agents-value").textContent = this.value;
// });

// document.getElementById("refinement-agents").addEventListener("input", function () {
// document.getElementById("refinement-agents-value").textContent = this.value;
// });

// document.getElementById("gap-agents").addEventListener("input", function () {
// document.getElementById("gap-agents-value").textContent = this.value;
// });

// document.getElementById("num_agents").addEventListener("input", function () {
// document.getElementById("num_agents-value").textContent = this.value;
// });

document.getElementById("temperature").addEventListener("input", function () {
document.getElementById("temperature-value").textContent = this.value;
});


function processStory() {
  const outputContainer = document.getElementById("generated-text");
  const generatedText = outputContainer.value; // store generated text in a variable

  // Gap agent
  $.ajax({
    type: "POST",
    url: "/gap-agent",
    contentType: "application/json",
    data: JSON.stringify({ text: generatedText }),
    success: function (response) {
      // Update the generated text with the gap agent's output
      const gapText = response;

      // Refinement agent
      $.ajax({
        type: "POST",
        url: "/refinement-agent",
        contentType: "application/json",
        data: JSON.stringify({ text: gapText }),
        success: function (response) {
          // Update the generated text with the refinement agent's output
          const refinementText = response;

          // Editing agent
          $.ajax({
            type: "POST",
            url: "/editing-agent",
            contentType: "application/json",
            data: JSON.stringify({ text: refinementText }),
            success: function (response) {
              // Update the generated text with the editing agent's output
              const editedText = response;

              // Display the final, processed text
              outputContainer.innerHTML = `<p><strong>Original Text:</strong></p><div>${generatedText}</div><p><strong>Processed Text:</strong></p><div>${editedText}</div>`;
            }
          });
        }
      });
    }
  });
}
