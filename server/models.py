from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('You must provide a name')
        elif name in db.session.query(Author.name).all():
            raise ValueError('You must provide a unique name')
        
        return name
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError('Phone number must be 10 characters long')
        
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    
    @validates('title')
    def validate_title(self, key, title):
        CLICKBAIT = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError('You must provide a title')
        elif title not in CLICKBAIT:
            raise ValueError(f'The title must include one or more of the following: {CLICKBAIT}')
        
        return title
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long')
        
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError('Summary must be less than 250 characters long')
        
        return summary
    @validates('category')
    def validate_category(self, key, category):
        CATEGORIES = ['Fiction', 'Non-Fiction']
        if category not in CATEGORIES:
            raise ValueError(f'Category must be one of the following: {CATEGORIES}')
        
        return category
    