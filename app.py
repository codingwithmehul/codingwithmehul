from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store online users
online_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = request.sid  # Unique session ID
    online_users[user_id] = f"User {user_id[:5]}"  # Show first 5 chars of ID
    emit('update_users', list(online_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in online_users:
        del online_users[user_id]
    emit('update_users', list(online_users.values()), broadcast=True)

@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    sender_name = online_users.get(user_id, "Unknown")
    full_message = f"{sender_name}: {data}"
    send(full_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
