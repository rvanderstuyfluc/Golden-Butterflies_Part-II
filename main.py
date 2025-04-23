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

def generate_question():

    a = random.randint(1, 10)

    b = random.randint(1, 10)

    op = random.choice(["+", "-", "*"])

    question = f"{a} {op} {b}"

    answer = eval(question)

    return question, answer

@app.route('/get_question')

def get_question():

    question, answer = generate_question()

    return jsonify({"question": question, "answer": answer})

if __name__ == '__main__':
     app.run(debug=True)
#if __name__ == "__main__":
#    start_game()