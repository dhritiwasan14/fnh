'''

Handling the general imports

'''


from flask import Flask, render_template, request, render_template, flash, redirect, session, url_for, request, g
from forms import *
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import dirCurrent


'''

Application Configuration

'''

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(dirCurrent, 'tmp'))


#placed here to prevent circular imports
from models import *
'''

Controller - Handling the routes.

'''

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        return None
    form = SearchForm(request.form)
    return render_template("home.html", form=form )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        if form.validate:
            username = form.username
            password = form.password
            email = form.email
            user = User(username, password, email)
            user.parse_json()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('home')
        

@app.errorhandler(404)
def error404(error):
    return render_template("error/404.html"), 404

'''

Handling the launch of application

'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)