from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SubmitField, RadioField, IntegerField, StringField, PasswordField, HiddenField, FormField
from wtforms.validators import ValidationError, DataRequired
from app.models import User
import random
from flask_babel import lazy_gettext as _l

class ConsentForm(FlaskForm):
    birthyears = [(str(i), str(i)) for i in range(1,117)]
    age = SelectField(_l('What is your age?'), choices=birthyears)
    gender = SelectField(_l('What is your gender?'), choices=[('1',_l('Female')), ('0',_l('Male'))], validators=[DataRequired()])

class Form2(FlaskForm):
    birthyears = [(str(i), str(i)) for i in range(1,117)]
    age = SelectField(_l('What is your age?'), choices=birthyears)
    citizen = SelectField(_l('Are you a Tunisian Citizen?'), choices=[('1', _l('Yes')),('0',_l('No'))])
    gender = SelectField(_l('What is your gender?'), choices=[('1',_l('Female')), ('0',_l('Male'))], validators=[DataRequired()])

class Form3(FlaskForm):
    ed = SelectField(_l('What is your highest education qualification?'), choices=[('0', _l('No education')), ('0', _l('Elementary')), ('0', _l('Preparatory/Basic')), ('0', _l('Secondary')), ('1', _l('BA')), ('1', _l('MA')), ('99', _l('Decline to answer'))])
    allchoices=[('ariana', 'Ariana'), 
        ('beja', 'Beja'), 
        ('ben_arous', 'Ben Arous'), 
        ('bizerte', 'Bizerte'), 
        ('gabes', 'Gabes'), 
        ('gafsa', 'Gafsa'), 
        ('jendouba', 'Jendouba'), 
        ('kairouan', 'Kairouan'), 
        ('kasserine', 'Kasserine'), 
        ('kebili', 'Kebili'), 
        ('kef', 'Kef'), 
        ('mahdia', 'Mahdia'), 
        ('manouba', 'Manouba'), 
        ('medenine', 'Medenine'), 
        ('monastir', 'Monastir'), 
        ('nabeul', 'Nabeul'), 
        ('sfax', 'Sfax'),
        ('sidi_bouzid', 'Sidi Bouzid'), 
        ('siliana', 'Siliana'), 
        ('sousse', 'Sousse'), 
        ('tataouine', 'Tataouine'), 
        ('tozuer', 'Tozeur'), 
        ('tunis', 'Tunis'), 
        ('zaghouan', 'Zaghouan')]
    extent = len(allchoices) - random.randint(0,len(allchoices))
    choices = sorted(allchoices[extent:len(allchoices)])
    for i in range(0,extent):
        choices.append(allchoices[i])
    loc = SelectField(_l('Please select the governorate you live in (note the survey is only for those currently living in Tunisia)'), choices=choices, validators=[DataRequired()])
    reg = SelectField(_l('Are you registered to take part in the upcoming national elections?'), choices=[('1',_l('Yes')), ('0',_l('No')), ('0',_l('I am not sure'))], validators=[DataRequired()])
    phone = StringField(_l('Please provide a mobile number so that we can send you the details of our study, enter you in the prize raffle, and notify you when you win.'))
    
class InterestForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email Address'))
    phone = StringField(_l('Phone Number'), validators=[DataRequired()])

class AdminLogin(FlaskForm):
    pw = PasswordField('Password', validators=[DataRequired()])

class SurveyURLForm(FlaskForm):
    url = StringField('URL')
    updatedby = StringField('Updated by')
    lang = HiddenField()
    treatmento = HiddenField()
    id = HiddenField()
    
class SurveyForm(FlaskForm):
    arabic_treatment1 = FormField(SurveyURLForm)
    arabic_treatment2 = FormField(SurveyURLForm)
    arabic_treatment3 = FormField(SurveyURLForm)
    arabic_treatment4 = FormField(SurveyURLForm)
    arabic_control = FormField(SurveyURLForm)
    french_treatment1 = FormField(SurveyURLForm)
    french_treatment2 = FormField(SurveyURLForm)
    french_treatment3 = FormField(SurveyURLForm)
    french_treatment4 = FormField(SurveyURLForm)
    french_control = FormField(SurveyURLForm)
    english_treatment1 = FormField(SurveyURLForm)
    english_treatment2 = FormField(SurveyURLForm)
    english_treatment3 = FormField(SurveyURLForm)
    english_treatment4 = FormField(SurveyURLForm)
    english_control = FormField(SurveyURLForm)
