
from typing import List
from django import db
from django.shortcuts import render
from django.http import HttpResponse
from . models import uzivatele
from . forms import Můjformular
from django.http import HttpResponseRedirect
from . tridy import EmailSender
from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.message import Message
##################################################################################

t = EmailSender('smtp.gmail.com', 587, "sokolim@stredniskola.cz", "Dunajovice49")


seznam = [] #seznam pro uložení emailů které dostanou z databaze 
hodnoty =[] # zde jsi budu ukládat měnící se hodnoty 


 # test htmls = requests.get("http://54.146.28.204/", headers=headers )
#"https://jiho.ceskereality.cz/pronajem/byty/cast-ceske-budejovice-1/"



#Tanto funkce nacita data z daneho místa na dane webevé strance
##############################################################


def nacti_dat():
	headers = {
	 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}


	try:
		htmls = requests.get("http://54.146.28.204/", headers=headers )
		htmls = htmls.text
		b = BeautifulSoup(  htmls, "lxml")
		
		pocet_nemovitosti = b.find("div", class_ = "number").text
		pocet_nemovitosti = pocet_nemovitosti.strip()
		
		return pocet_nemovitosti
	except:
  		return "chyba"
 
########################################################################################




	



def Email_funkce( m , seznam):
	server =smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("sokolim@stredniskola.cz", "Dunajovice49")
	for i in seznam:
		server.sendmail("sokolim@stredniskola.cz", i,m )
	server.quit()
	


def Get_dat_fromDb(seznam):
	for i in uzivatele.objects.all():
		seznam.append(str(i))


def kontrola():
	first = nacti_dat()
	hodnoty.append(first)
	
	if len(hodnoty)==2:
		if hodnoty[0]!= hodnoty[1] and (hodnoty[0]!="chyba" or hodnoty[1]!="chyba"):
			hodnoty[0]=hodnoty[1]
			Get_dat_fromDb(seznam)
			Email_funkce( "dobry den zmena poctu nabidek "+ hodnoty[0], seznam)
			hodnoty.pop(1)

	
		



	






def index(request):
	submited = False
	if request.method =="POST":
		form = Můjformular(request.POST)
		if form.is_valid():
			form.save()
			text = form.cleaned_data["email"]
			seznam.append(text)
			t.Emailsend(seznam, "Dekuji za registraci aktualni pocet nemovitosi je "+ nacti_dat())
			seznam.clear()
			return HttpResponseRedirect("?submited=True")


	

			
	else:
		form = Můjformular
		if "submited" in request.GET:
			submited = True
	return render(request,"myapp/index.html", {"form":form, "submited":submited})








