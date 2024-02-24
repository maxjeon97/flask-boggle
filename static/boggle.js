"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

const $tbody = $("tbody");
const $gameScore = $("#score")


let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure

  for (const row of board) {
    const $row = $("<tr>");

    for (const letter of row) {
      const $letter = $(`<td>${letter}</td>`);

      $row.append($letter);
    }

    $tbody.append($row);
  }
}


/* Submit request to API to get score of a word
Returns an object -> {"result": "...word_status...", "gameScore": game_score}
*/
async function getScore() {
  const response = await fetch(
    '/api/score-word',
    {
      method: "POST",
      body: JSON.stringify(
        {
          gameId: `${gameId}`,
          word: `${$wordInput.val().toUpperCase()}`
        }
      ),
      headers:
      {
        "content-type": "application/json"
      }
    }
  );

  return await response.json();
}


/* Returns message based on results of word submission */
function generateMessage(data) {
  if (data.result === "not-word") {
    return `That is not a word!`;
  }

  else if (data.result === "not-on-board") {
    return `That word doesn't exist on this board!`;
  }

  else {
    return `Ok!`;
  }
}

function displayScore(data) {
  $gameScore.html(`${data.gameScore}`)
}

/* Displays message in the DOM if word is invalid
Otherwise appends word to the DOM word list*/
function displayResult(message) {
  if (message === 'Ok!') {
    $playedWords.append(`<li>${$wordInput.val().toUpperCase()}</li>`);
  }

  else {
    $message.html(`${message}`);
  }
}



/* Handles form submission */
async function handleFormSubmit(evt) {
  evt.preventDefault();

  const data = await getScore();
  const message = generateMessage(data);
  displayScore(data);

  displayResult(message);
}

$form.on("submit", handleFormSubmit);

start();