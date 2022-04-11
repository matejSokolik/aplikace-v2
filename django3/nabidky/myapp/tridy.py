import smtplib
from typing import List






class EmailSender:
	def __init__(self, host: str, port: int, emailofsender: str, passvd: str ) -> None:
		self.host = host
		self.port = port
		self.emailofsender= emailofsender
		self.passvd  = passvd
	

	def Emailsend(self, emails: List, mess: str):
		server =smtplib.SMTP(self.host, self.port)
		server.starttls()
		server.login(self.emailofsender, self.passvd)
		for i in emails:
			server.sendmail("sokolim@stredniskola.cz", i,mess )
		emails.clear()










