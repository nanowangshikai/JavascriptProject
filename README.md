# Super Cars Ranked!

A web application designed to compare the relative popularities of some of the worlds most, and ranks the results of the worlds most celebrated Super Cars. The application uses a polling system, where user votes are tallied for each car and displayed as a bar chart once the user has submitted their polled response.

## Architecture of The Application
**Model View Controller:**
The architecture of our web application is most easily explained using a 'Model View Controller (MVC)'. Within this architecture: 

* 'Model' represents the schema and databases from which the controller retrieves data from
* 'View' represents the visual representations of the data drawn from these models
* 'Controller' represents the initialisation, routing and execution code that act as an intermediary between the 'Model' and 'View'

**Model (models.py):**
Our web application stores its data using SQLite3 and SQLAlchemy within the following model frameworks.

* _User:_ This model stores information about the users in the database. This information includes a primary key id, email, username, car preference and password hash, as well as some keys linking it to other tables. It also specifies admin rights and password possessed by the user, which define what pages they can access

* _Brand:_ Brand stores the brands of cars which will be used for ranking in the app. These brands are linked to the *Choice* model which refers to these brands using a foreign key

* _Choice:_ The choice model is what links the *User* to their selected *Brand* of car. It also holds a *'vote'* variable which holds a boolean specifying whether the user has had their vote or not, important in determining whether they are allowed to vote

Below is an example of our *User* model:

        class User(UserMixin, db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), index=True, unique=True)
            email = db.Column(db.String(120), index=True, unique=True)
            admin = db.Column(db.Boolean, default=False, nullable=False)
            preference = db.Column(db.String(320))
            password_hash = db.Column(db.String(128))
            record_id = relationship("Record", backref="user", lazy="dynamic")
            choice_id = relationship("Choice", backref="user", lazy="dynamic")


            def is_admin(self):
                return self.admin

            def set_password(self, password):
                self.password_hash = generate_password_hash(password)

            def check_password(self, password):
                return check_password_hash(self.password_hash, password)

            def __repr__(self):
                print('<admin or not {}>'.format(self.admin))
                return '{}'.format(self.username)

**Control (routes.py):**
Control Architecture in our application is mainly handled from within the Python/Flask routes file. This file handles 'GET' and 'POST' requests, and assigns each url in the application to a function known as a 'controller action'. These functions transform data from the models and pass this information into the 'View' files using Jinja2, and vice versa in responding to requests from these view functions.

Our app has the following controller actions:

* _home:_ Returns a View of the Homepage
* _index:_ This function tallies user votes based on data retrieved from the 'Choice' model and returns a the 'Index' View which displays this information graphically. The function also includes measures to prevent a user that has already voted, is not logged in, or has admin privilages from accessing the 'Index' View.
* _select:_ This function is called from the 'Index' View when a user selects their choice of car. Given that the user is not an admin, and they haven't voted aleady, the function adds the users vote to the 'Choice' Model, and the user is directed to a 'Vote' View, which confirms their vote, with the option to go back to the 'Index' View and see the updated graphical results
* _hoster:_ This function joins the Choice and User models in SQLite, and providing the user is an admin, redirects them to the 'Admin' View, passing these joined tables as well as information from the 'Brand' model
* _addVote:_ This function gives those with admin privilages the ability to add new types of cars to pick from in the 'Brand' model, recieving a POST request from a form on the 'Admin' View, and updating the 'Brand' model based on this request
* _deleteBrand:_ This function does essentially the opposite to the 'addVote' function, allowing the admin to remove car options from the 'Admin' View
* _delete-user:_ This function gives the admin the ability to delete registered users from the 'User' Model, based on form data recieved from a POST request on the 'Admin' View. It will in turn delete all votes on the 'Choice' Model associated with the deleted user
* _login:_ Given that a user is not already logged in, this function deals with passed information from the Flask 'LoginForm()' in the 'Login' View. Providing this user is registered, and valid information is entered, the function returns either the 'Index' View, or 'Admin' View, based on their privilages
* _logout:_ Logs a user out and returns the 'Index' View
* _register:_ Providing that the user is not already logged in, takes information from the Flask 'RegistrationForm()', and providing valid information is entered, and no duplicates being in database, adds the new user to the 'User' Model, and redirects them to the 'Login' View. 
Here is an example of the 'register' controller function:
        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            form = RegistrationForm()
            if form.validate_on_submit():
                user = User(username=form.username.data, email=form.email.data, preference=form.preference.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('login'))
            
            return render_template('register.html', title='Register', form=form)

**View (Templates/Static):**
This includes all visually presented code in the application, consisting of templates (HTML) and static (CSS/JavaScript).

Our app includes the following templates:
* _base:_ This is the base template from which all the others extend using Jinja2. The head of the template links various stylesheets and scripts including static files, BootStrap, AJAX and JQuery. Additionally the template displays a header from which users can navigate the web app, and Jinja2 functions to display flashed messages from any of the 'controller functions'
* _home:_ Displays a slideshow of cars, acting as an aesthetic welcome screen for users when they first enter the web app. From this page they have the option to Sign Up, or Log In
* _register:_ From this template the user is presented with a forms as a part of the Flask 'RegisterForm' package. As the user fills in these forms, they are prompted by validators defined in the 'forms.py' file to enter the correct information. Once all forms are correctly filled out the user can submit the 'RegisterForm' using the 'Submit' button, posting this back to the controller functions
* _login:_ Similar to 'Register' template, this template prompts users to correctly fill out forms based on validators defined in the 'forms.py' file. This information is posted upon pressing the 'Submit' button
* _index:_ This page has 2 major purposes. The first being to provide an avenue for the user to place their votes, with car options being displayed as a series of buttons linked to seperate forms that pass the value of the form (the Car Series) back to the 'controller functions' where they are passed to the 'Choice' Model. The second purpose is to display the data tallied from the 'Choice' Model into a graphical representation. In our app we displayed a Bar Chart, ordered from tallest to shortest, left to right. Also displayed is a record in the form of a table showing each user and their corresponding vote information
* _admin:_ Given that the user has admin permissions, this template displays a record of all users registered on the app, as well as a seperate record of each users vote information. For both of these records the user is displayed with the option to delete the user and/or their vote (so long as they are not another admin). Additionally, there are drop down displays controlled by JavaScript which when opened give the admin the option to add new options (Car Series) to the poll, as well as delete the existing ones
* _vote:_ The 'Vote' View displays the user with a confirmation of their vote, as well as a button redirecting back to the 'Index' View such that the user can see the results of the poll

Here is an example of a small template model used in our web app (vote.html):
        {% extends "base.html" %}

        {% block content %}

            <div class="info">
                <p>This is the Voting Page</p>
                <p>Current User : {{current_user.username}}</p>
                <p>Voted {{select}}</p>

                <a href="{{ url_for('index') }}"><button>Back to Voting page</button></a>
            </div>

        {% endblock %}

Our app also includes the following static files:
* _CSS:_ All style information is stored in here. Additionally to CSS, we used BootStrap to style our page
* _Javascript/JQuery:_ In here we provide some basic functionality for the client-side of the web app. For example for the drop down menus on the admin page, we used JQuery to register the click, and trigger the drop down event.

Here is an example of our CSS (style.css):
        body{
            background: url('Photo/mountain.jpg');
            background-repeat: no-repeat;
            background-size: cover;
            height: 100%;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
            font-family: poppins;
        }

        header{
            background: rgb(43, 44, 43);
            top: 0;
            left: 0; 
            width: 100%;
            box-sizing: border-box;
            padding: 0 40px;
            position: absolute;
            opacity: .9;
            
        }

## Launching The Application

**Install Python:**
`python3`
`exit()`

**Set Up Virtual Environment:**
`python3 -m venv venv`
`pip3 install virtualenv`
`virtualenv venv`
`source venv/bin/activate`

**Change Directory To Project Folder:**
`cd (INSERT PROJECT FOLDER PATH LOCATION)`

**Set Up Flask:**
`pip install flask`
`export FLASK_APP=main.py`

**Install Relevant Modules:**
`pip install flask_sqlalchemy`
`pip install flask_migrate`
`pip install flask_login`
`pip install flask_wtf`
`pip install flask_admin`

**Run The App:**
`flask run`

The app should now be running on [http://localhost:5000](http://localhost:5000), entered into any browser

**Additional Controls:**
Stop App: `^C`
Exit Environment: `deactivate`


## Running Unit Tests:
Our Web App has 19 Unit Tests that comprehensively test the functionality of our web
Here's a few examples:

*This test runs through possible ways the Registration form could be incorrectly completed, and ensures it behaves as expected*
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

*this test checks that the delete user function performs effectively*
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
*this test checks that a user cannot access the admin page by entering the relevant page into the url*
        #user tries to access admin page directly through url
        def test_nonadmin_url(self):
            user = User(username="Grae", email="grae@email.com", preference="AS")
            user.set_password('password')
            user.admin = False
            db.session.add(user)
            db.session.commit()

            self.login("Grae", "password")
            response = self.app.get('/hoster', follow_redirects = True)
            self.assertIn(b'Cannot access admin page directly', response.data)

To run unit tests, enter the following in Command Prompt:
`python -m unittest test.py`

To view all of tests go to 'tests.py'

## Authors

* **Grae Cumming and Nano Wang**

## Acknowledgments

* Built following the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by **Miguel Grinberg**.

* Special mention to [Amazing Transparent Login Form Just By Using HTML & CSS](https://www.youtube.com/watch?v=ooc6f1w6Mzg&fbclid=IwAR1TMVOS0lO7oIvU_wJpZZbzsckBGgA2W-eV5oZujLk4sk4AjllcDkXKwKc) by **DarkCode**
