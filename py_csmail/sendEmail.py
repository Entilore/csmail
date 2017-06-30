#!/usr/bin/env python

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MIMEMail(MIMEMultipart):
	def __init__(self, subject, message, exp, from_address=None):
		MIMEMultipart.__init__(self)
		if not from_address:
			from_address = exp["email"]
		self["Subject"] = subject
		self["From"] = from_address

		self.exp = exp

		self.attach(MIMEText(message, "plain", "utf-8"))

		self.mailserver = smtplib.SMTP_SSL(exp["smtp"])
		self.mailserver.login(self.exp["email"], self.exp["password"])

	def sendMails(self, dests):
		for d in dests:
			self.send(d)

	def send(self, dest):
		self["To"] = dest

		self.mailserver.sendmail(self.exp["email"], dest, self.as_string())

	def __del__(self):
		self.mailserver.quit()
