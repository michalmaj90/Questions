from django import forms
from django.forms import ModelForm
from .validators import validate_email, validate_url, validate_year, validate_sex, validate_number
from exercises.models import GRADES, SchoolSubject, Message, StudentNotice

CONVERSION = (
    (1, "PLNtoUSD"),
    (2, "USDtoPLN"),
)

TOPPINGS = (
    ('olives', 'oliwki'),
    ('tomatoes', 'pomidory'),
    ('cheese', 'dodatkowy ser'),
    ('anchovies', 'anchovies'),
    ('onion', 'cebula')
)

BACKGROUND_COLOR = (
    ('black', 'black'),
    ('white', 'white'),
    ('red', 'red'),
    ('yellow', 'yellow'),
    ('blue', 'blue')
)

class StudentSearchForm(forms.Form):
    last_name = forms.CharField()

class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    class_name = forms.CharField()
    year_of_birth = forms.IntegerField(validators=[validate_year])

class CurrencyForm(forms.Form):
    currency = forms.FloatField()
    conversion = forms.IntegerField(widget=forms.Select(choices=CONVERSION))

class AddGradesForm(forms.Form):
    student = forms.CharField()
    subject = forms.CharField()
    grade = forms.FloatField(widget=forms.Select(choices=GRADES))

class PizzaToppingsForm(forms.Form):
    toppings = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=TOPPINGS)

class PresenceListForm(forms.Form):
    student = forms.CharField()
    day = forms.DateField(widget=forms.HiddenInput)
    present = forms.NullBooleanField()

class BackgroundColorForm(forms.Form):
    background_color = forms.CharField(widget=forms.RadioSelect(choices=BACKGROUND_COLOR))

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class PersonalDataForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(validators=[validate_email])
    www = forms.CharField(validators=[validate_url])

class CheckSexForm(forms.Form):
    first_name = forms.CharField(validators=[validate_sex])
    last_name = forms.CharField()

class StringNumberForm(forms.Form):
    word = forms.CharField()
    number = forms.IntegerField(validators=[validate_number])

class AddSubjectForm(ModelForm):
    class Meta:
        model = SchoolSubject
        fields = ['name', 'teacher_name']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['date_sent']

class StudentNoticeForm(ModelForm):
    class Meta:
        model = StudentNotice
        fields = ['from_who', 'to', 'content']

class AddUserForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(validators=[validate_email])

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label='Wprowadź nowe hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Wprowadź ponownie nowe hasło', widget=forms.PasswordInput)
