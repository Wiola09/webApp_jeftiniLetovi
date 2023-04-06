
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, \
    SelectMultipleField, HiddenField, EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired, ValidationError
from flask_ckeditor import CKEditorField

from konstante import TODAY, TOMOROW, MESEC_KASNIJE

"%d""/""%m""/""%Y"
# #WTForm

class UnesiPodateZaPretraguForm(FlaskForm):
    date_from = DateField('Departure Date From', format='%Y-%m-%d', default=TOMOROW, validators=[DataRequired()])
    date_to = DateField('Departure Date To', format='%Y-%m-%d', default=MESEC_KASNIJE, validators=[DataRequired()])
    adults = SelectField("Nuber Of Adults", choices=[1, 2, 3, 4, 5, 6], default=2, validators=[DataRequired()])
    children = SelectField("Nuber Of Children", choices=[0, 1, 2, 3, 4, 5, 6], default=0, validators=[DataRequired()])
    nights_in_dst_from = IntegerField("Min Nights At The Dest.", default=1, validators=[NumberRange(min=0, message="Morate unijeti pozitivan broj.")])
    polaziste = SelectField("Departure Location", default="BEG", choices=["BEG"])
    destinacija = SelectField("Destination Location", default="", choices=[])
    nights_in_dst_to = IntegerField("Max Nights At The Dest.", default=3, validators=[NumberRange(min=0)], render_kw={"style": "white-space: pre-wrap"})


    # datum_vreme_kraja = DateField("Датум и време краја", format='%Y-%m-%d', default=TOMOROW, validators=[DataRequired()])
    submit_flight_data = SubmitField("Send Flight Data")
    delete_destination = SubmitField("Delete Destination")

# Koristi "placeholder", umesto default=
class UnesiGrad(FlaskForm):
    grad = StringField("Pretraga grada", validators=[DataRequired()],
                       render_kw={"placeholder": "Enter text here"
                                  })
    pretraži_grad = SubmitField("Pretraži grad")

# # Verzija 3 kada se klikne na polje oznaci se vrednost u njemu, to vazi i za pocetnu vrednost, ali i za kasnije
# class UnesiGrad(FlaskForm):
#     grad = StringField("Pretraga grada", default="Unesite ime grada", validators=[DataRequired()],
#                        render_kw={"onfocus": "this.select();",
#                                   "onclick": "if (this.value=='Unesite ime grada') this.value='Unesite ime grada'",
#                                   "onmouseup": "if (this.value=='') this.value='Unesite ime grada'"
#                                   })
#     pretraži_grad = SubmitField("Pretraži grad")


# Vrzija 2 forme gde stoji samo tekst u polju za unos, ali kad se klikne na polje taj tekst se obrise
# class UnesiGrad(FlaskForm):
#     grad = StringField("Pretraga grada", default="Unesite ime grada", validators=[DataRequired()],
#                        render_kw={"onclick": "this.select()", "onfocus": "if (this.value=='Unesite ime grada') this.value=''"})
#     pretraži_grad = SubmitField("Pretraži grad")

    # Vrzija 1 forme gde stoji samo tekst u polju za unos
# class UnesiGrad(FlaskForm):
#     grad = StringField("Pretraga grada", default="Unesite ime grada", validators=[DataRequired()], render_kw={"onclick": "this.select()", "onfocus": "if (this.value=='Unesite ime grada') this.value=''"})
#     pretraži_grad = SubmitField("Pretraži grad")



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

