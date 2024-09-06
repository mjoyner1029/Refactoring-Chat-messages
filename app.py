# app.py

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the message storage hashmap
message_storage = {}

@app.route('/get_all_messages', methods=['GET'])
def get_all_messages():
    user = request.args.get('user')
    if user in message_storage:
        return jsonify(message_storage[user])
    else:
        return jsonify([])

@socketio.on('message')
def handle_message(data):
    user = data.get('user')
    message = data.get('message')
    
    if user not in message_storage:
        message_storage[user] = []
    
    message_storage[user].append(message)
    
    # Emit message to all clients
    emit('message', {'user': user, 'message': message}, broadcast=True)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user = data.get('user')
    message = data.get('message')
    
    if user not in message_storage:
        message_storage[user] = []
    
    message_storage[user].append(message)
    
    return jsonify({'status': 'Message received'})

if __name__ == '__main__':
    socketio.run(app, debug=True)

