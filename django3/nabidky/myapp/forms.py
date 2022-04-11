
from django import forms
from django.forms import ModelForm
from . models import uzivatele


class Můjformular(ModelForm):
	class Meta:
		model = uzivatele
		fields = ("jmeno", "email")


		