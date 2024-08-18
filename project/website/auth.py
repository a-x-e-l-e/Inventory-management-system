from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from .models import Käyttäjä
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from functools import wraps
from flask import abort
from .forms import LoginForm, NewUserForm, SetPassword, ChangePassword

auth = Blueprint('auth', __name__)
serializer = current_app.config['serializer']

#Määritetään decorator, jonka avulla voidaan tarkistaa ennen käyttäjän päästämistä admin-sivulle, onko käyttäjä admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.admin:
                abort(403)  #Ei päästetä
            return f(*args, **kwargs)
        else:
            flash("Kirjaudu sisään nähdäksesi tämän sivun", category="error")
            return redirect(url_for("auth.login"))
    return decorated_function

#Luodaan token, jonka avulla käyttäjä voi asettaa salasanansa
def generate_password_token(email):
    return serializer.dumps(email, salt='set-password-salt123')

#Tarkistetaan token ja sen voimassaolo (voimassa yhden tunnin)
def validate_password_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='set-password-salt123', max_age=expiration)
    except Exception as e:
        return None
    return email

#Vain admin-käyttäjän käytössä oleva sivu, jossa hän voi selata, luoda, ja poistaa käyttäjiä (muttei kuitenkaan itseään).
#Onnistuneen käyttäjän luonnin yhteydessä luodaan linkki, jonka admin voi lähettää käyttäjälle.
#Linkin kautta käyttäjä voi asettaa itselleen haluamansa salasanan.
@auth.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_page():
    users = Käyttäjä.query.all()

    select_list = []

    form = NewUserForm()

    if users: 
        for user in users:
            select_list.append((user.id, f"{user.etunimi} {user.sukunimi} | {user.sähköposti}"))

    if select_list:
        form.select.choices = select_list
    else:
        form.select.choices = [("", "Ei käyttäjiä")]

    if request.method == 'POST' and form.new_or_browse.data == 'new' and form.validate_on_submit():
        
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if Käyttäjä.query.filter_by(sähköposti=email).first():
            flash('Sähköpostiosoite on jo käytössä.', 'error')
            return redirect(url_for('auth.admin_page'))
        elif password1 == password2:
            password_hash = generate_password_hash(password1)
            new_user = Käyttäjä(etunimi=firstname, sukunimi=lastname, sähköposti=email, salasana_hash=password_hash)
            db.session.add(new_user)
            try:
                db.session.commit()

                token = generate_password_token(email)
                set_password_url = url_for('auth.set_password', token=token, _external=True)
                flash(f"Uusi käyttäjä luotu!", "success")
                return render_template("generated_link2.html", set_password_url=set_password_url)
            except Exception as e:
                flash('Käyttäjän luominen ei onnistunut: ei voitu kirjoittaa tietokantaan.', 'error')
                return redirect(url_for('auth.admin_page'))
        else:
            flash('Salasanat eivät täsmää.', 'error')
            return redirect(url_for('auth.admin_page'))
        
    elif request.method == 'POST' and form.new_or_browse.data == 'browse' and form.validate_on_submit():
        userID = form.select.data

        user_to_be_deleted = Käyttäjä.query.get(userID)
        if user_to_be_deleted:
            if user_to_be_deleted.admin:
                flash('Admin-käyttäjää ei voida poistaa.', 'error')
                return redirect(url_for('auth.admin_page'))
            db.session.delete(user_to_be_deleted)
            try:
                db.session.commit()

                flash('Käyttäjä poistettu!', 'success_data')
                return redirect(url_for('auth.admin_page'))
            except Exception as e:
                flash('Ei voitu poistaa käyttäjää.', 'error')
                return redirect(url_for('views.home'))
        else:
            flash('Käyttäjää ei löytynyt', 'error')
            return redirect(url_for('auth.admin_page'))


    return render_template("admin_page2.html", users=users, form=form)

#Kirjaudu sisään -sivu, jossa tietysti tarkistetaan että käyttäjä on ensinnäkin olemassa,
#ja mikäli on, että syötetystä salasanasta luotu hash vastaa tietokantaan tallennettua hashia
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Käyttäjä.query.filter_by(sähköposti=email).first()
        if user:
            if check_password_hash(user.salasana_hash, password):
                flash('Sinut on kirjattu sisään.', category="success_data")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Väärä salasana.", category="error")
        else:
            flash("Käyttäjää ei näytä olevan olemassa.", category="error")

    return render_template("login2.html", form=form)

#Kirjautuessa ulos käyttäjä ohjataan takaisin login-sivulle
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sinut on kirjattu ulos.", category="success_data")
    return redirect(url_for('auth.login'))


#Linkki, joka luodaan uuden käyttäjän luonnin yhteydessä, johtaa tälle sivulle. 
#Tällä sivulla käyttäjä voi asettaa itselleen uuden salasanan.
@auth.route('/set-password/<token>', methods=['GET', 'POST'])
def set_password(token):
    form = SetPassword()
    email = validate_password_token(token)
    if not email:
        flash('Token ei kelpaa.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST' and form.validate_on_submit():
        new_password1 = form.password1.data
        new_password2 = form.password2.data
        user = Käyttäjä.query.filter_by(sähköposti=email).first()
        if user and new_password1 == new_password2:
            new_password_hash = generate_password_hash(new_password1)
            user.salasana_hash = new_password_hash
            try:
                db.session.commit()
                flash('Salasanan asettaminen onnistui. Voit nyt kirjautua sisään.', 'success_data')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash('Toiminto epäonnistui: ei voitu kirjoittaa tietokantaan.', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Jotakin meni vikaan.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template("set_password2.html", sähköposti=email, form=form)

#Tili-sivu, jolla käyttäjä näkee tietoja tilistään, ja voi myös halutessaan vaihtaa salasanansa
@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ChangePassword()

    old_password = form.old_password.data
    new_password1 = form.password1.data
    new_password2 = form.password2.data

    if request.method == "POST" and not check_password_hash(current_user.salasana_hash, old_password) and not form.validate_on_submit():
            form.old_password.errors.append("Syötä nykyinen salasanasi.")
            return render_template('account2.html', form=form)

    if request.method == "POST" and form.validate_on_submit():
        if not check_password_hash(current_user.salasana_hash, old_password):
            form.old_password.errors.append("Syötä nykyinen salasanasi.")
            return render_template('account2.html', form=form)
        elif check_password_hash(current_user.salasana_hash, old_password) and new_password1 == new_password2:
            new_password_hash = generate_password_hash(new_password1)
            current_user.salasana_hash = new_password_hash
            try:
                db.session.commit()

                flash('Salasanan päivitys onnistui.', 'success_data')
                return redirect(url_for('auth.account'))
            except Exception as e:
                flash('Toiminto epäonnistui: ei voitu kirjoittaa tietokantaan.', 'error')
                return redirect(url_for('auth.account'))
        else:
            flash('Väärä nykyinen salasana, tai uudet salasanat eivät täsmää.', 'error')
            return redirect(url_for('auth.account'))

    return render_template('account2.html', current_user=current_user, form=form)

