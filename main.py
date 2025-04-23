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

    # Capture the output of the terminal
    output = io.StringIO()
    sys.stdout = output

    # Example terminal output
    print("Hello, this is the terminal output!")
    print("Another line of output.")

    # Reset stdout
    sys.stdout = sys.__stdout__

    # Get the captured output
    terminal_output = output.getvalue()

    # Render the output in an HTML page
    html_template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Terminal Output</title>
    </head>
    <body>
        <h1>Terminal Output</h1>
        <pre>{{ output }}</pre>
    </body>
    </html>
    """
    return render_template_string(html_template, output=terminal_output)


# @app.route('/increment', methods=['POST'])
# def increment():
#     global count
#     count += 1
#     return jsonify({'count': count})

# @app.route('/increment2', methods=['POST'])
# def increment2():
#     global gcount
#     gcount += 1
#     return jsonify({'gcount': gcount})

# @app.route('/py', methods=['GET', 'POST'])
# def squarenumber():
#     if request.method == 'POST':
#         num = request.form.get('num')
#         if num is None:  # No number entered, show input form
#             return render_template('squarenum.html')
#         elif num.strip() == '':  # Empty input
#             return "<h1>Invalid number. Please enter a number.</h1>"
#         square = int(num) ** 2
#         return render_template('answer.html', squareofnum=square, num=num)
#     return render_template('squarenum.html')

# @app.route('/play_game', methods=['GET', 'POST'])
# def play_game():
#     start_game()

# @app.route('/flip_case', methods=['POST'])
# def flip_case():
#     text = request.json['text']
#     flipped_text = ''.join(c.lower() if c.isupper() else c.upper() for c in text)
#     return jsonify({'flipped_text': flipped_text})

# Math problems
# math_rooms = [
#     {"question": "5 + 3", "answer": "8", "room": "room1"},
#     {"question": "12 - 4", "answer": "8", "room": "room2"},
#     {"question": "3 × 3", "answer": "9", "room": "room3"},
#     {"question": "16 ÷ 4", "answer": "4", "room": "room4"},]

# Generate a random math question

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