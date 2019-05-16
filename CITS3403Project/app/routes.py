from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User, Brand, Choice, Record
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/index')
@login_required
def index():
    car1 = []
    for i in db.session.query(Brand.carSeries).all():
        car1.append(i[0])

    carVote = {}

    for i in db.session.query(Choice.chooseSeries).all():
        carVote[i[0]] = carVote.get(i[0], 0) + 1


    flash("Voting result " + str(carVote))
    carValue = carVote.values()

    user = []
    for i in db.session.query(Choice.UserId).all():
        user.append(i[0])

    for i in user:
        if current_user.id in user:
            choice = Choice(chooseSeries=select, UserId = current_user.id, vote=1) 
            flash("current user have voted")
            break
        else:
            flash("not voted yet")
            choice = Choice(chooseSeries=select, UserId = current_user.id, vote=0) 
            break

    tableCar=[]
    tableVote=[]
    for i in db.session.query(Choice.chooseSeries).all():
        tableCar.append(i[0])

    for i in db.session.query(Choice.vote).all():
        tableVote.append(i[0])

    tableUser = []
    for i in db.session.query(User).join(Choice):
        tableUser.append(i)

    # flash(tableUser)
    # flash(tableCar)
    # flash(tableVote)
    a = zip(tableUser,tableCar,tableVote)

    return render_template('index.html',title='Home', car1=car1, carVote = carVote, choice=choice, a=a, carValue=carValue)


@app.route("/select" , methods=['GET', 'POST'])
def select():
    select = request.form.get('car_select')

    user = []
    for i in db.session.query(Choice.UserId).all():
        user.append(i[0])

    for i in user:
        if current_user.id in user:
            return render_template('vote.html', select=select)
        else:
            choice = Choice(chooseSeries=select, UserId = current_user.id, vote=1) 
            db.session.add(choice)
            db.session.commit()
            flash("Voted:" + str(select))

            return render_template('vote.html', select=select, choice=choice)


if __name__ == "__main__":
    app.run(debug=True)

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Brand, db.session))
admin.add_view(ModelView(Choice, db.session))
admin.add_view(ModelView(Record, db.session))

@app.route('/hoster')
@login_required
def hoster():
    users = User.query.all()

    choose = db.session.query(Choice).join(User)

    return render_template('admin.html', users=users, choose=choose)

@app.route('/delete_user/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    
    user = User.query.get_or_404(id)
    # if user.username != current_user:
    #     abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('One row has been deleted!')

    return redirect(url_for('hoster'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if User.is_admin(current_user):
            return redirect(url_for('hoster'))
        else:
	        return redirect(url_for('select'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if User.is_admin(current_user):
            return redirect(url_for('hoster'))
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

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

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

###this is static url cache buster, updating css once refresh the page
import os
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
