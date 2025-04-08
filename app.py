from flask import Flask, jsonify, render_template, request # type: ignore
import io 
from contextlib import redirect_stdout 
from main import start_game
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)



