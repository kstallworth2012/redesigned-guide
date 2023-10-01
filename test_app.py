from app import app
from unittest import TestCase
from flask import Flask, request, render_template, redirect, flash, session, jsonify,make_response
from models import db, User,Posts


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9644@localhost/Blogly_Test'
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
	"""
	Tests User model
	"""
	def setUp(self):
		"""
		clean up existing users
		"""
		print("====================================")
		print("SET UP")
		print("====================================")
		User.query.delete()


	def tearDown(self):
		"""
		Clean up any transactions 
		"""
		print("====================================")
		print("Tear Down")
		print("====================================")

		db.session.rollback()


	def test_greet(self):
		testUser = User(first_name='Test',last_name='User',image_url='https://www.pngegg.com/en/png-wnjpt')
		self.assertEqual(testUser.greet(),"What's the business baby!? My name is Test User")

class PostsModelTestCase(TestCase):
	"""
	Tests Posts model 
	"""
	def setUp(self):
		Posts.query.delete()


	def tearDown(self):
		db.session.rollback()




		




class UserViewsTestCase(TestCase):
	"""
	Tests for views for Users 
	"""

	def setUp(self):
		"""
		Add Sample User
		"""
		User.query.delete()

		testUser1 = User(first_name='Tester',last_name='User',image_url='https://www.pngegg.com/en/png-wnjpt')
		db.session.add(testUser1)
		db.session.commit()

		self.user_id = testUser1.id
		self.user = testUser1

	def tearDown(self):
		"""
		CLEAN UP ANY FOULED TRANSACTIONS
		"""
		db.session.rollback()


	def test_list_users(self):
		with app.test_client() as client:
			res = client.get('/user_list')
			html = res.get_data(as_text=True)

			self.assertEqual(res.status_code,200)
			self.assertIn('<h4>SUPER USER LIST</h4>',html)


	def test_show_user(self):
		with app.test_client() as client:
			res = client.get(f'/show_user/{self.user_id}')
			html = res.get_data(as_text=True)
			self.assertEqual(res.status_code,200)
			self.assertIn(f'<span class="card-title">Tester User</span>',html)


	def test_add_user(self):
		with app.test_client() as client:
			d = {"first_name":"Test", "last_name":"User","image_url":"https://www.pngegg.com/en/png-wnjpt"}
			res = client.post("/new-user",data=d,follow_redirects=True)
			html = res.get_data(as_text=True)

			self.assertEqual(res.status_code,200)











































