from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages - returns all messages ordered by created_at ascending
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

# POST /messages - creates a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    if not data.get('body') or not data.get('username'):
        return jsonify({'error': 'Body and username are required'}), 400
    
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id> - updates message body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    
    if 'body' in data:
        message.body = data['body']
        db.session.commit()
    
    return jsonify(message.to_dict())

# DELETE /messages/<int:id> - deletes a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    
    db.session.delete(message)
    db.session.commit()
    
    return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)