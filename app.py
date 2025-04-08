from flask import Flask, jsonify, render_template, request # type: ignore
import io 
from contextlib import redirect_stdout 
from main import start_game
app = Flask(__name__)


@app.route('/play_game', methods=['POST'])
def play_game():
    f = io.StringIO()
    with redirect_stdout(f):
        start_game()
    output = f.getvalue()
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)



