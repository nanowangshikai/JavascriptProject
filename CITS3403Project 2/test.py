import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Brand, Choice, Record
from app.forms import LoginForm
from app.forms import RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all() 
        brand1 = Brand(carSeries = "Lambo")
        brand2 = Brand(carSeries = "AS")
        brand3 = Brand(carSeries = "GTR")
        db.session.add(brand1)
        db.session.add(brand2)
        db.session.add(brand3)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    #HELPER FUNCTIONS
    def register(self, username, email, password, password2, preference):
        return self.app.post("/register", data=dict(username=username, 
        email=email,
        password=password,
        password2=password2,
        preference=preference),
        follow_redirects = True)

    def login(self, username, password):
        return self.app.post("/login", data=dict(username=username,
        password=password), follow_redirects = True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects = True)

    def delete(self, id):
        return self.app.post(str("/delete_user/" + str(id)))

    def select(self):
        return self.app.post("/select", data=dict(car_select="Lambo"), follow_redirects = True)
    
#REGISTRATION FUNCTIONALITY TESTS
    #Tests a valid registration attempt
    def test_valid_registration(self):
        response = self.register("user", "user@email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
    
    #Tests an invalid registration attempt where passwords do not match
    def test_invalid_registration_passwords(self):
        response = self.register("user", "grae@email.com", "password", "invalid password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password', response.data)

    #Tests an invalid registration attempt where email is invalid
    def test_invalid_registration_email(self):
        #missing @ symbol
        response = self.register("user", "invalid email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)

        #missing domain
        response = self.register("user", "invalid@email", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)

        #invalid space inserted
        response = self.register("user", "invalid@ email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)
    
    #Tests an invalid registration where the username and/or email are already taken
    def test_invalid_registration_duplicates(self):
        u1 = User(username = "existing_user", email = "existing_user@email.com", preference = "lambo")
        db.session.add(u1)
        db.session.commit()

        #duplicate username
        response = self.register("existing_user", "user@email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User name has been used', response.data)

        #duplicate email
        response = self.register("user", "existing_user@email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email has been used', response.data)
    
    #Tests an invalid registration where one of the fields has been left blank
    def test_invalid_registration_missing(self):
        response = self.register("", "user@email.com", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data) #redirected to register page
        self.assertIn(b'value=""', response.data) #at least 1 field has been left empty

        response = self.register("user", "", "password", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

        response = self.register("user", "user@email.com", "", "password", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

        response = self.register("user", "user@email.com", "password", "", "Lambo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

#LOGIN FUNCTIONALITY TESTS
    #Tests a valid login 
    def test_successful_login(self):
        user = User(username="Grae", email="grae@email.com", preference="AS")
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        db.session.add(user)
        db.session.commit()

        response = self.login("Grae", "password")
        self.assertIn(b'Hello, Grae', response.data)
        self.assertIn(b'<title>Home</title>', response.data)
    
    #Tests invalid login attempts
    def test_unsuccussful_login(self):
        user = User(username="Grae", email="grae@email.com", preference="AS")
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        db.session.add(user)
        db.session.commit()

        #invalid username or password
        response = self.login("Grae", "invalid")
        self.assertIn(b'Invalid username or password', response.data)

        response = self.login("invalid", "password")
        self.assertIn(b'Invalid username or password', response.data)
        
        #username or password missing
        response = self.login("", "password")
        self.assertIn(b'This field is required', response.data)

        response = self.login("Grae", "")
        self.assertIn(b'This field is required', response.data)

#LOGOUT FUNCTIONALITY TESTS:
    #test logout
    def test_logout(self):
        self.app.get('/register', follow_redirects = True)
        self.register("user", "user@email.com", "password", "password", "Lambo")
        self.app.get('/login', follow_redirects = True)
        self.login("user", "password")
        response = self.app.get('/logout', follow_redirects = True)
        self.assertIn(b'Logged Out', response.data)

#ADMIN TESTS:
    #successful login as admin
    def test_admin_login(self):
        user = User(username="Grae", email="grae@email.com", preference="AS")
        user.set_password('password')
        user.admin = True
        db.session.add(user)
        db.session.commit()

        response = self.login("Grae", "password")
        self.assertIn(b'Welcome Admin! Grae', response.data)

    #unsuccessful login as admin
    def test_nonadmin_login(self):
        user = User(username="Grae", email="grae@email.com", preference="AS")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()

        response = self.login("Grae", "password")
        self.assertNotIn(b'Welcome Admin! Grae', response.data)
    
    #admin delete user
    def test_delete(self):
        #create dummy users
        user1 = User(username="user1", email="user1@email.com", preference="AS")
        user1.set_password('password')
        choice1 = Choice(chooseSeries="Lambo", UserId=1, vote=1)
        user2 = User(username="user2", email="user2@email.com", preference="Lambo")
        user2.set_password('password')
        choice2 = Choice(chooseSeries="Lambo", UserId=2, vote=1)
        user3 = User(username="user3", email="user3@email.com", preference="GTR")
        user3.set_password('password')
        choice3 = Choice(chooseSeries="AS", UserId=3, vote=1)
        db.session.add(user1)
        db.session.add(choice1)
        db.session.add(user2)
        db.session.add(choice2)
        db.session.add(user3)
        db.session.add(choice3)
        db.session.commit()

        #login as admin
        administrator = User(username="admin", email="admin@email.com", preference="AS")
        administrator.set_password('password')
        administrator.admin = True
        db.session.add(administrator)
        db.session.commit()
        self.login("admin", "password")

        #check admin page and database for user1
        response = self.app.get('/hoster', follow_redirects = True)
        self.assertIn(b'user1', response.data)
        self.assertTrue(User.query.get(1))

        #admin deletes user1
        self.delete(1)
        
        #check admin page and database for user1
        response = self.app.get('/hoster', follow_redirects = True)
        self.assertNotIn(b'user1', response.data)
        self.assertFalse(User.query.get(1))

        #check admin page for votes from user1 (id = 1)
        self.assertNotIn(b'<td class="active" value="userid">1</td>', response.data)

#VOTING TESTS
    #Test vote for user that has not voted
    def test_vote(self):
        user = User(username="user", email="user@email.com", preference="AS")
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        self.login("user", "password")
        #self.select()




#CHANGES:

    #<td class="active" value="userid">1</td> IN ADMIN

    #you can access hoster page even if you're not an admin as long as you're logged in
    #deleting vote deletes user
    #admin page
    #UserIDs, not usernames in admin vote list

    if __name__ == '__main__':
        unittest.main()