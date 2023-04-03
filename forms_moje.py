
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, \
    SelectMultipleField, HiddenField, EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired, ValidationError
from flask_ckeditor import CKEditorField

from konstante import TODAY, TOMOROW, MESEC_KASNIJE

"%d""/""%m""/""%Y"
# #WTForm

class UnesiPodateZaPretraguForm(FlaskForm):
    date_from = DateField('Flight Date From', format='%Y-%m-%d', default=TOMOROW, validators=[DataRequired()])
    date_to = DateField('Flight Date To', format='%Y-%m-%d', default=MESEC_KASNIJE, validators=[DataRequired()])
    adults = SelectField("Nuber Of Adults", choices=[1, 2, 3, 4, 5, 6], default=2, validators=[DataRequired()])
    children = SelectField("Nuber Of Children", choices=[0, 1, 2, 3, 4, 5, 6], default=0, validators=[DataRequired()])
    nights_in_dst_from = IntegerField("Min Broj Nocenja", default=1, validators=[NumberRange(min=0, message="Morate unijeti pozitivan broj.")])
    polaziste = SelectField("Polaziste", default="BEG", choices=["BEG"])
    destinacija = SelectField("Destinacija", default="", choices=[])
    nights_in_dst_to = IntegerField("Max Broj Nocenja", default=3, validators=[NumberRange(min=0)])
    # datum_vreme_kraja = DateField("Датум и време краја", format='%Y-%m-%d', default=TOMOROW, validators=[DataRequired()])
    submit = SubmitField("Send Data")
    submit2 = SubmitField("Delete Destination")


class UnesiGrad(FlaskForm):
    grad = StringField("Pretraga grada", default="Unesite ime grada", validators=[DataRequired()])
    pretraži_grad = SubmitField("Pretraži grad")


# ne koristim ove dve forme, ec razbijen kod u html
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("SIGN ME UP!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")

