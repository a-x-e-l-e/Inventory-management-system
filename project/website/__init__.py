from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/{DB_NAME}'
    # !! VAIHDA TÄMÄ SECRET KEY ENNEN KÄYTTÖÄ / CHANGE THIS SECRET KEY BEFORE USING THE PROJECT !!
    app.secret_key = '89bc48bae543ff81044f849735d7427d7398ece1b1782028997ce75a8df6fcac'

    app.app_context().push()

    serializer = URLSafeTimedSerializer(app.secret_key)
    app.config['serializer'] = serializer

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Tavara, Hanke, Käyttäjä

    with app.app_context():
        db.create_all()
        # Käynnistettäessä ensimmäistä kertaa, luodaan admin-tili default-salasanoineen
        #Vaihda salasana hetimmiten
        if not Käyttäjä.query.filter_by(admin=True).first():
            admin_password_hash = generate_password_hash('adminpassword999')
            admin = Käyttäjä(sähköposti='admin', salasana_hash=admin_password_hash, etunimi="Admin", sukunimi="Admin", admin=True)
            db.session.add(admin)
            try:
                db.session.commit()
            except Exception as e:
                print("Jotakin meni vikaan. Varmista, että tietokantaan voidaan kirjoittaa.")

    login_manager = LoginManager()
    #Jos käyttäjä ei ole kirjautunut, näytetään login-sivu
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Kirjaudu sisään nähdäksesi tämän sivun."
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Käyttäjä.query.get(int(id))

    return app
