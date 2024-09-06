# test_app.py

import unittest
from app import app, message_storage, socketio
from flask import json
from flask_socketio import SocketIOTestClient

class ChatAppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.socketio_client = SocketIOTestClient(socketio, app)
    
    def test_send_message(self):
        response = self.client.post('/send_message', json={
            'user': 'JohnDoe',
            'message': 'Hello world!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'Message received')
        self.assertIn('JohnDoe', message_storage)
        self.assertIn('Hello world!', message_storage['JohnDoe'])
    
    def test_get_all_messages(self):
        response = self.client.get('/get_all_messages?user=JohnDoe')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['Hello world!'])

    def test_socket_message(self):
        self.socketio_client.emit('message', {
            'user': 'JaneDoe',
            'message': 'Hi there!'
        })
        self.assertIn('JaneDoe', message_storage)
        self.assertIn('Hi there!', message_storage['JaneDoe'])

if __name__ == '__main__':
    unittest.main()
