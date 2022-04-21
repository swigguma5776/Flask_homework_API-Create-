from re import template
from flask import Blueprint, render_template, request, redirect, url_for, flash
from homework_inventory.models import User, db 
from homework_inventory.forms import UserLoginForm

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account: {email}", 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    return render_template('signin.html')