from app import app, db
from app.models import User, Brand, Choice, Record


@app.shell_context_processor

def make_shell_context():
    return {'db' : db, 'User' : User, 'Brand' : Brand, 'Choice' : Choice, 'Record' : Record}

