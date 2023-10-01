from flask import Flask, request, render_template, redirect, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User,Posts,Tag,PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9644@localhost/Blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] ="doubloonshoainakffasd"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] =False

connect_db(app)




@app.route('/')
def home_page():
	"""Shows the home page """
	posts = Posts.query.all()
	return render_template('home_page.html',posts=posts)
# 	return  """
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <title>THIS IS KENNETH ON HIS SOFTWARE ENGINEERING JOURNEY!</title>
# </head>
# <body>
# <div>
# <h1>	WELCOME AGAIN TO MY SOFTWARE ENGINEERING JOURNEY</h1>
# </div>
# </body>
# </html>
#     """


@app.route('/user_list')
def user_list():
	"""
	shows list of all users
	"""
	users = User.query.all()
	return render_template('user_list.html',users=users)

@app.route('/user-form')
def user_form():
	return render_template("user_form.html")
@app.route('/new-user', methods=["POST"])
def new_user():
	firstName = request.form["first_name"]
	lastName = request.form["last_name"]
	imageUrl = request.form["image_url"]
	# https://www.pngegg.com/en/png-wnjpt
	new_user = User(first_name=firstName,last_name=lastName,image_url=imageUrl)
	db.session.add(new_user)
	db.session.commit()

	return redirect(f'/show-user/{new_user.id}')


@app.route('/show-user/<int:user_id>')
def show_user(user_id):
	"""
	Show info on a single user
	"""
	user = User.query.get_or_404(user_id)
	return render_template("user_information.html",user=user)


@app.route('/show-user/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
	"""
	Edit User information 
	"""
	user = User.query.get_or_404(user_id)
	firstName = request.form["first_name"]
	lastName = request.form["last_name"]
	imageUrl = request.form["image_url"]
	
	db.session.add(user)
	db.session.commit()

	return redirect('/user_list')
	# render_template("user_update.html",user)


@app.route('/show-user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
	"""
	Delete a USER 
	"""
	user = User.query.get_or_404(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect('/user_list')
	# return render_template("user_delete.html",user)



@app.route('/show-user/<int:user_id>/posts/new')
def show_post_form(user_id):
	"""
	Show form to add a post for that user 
	"""
	user = User.query.get_or_404(user_id)
	return render_template('new_post.html',user=user) 


@app.route('/show-user/<int:user_id>/posts/new', methods=["POST"])
def show_post_detail(user_id):
	"""
	Handle add form; add post and redirect to the user detail page 
	"""
	user = User.query.get_or_404(user_id)
	newPost = Posts(title=request.form['title'], content=request.form['content'], user=user)

	db.session.add(newPost)
	db.session.commit()

	return redirect(f'/show-user/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
	"""
	show a post
	"""
	user_post = Posts.query.get_or_404(post_id)
	return render_template('post_detail.html',user_post=user_post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
	"""
	Show a form to edit a post
	"""
	user_post = Posts.query.get_or_404(post_id) 
	return render_template('edit_post.html',user_post=user_post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
	"""
	Handle editing of a post. Redirect back to the post view.
	"""
	user_post = Posts.query.get_or_404(post_id)
	user_post.title = request.form['title']
	user_post.content = request.form['content']
	
	db.session.add(user_post)
	db.session.commit() 
	return redirect(f'/show-user/{user_post.id}')



@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
	"""
	Delete Post
	"""
	user_post = Posts.query.get_or_404(post_id)

	db.session.delete(user_post)
	db.session.commit()
	return redirect(f'/show-user/{user_post.id}')



# =============================================================================================
# Part Three: Add M2M Relationship
# =============================================================================================

# Add Routes

# # GET /tags
@app.route('/tags')
def all_tags():
	tags = Tag.query.all()
	return render_template('tags_list.html',tags=tags)
# # Lists all tags, with links to the tag detail page.
# # GET /tags/[tag-id]
@app.route('/tags/<int:tag_id>')
def get_tag_detail(tag_id):
	tag = Tag.query.get_or_404(tag_id)
	return render_template('tag_detail.html',tag=tag)
# # Show detail about a tag. Have links to edit form and to delete.
# # GET /tags/new
@app.route('/tags/new')
def new_tag_form():
	return render_template('new_tag.html')

# # Shows a form to add a new tag.
# # POST /tags/new
@app.route('/tags/new-tag',methods=["POST"])
def new_tag():
	
	tagName = request.form["tag_name"]

	new_tag = Tag(name=tagName)
	
	db.session.add(new_tag)
	db.session.commit()

	return redirect('/tags')
# # Process add form, adds tag, and redirect to tag list.

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
	"""
	Show edit form for a tag.
	"""
	eTag = Tag.query.get_or_404(tag_id) 
	return render_template('edit_tag.html',eTag=eTag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
	"""
	Process edit form, edit tag, and redirects to the tags list.
	"""
	eTag = Tag.query.get_or_404(tag_id)
	eTag.name = request.form['tag_name']
	
	
	db.session.add(eTag)
	db.session.commit() 
	return redirect(f'/tags/{eTag.id}')





@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
	"""
	Delete a tag.
	"""
	eTag = Tag.query.get_or_404(tag_id)

	db.session.delete(eTag)
	db.session.commit()
	return redirect(f'/show-user/{user_post.id}')
