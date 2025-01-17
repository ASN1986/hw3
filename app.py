from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect

from form import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '2084c51ce11c3ed60044c00605760bed8e843a6ab980b7ca44b5219e3c656302'

csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///registration_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        exist_user = User.query.filter(
            (User.firstname == firstname) or (User.lastname == lastname) or (User.email == email)
        ).first()
        if exist_user:
            error_msg = 'Username or email already exists.'
            form.firstname.errors.append(error_msg)
            return render_template('register.html', form=form)
        new_user = User(firstname=firstname, lastname=lastname,
                        email=email)
        new_user.set_pass(password)
        db.session.add(new_user)
        db.session.commit()
        success_msg = 'Registration successful!'
        return success_msg
    return render_template('register.html', form=form)


@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    users = User.query.all()
    return f'{list(users)}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)