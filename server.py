# import os
# import subprocess
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# # Update paths based on correct folder structure
# GAME_PATHS = {
#     "car": os.path.join("games", "car", "car.py"),  # Removed "static"
#     "pong": os.path.join("games", "pong", "pong.py"),  # Removed "static"
#     "tetris": os.path.join("games", "tetris", "main.py"),  # Removed "static"
# }
#
# @app.route('/')
# def home():
#     return render_template("index.html")
#
# @app.route('/run/<game>')
# def run_game(game):
#     if game in GAME_PATHS:
#         game_path = GAME_PATHS[game]
#         subprocess.Popen(["python", game_path])
#         return f"Running {game} game..."
#     else:
#         return "Error: Game not found!"
#
# if __name__ == '__main__':
#     app.run(debug=True)


import os
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

# Dictionary to store running game processes
running_processes = {}

# Game file paths
GAME_PATHS = {
    "car": os.path.join("games", "car", "car.py"),
    "pong": os.path.join("games", "pong", "pong.py"),
    "tetris": os.path.join("games", "tetris", "main.py"),
}


@app.route('/')
def home():
    return render_template("index.html")


# Route to start a game
@app.route('/run/<game>')
def run_game(game):
    if game in GAME_PATHS:
        # If game is already running, prevent duplicate instances
        if game in running_processes and running_processes[game].poll() is None:
            return f"{game} is already running!"

        # Start the game and store the process
        game_path = GAME_PATHS[game]
        process = subprocess.Popen(["python", game_path])
        running_processes[game] = process
        return f"Running {game} game..."
    else:
        return "Error: Game not found!"


# Route to stop a running game
@app.route('/stop/<game>')
def stop_game(game):
    if game in running_processes:
        process = running_processes[game]

        # Check if the process is still running
        if process.poll() is None:
            process.terminate()  # Terminate the process
            process.wait()  # Wait for process to end
            del running_processes[game]  # Remove from dictionary
            return f"Stopped {game} game."
        else:
            del running_processes[game]  # Cleanup stale process
            return f"{game} was not running."
    else:
        return "Error: Game not running!"


if __name__ == '__main__':
    app.run(debug=True)

