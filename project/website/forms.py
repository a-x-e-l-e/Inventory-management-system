from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Optional

class LoginForm(FlaskForm):
    email = StringField("Sähköposti", validators=[DataRequired(message="Täytä tämä kenttä."), Length(min=1, max=50, message="Täytä tämä kenttä")])
    password = PasswordField("Salasana", validators=[DataRequired(message="Täytä tämä kenttä."), Length(min=1, max=50, message="Täytä tämä kenttä")])

    submit = SubmitField("Kirjaudu sisään")


class NewItem(FlaskForm):
    item_name = StringField("Tavaran nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    item_model = StringField("Tavaran malli", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    item_manufacturer = StringField("Tavaran valmistaja", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    can_be_thrown_away = DateField("Voidaan heittää pois aikaisintaan", validators=[DataRequired(message="Valitse päivämäärä.")])
    warranty = DateField("Takuu päättyy", validators=[DataRequired(message="Valitse päivämäärä.")])

    owner_name = StringField("Tavaran omistajan nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    owner_email = StringField("Tavaran omistajan sähköposti", validators=[DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")])

    user_name = StringField("Tavaran käyttäjän nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    user_email = StringField("Tavaran käyttäjän sähköposti", validators=[DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")])

    project_name = StringField("Hankkeen nimi", validators=[DataRequired(), Length(min=1, max=50)])
    project_manager = StringField("Projektipäällikön nimi", validators=[DataRequired(), Length(min=1, max=50)])
    start_date = DateField("Hankkeen aloituspäivämäärä", validators=[DataRequired()])
    end_date = DateField("Hankkeen loppumispäivämäärä", validators=[DataRequired()])

    new_or_old = RadioField("", choices=[("new", "Luo uusi"),("not-new", "Käytä olemassaolevaa")], validators=[DataRequired()], name="radio-buttons")

    select = SelectField("Valitse")

    def adjust_validators(self):
        self.select.validators = []

        self.project_name.validators = []
        self.project_manager.validators = []
        self.start_date.validators = [Optional()]
        self.end_date.validators = [Optional()]

        if self.new_or_old.data == "new":
            self.project_name.validators = [DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")]
            self.project_manager.validators = [DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")]
            self.start_date.validators = [DataRequired(message="Valitse päivämäärä.")]
            self.end_date.validators = [DataRequired(message="Valitse päivämäärä.")]
        elif self.new_or_old.data == 'not-new':
            self.select.validators = [DataRequired("Valitse hanke, tai jos hankkeita ei ole, luo uusi")]

    def validate(self, extra_validators=None):
        self.adjust_validators()
        if extra_validators is None:
            extra_validators = {}
        return super(NewItem, self).validate(extra_validators=extra_validators)
    

class EditItem(FlaskForm):
    item_name = StringField("Tavaran nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    item_model = StringField("Tavaran malli", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    item_manufacturer = StringField("Tavaran valmistaja", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    can_be_thrown_away = DateField("Voidaan heittää pois aikaisintaan", validators=[DataRequired(message="Valitse päivämäärä.")])
    warranty = DateField("Takuu päättyy", validators=[DataRequired(message="Valitse päivämäärä.")])

    owner_name = StringField("Tavaran omistajan nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    owner_email = StringField("Tavaran omistajan sähköposti", validators=[DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")])

    user_name = StringField("Tavaran käyttäjän nimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    user_email = StringField("Tavaran käyttäjän sähköposti", validators=[DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")])

    project_name = StringField("Hankkeen nimi", validators=[DataRequired(), Length(min=1, max=50)])
    project_manager = StringField("Projektipäällikön nimi", validators=[DataRequired(), Length(min=1, max=50)])
    start_date = DateField("Hankkeen aloituspäivämäärä", validators=[DataRequired()])
    end_date = DateField("Hankkeen loppumispäivämäärä", validators=[DataRequired()])


class NewUserForm(FlaskForm):
    first_name = StringField("Etunimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    last_name = StringField("Sukunimi", validators=[DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")])
    email = StringField("Sähköposti", validators=[DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")])
    password1 = PasswordField("Salasana", validators=[DataRequired(message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä."), Length(min=8, max=50, message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä.")])
    password2 = PasswordField("Vahvista salasana", validators=[DataRequired(), EqualTo("password1", message="Salasanat eivät täsmänneet.")])

    new_or_browse = RadioField("", choices=[("new", "Luo uusi"),("browse", "Selaa käyttäjiä")], validators=[DataRequired()], name="radio-buttons")

    select = SelectField("Valitse")

    def adjust_validators(self):
        self.select.validators = []

        self.first_name.validators = []
        self.last_name.validators = []
        self.email.validators = []
        self.password1.validators = []
        self.password2.validators = []

        if self.new_or_browse.data == "new":
            self.first_name.validators = [DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")]
            self.last_name.validators = [DataRequired(message="Täytä tämä kenttä käyttäen 1-50 merkkiä."), Length(min=1, max=50, message="Täytä tämä kenttä käyttäen 1-50 merkkiä.")]
            self.email.validators = [DataRequired(message="Täytä tähän kenttään kelvollinen sähköpostiosoite."), Email(message="Täytä tähän kenttään kelvollinen sähköpostiosoite.")]
            self.password1.validators = [DataRequired(message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä."), Length(min=8, max=50, message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä.")]
            self.password2.validators = [DataRequired(message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä."), EqualTo("password1", message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä.")]
        elif self.new_or_browse.data == 'browse':
            self.select.validators = [DataRequired()]

    def validate(self, extra_validators=None):
        self.adjust_validators()
        if extra_validators is None:
            extra_validators = {}
        return super(NewUserForm, self).validate(extra_validators=extra_validators)
    
class SetPassword(FlaskForm):
    password1 = PasswordField("Salasana", validators=[DataRequired(message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä."), Length(min=8, max=50, message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä.")])
    password2 = PasswordField("Vahvista salasana", validators=[DataRequired(message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä."), EqualTo("password1", message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä.")])

class ChangePassword(FlaskForm):
    old_password = PasswordField("Nykyinen salasana", validators=[DataRequired(message="Syötä nykyinen salasanasi.")])
    password1 = PasswordField("Salasana", validators=[DataRequired(message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä."), Length(min=8, max=50, message="Syötä salasana, jossa on vähintään 8 ja enintään 50 merkkiä.")])
    password2 = PasswordField("Vahvista salasana", validators=[DataRequired(message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä."), EqualTo("password1", message="Salasanat eivät täsmänneet tai salasanan pituus ei ollut 8-50 merkkiä.")])