from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
	db.app = app 
	db.init_app(app)


	# MODELS GO HERE 
class User(db.Model):
	__tablename__='users'

	def __repr__(self):
		""" show info about pet. """
		u = self
		return f'<Users id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>'

	def greet(self):
		return f"What's the business baby!? My name is {self.first_name} {self.last_name}"

	def first(self):
		return f'{self.first_name}'

	def get_full_name(self):
		return f'{self.first_name} {self.last_name}'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	first_name = db.Column(db.String(50), nullable=False, unique=True)

	last_name = db.Column(db.String(30), nullable=True)

	image_url = db.Column(db.String(500), nullable=False)
	# post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	uposts = db.relationship('Posts',backref='user')


class Posts(db.Model):
	__tablename__ = 'posts'

	def __repr__(self):
		"""Info about a user post."""
		return f'User:{self.user.first_name} {self.user.last_name}\nTitle:{self.title}\nDate Created:{self.create_at}\n\nContent:{self.content}'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(50), nullable=False, unique=True)
	content = db.Column(db.Text, nullable=True)
	create_at = db.Column(db.DateTime, default=datetime.now) #or utcnow
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	# user = db.relationship('User')















class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Posts',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tag",
    )
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)







