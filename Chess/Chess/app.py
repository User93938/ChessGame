from flask import Flask, render_template, request, jsonify
from ChessEngine import GameState, Move

app = Flask(__name__)
game_state = GameState()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify(game_state.board)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    move = Move(data['start'], data['end'], game_state.board)
    game_state.makeMove(move)
    return jsonify(game_state.board)

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = GameState()
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)
