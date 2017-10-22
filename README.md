# CLI Send Mail

Send mails from the CLI

*Warning : this app have to save your password*

# Installation

First install python3 and  pip3. Then install csmail:

```bash 
sudo pip3 install git+https://github.com/ThHareau/csmail
```

# Usage

First, configure your first email:
```bash 
sudo csmail email add <YOUR EMAIL> <YOUR SMTP SERVER HOSTNAME> <YOUR PASSWORD>
# the password will be saved unencrypted, in a file only accessible by the root user. That's why sudo is needed
```

Then send your first email: 

```bash
csmail send -s "your subject" "Your message" "<SOME RECIPIENT EMAIL>"
```
