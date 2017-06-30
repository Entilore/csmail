import click
from py_csmail import emailsManagement as em
from py_csmail.sendEmail import MIMEMail as MIMEMail


def check_emails(ctx, obj, value):
	return [check_email(ctx, obj, m) for m in value]


def check_email(ctx, obj, value):
	if value and not em.check_email_address(value):
		raise click.BadParameter("wrong email format: {}".format(value))
	return value


def check_existing_email(ctx, obj, value):
	if value:
		if not em.exists(value):
			raise click.BadParameter("Unknown email: {}".format(value))
	return value


def check_smtp(ctx, obj, value):
	if value and not em.check_smtp(value):
		raise click.BadParameter("wrong smtp format")
	return value


def print_email_action(fnc, action_name):
	try:
		dct = {k: v if k != "password" else "****" for (k, v) in fnc().items()}
		if dct:
			click.echo("email successfully {}: {}".format(action_name, dct))
		else:
			click.echo("Something went wrong")
	except ValueError as e:
		raise click.UsageError(e)


@click.group()
def cli():
	pass


@cli.group()
def email():
	pass


@email.command()
@click.argument("email", callback=check_email)
@click.argument("smtp_ssl", callback=check_smtp)
@click.argument("password", required=False)
def add(email, smtp_ssl, password):
	print_email_action(
		lambda: em.add(email, smtp_ssl, password),
		"saved"
	)


@email.command()
def list():
	for t in em.get_all():
		click.echo(t)


@email.command()
@click.argument("email", callback=check_email)
@click.argument("smtp_ssl", required=False, callback=check_smtp)
@click.argument("password", required=False)
def update(email, smtp_ssl, password):
	print_email_action(
		lambda: em.update(email, smtp_ssl, password),
		"updated"
	)


@email.command()
@click.argument("email", callback=check_email)
def delete(email):
	print_email_action(
		lambda: em.delete(email),
		"deleted"
	)


@cli.command()
@click.option("--exp", "-e", required=False, help="the expeditor to use [default: the first setup data]", callback=check_existing_email)
@click.option("--subject", "-s", required=False, default="", help="the subject to use")
@click.option("--exp_name", "-f", required=False, help="the value to put in FROM field")
@click.argument("message", required=True, default="Ping")
@click.argument("dests", nargs=-1, required=True, callback=check_emails)
def send(exp, subject, exp_name, message, dests):
	exp_data = em.get(exp)

	email = MIMEMail(subject, message, exp_data, exp_name)
	email.sendMails(dests)
	click.echo("Done")
