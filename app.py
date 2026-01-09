from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)

@app.route("/")
def chat():
    return render_template("chat.html")

@socketio.on("message")
def handle_message(msg):
    send(f"{msg['username']}: {msg['message']}", broadcast=True)

@socketio.on("join")
def handle_join(username):
    send(f"{username} joined the chat", broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
