from tkinter.tix import Tree
from apscheduler.schedulers.background import BackgroundScheduler
from myapp.views import  kontrola

def start():
	s = BackgroundScheduler()
	
	s.add_job(kontrola, "interval", minutes=0.1,  replace_existing=True)
	s.start()

