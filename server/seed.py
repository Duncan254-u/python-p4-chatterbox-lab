from app import app
from models import db, Message

with app.app_context():
 
    Message.query.delete()
    

    messages = [
        Message(body="Hello World!", username="alice"),
        Message(body="How's everyone doing?", username="bob"),
        Message(body="Great to be here!", username="charlie"),
        Message(body="Flask is awesome!", username="diana"),
        Message(body="Building APIs is fun!", username="eve")
    ]
    
    # Add messages to database
    for message in messages:
        db.session.add(message)
    
    db.session.commit()
    print("Database seeded successfully!")