const timerDisplay = document.getElementById("timer");
const countdown = setInterval(() => {

    if (timeLeft <= 0) {

        clearInterval(countdown);

        alert("Time's up! Game over!");

    } else {

        timeLeft--;

        timerDisplay.textContent = `Time Left: ${timeLeft}`;

        // Add warning animation when 10 seconds or less

        if (timeLeft <= 10) {

            timerDisplay.classList.add("timer-warning");

        }

    }

}, 1000);


function addPoints(points) {

  score += points;

  scoreDisplay.textContent = `Score: ${score}`;



  // Add animation class

  scoreDisplay.classList.add("score-boost");



  // Remove it after animation so it can be reused

  setTimeout(() => {

      scoreDisplay.classList.remove("score-boost");

  }, 500);

}

let difficulty = "easy";

 

function generateQuestion() {

    let num1, num2, operator;

 

    if (difficulty === "easy") {

        num1 = Math.floor(Math.random() * 10);

        num2 = Math.floor(Math.random() * 10);

        operator = "+";

    } else if (difficulty === "medium") {

        num1 = Math.floor(Math.random() * 50);

        num2 = Math.floor(Math.random() * 50);

        operator = ["+", "-"][Math.floor(Math.random() * 2)];

    } else if (difficulty === "hard") {

        num1 = Math.floor(Math.random() * 100);

        num2 = Math.floor(Math.random() * 100);

        operator = ["+", "-", "*", "/"][Math.floor(Math.random() * 4)];

    }

    return { num1, num2, operator };

}