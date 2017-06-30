#!/usr/bin/env python

import os
import yaml
import re
from py_csmail.definitions import ROOT_DIR

EMAILS_PATH = os.path.join(ROOT_DIR, 'data/accounts.yml')

EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
SMTP_RE = re.compile(r"^([\da-z\.-]+)\.([a-z\.]{2,6})(\:\d+)?")

__emailsData = None


def _assert_true(condition, message=None):
	if not condition:
		raise ValueError(message)


def __get_emails():
	global __emailsData
	if __emailsData:
		return __emailsData
	data = None

	DATA_DIR = "/".join(EMAILS_PATH.split("/")[:-1])
	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)

	data = []
	try:
		with open(EMAILS_PATH, "r") as f:
			data = yaml.load(f)

	except IOError:
		open(EMAILS_PATH, 'w')

	if not data:
		data = []
	__emailsData = data
	return data


def __save_emails(data):
	global __emailsData
	__emailsData = data
	with open(EMAILS_PATH, "w") as f:
		yaml.dump(data, f)


def exists(email, smtp=None):
	return not not get_email(email, smtp)


def __check_email(email_address, smtp=None, email_needed=True, smtp_needed=True):
	if(email_needed or email_address):
		_assert_true(email_address, "Email address is required")
		_assert_true(check_email_address(email_address), "Wrong format for email address: {}".format(email_address))

	if(smtp_needed or smtp):
		_assert_true(smtp, "SMTP is required")
		_assert_true(check_smtp(smtp), "Wrong format for SMTP: {}".format(smtp))


def __get_email_dict(email_address, smtp, password):
	email = {"email": email_address, "smtp": smtp}
	if password:
		email["password"] = password
	return email


def get_email(email=None, smtp=None):
	__check_email(email, smtp, email_needed=False, smtp_needed=False)
	emails = __get_emails()

	if(emails):
		if email is None:
			return 0, emails[0]

		for idx, EMAIL in enumerate(__get_emails()):
			if email == EMAIL["email"]:
				if(not smtp or (smtp and EMAIL["smtp"] == smtp)):
					return idx, EMAIL

	return None


def get(email=None, smtp=None):
	_, ret = get_email(email, smtp)
	return ret


def get_all():
	return [(elt["email"], elt.get("smtp", "")) for elt in __get_emails()]


def add(email_address, smtp, password=None):
	__check_email(email_address, smtp)

	_assert_true(not exists(email_address), "{} already exists".format(email_address))

	data = __get_emails()

	email_dict = __get_email_dict(email_address, smtp, password)
	data.append(email_dict)
	__save_emails(data)
	return email_dict


def update(email_address, smtp=None, password=None):
	__check_email(email_address, smtp, smtp_needed=False)

	emails = __get_emails()
	email_dict = get_email(email_address)
	if email_dict:
		idx, email_dict = email_dict

		assert emails[idx]['email'] == email_address

		if not smtp:
			smtp = email_dict['smtp']
		if not password:
			password = email_dict['password']
		email_dict = __get_email_dict(email_address, smtp, password)
		emails[idx] = email_dict
		__save_emails(emails)

	return email_dict


def delete(email_address):
	__check_email(email_address, smtp_needed=False)

	emails = __get_emails()

	email_dict = get_email(email_address)
	if email_dict:
		idx, email_dict = email_dict

		assert emails[idx]['email'] == email_address

		del emails[idx]

		__save_emails(emails)
	else:
		raise ValueError("address {} does not exists".format(email_address))
	return email_dict


def check_email_address(email_address):
	return EMAIL_RE.match(email_address)


def check_smtp(smtp):
	return SMTP_RE.match(smtp)
