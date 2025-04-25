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
    # Define difficulty parameters
    if difficulty == "easy":
        # Numbers from 1-10, basic operations
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-", "*"])
    elif difficulty == "medium":
        # Numbers from 1-20, includes division
        a = random.randint(5, 20)
        b = random.randint(5, 20)
        op = random.choice(["+", "-", "*", "/"])
        # Ensure clean division
        if op == "/":
            # Make sure division results in an integer
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
    elif difficulty == "hard":
        # Larger numbers, all operations
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        op = random.choice(["+", "-", "*", "/"])
        # Ensure clean division
        if op == "/":
            # Make sure division results in an integer
            b = random.randint(1, 12)
            a = b * random.randint(1, 12)
    
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

@app.route('/get_question')
def get_question():
    # Get difficulty from the request parameters
    difficulty = request.args.get('difficulty', 'easy')
    question, answer = generate_question(difficulty)
    return jsonify({"question": question, "answer": answer})

if __name__ == '__main__':
     app.run(debug=True)
#if __name__ == "__main__":
#    start_game()
