import io
from contextlib import redirect_stdout
from flask import Flask, jsonify, render_template, request, render_template_string
import json
import sys
import random
from typing import List, Optional, Tuple
from enum import Enum
import os
count = 0
gcount = 0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_question(difficulty="easy"):
    if difficulty == "easy":
        # Simple numbers and operations
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
        answer = eval(f"{a} {op} {b}")

    elif difficulty == "medium":
        # Moderate numbers and more operation types
        a = random.randint(10, 30)
        b = random.randint(2, 15)
        op = random.choice(["+", "-", "*"])
        answer = eval(f"{a} {op} {b}")

    elif difficulty == "hard":
        # Large numbers and division, maybe decimals
        a = random.randint(20, 100)
        b = random.randint(2, 20)
        op = random.choice(["+", "-", "*", "/"])
        if op == "/":
            b = random.randint(1, 10)
            a = b * random.randint(2, 10)  # clean division
            answer = round(a / b, 2)
        else:
            answer = eval(f"{a} {op} {b}")

    question = f"{a} {op} {b}"
    return question, answer

@app.route('/get_question')
def get_question():
    # Get difficulty from the request parameters
    difficulty = request.args.get('difficulty', 'easy')
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "easy"
question, answer = generate_question(difficulty)
    
    return jsonify({"question": question, "answer": answer})

if __name__ == '__main__':
     app.run(debug=True)
#if __name__ == "__main__":
#    start_game()
