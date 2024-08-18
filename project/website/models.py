from . import db
from flask_login import UserMixin

class Käyttäjä(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sähköposti = db.Column(db.String(200), unique=True)
    salasana_hash = db.Column(db.String(200))
    etunimi = db.Column(db.String(200))
    sukunimi = db.Column(db.String(200))
    admin = db.Column(db.Boolean, default=False)

class Tavara(db.Model):
    tavaraID = db.Column(db.Integer, primary_key=True)
    tavaraNimi = db.Column(db.String(200))
    tavaraMalli = db.Column(db.String(200))
    tavaraValmistaja = db.Column(db.String(200))
    voidaanHeittääPoisAikaisintaan = db.Column(db.String(200))
    takuuPäättyy = db.Column(db.String(200))
    omistajaNimi = db.Column(db.String(200))
    omistajaSähköposti = db.Column(db.String(200))
    käyttäjäNimi = db.Column(db.String(200))
    käyttäjäSähköposti = db.Column(db.String(200))
    hankeID = db.Column(db.Integer, db.ForeignKey('hanke.hankeID'))

class Hanke(db.Model):
    hankeID = db.Column(db.Integer, primary_key=True)
    hankeNimi = db.Column(db.String(200))
    projektiPäällikkö = db.Column(db.String(200))
    aloitusPvm = db.Column(db.String(200))
    loppumisPvm = db.Column(db.String(200))
    tavarat = db.relationship('Tavara')