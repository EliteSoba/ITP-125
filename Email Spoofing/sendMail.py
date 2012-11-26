#Imports
from email.mime.text import MIMEText
import fileinput
import smtplib
import getpass
import string
import sys

########################################################################################################
#                                            Tobias Lee                                                #
#                                            8011734618                                                #
#                                             ITP 125                                                  #
#                                           Email Spoofing                                             #
#Credit to Google for helping me with this.                                                            #
#More specifically, docs.python.org/, http://www.tutorialspoint.com/python/python_sending_email.htm,   #
#and Quentin Hsu for telling me I could use smtp.gmail.com for testing and about getpass()             #
#Next up is making a GUI version of this                                                               #
########################################################################################################

#Usage: sendMail.py [-v] -s="SMTP Server" [-SSL] -u="Username" [-p="Password"] -t="Comma, Divided, Recepients" -f="From <Email>" [-sub="Subject"] -m="File"
# [s]erver, [u]sername, [p]assword, [t]o, [f]rom, [sub]ject, [m]essage
#SAMPLE: sendMail.py -v -s="smtp.gmail.com" -SSL -u="tobiasle@usc.edu" -t="joseph.greenfield@usc.edu" -f="God <God@heaven.com>" -m="commandments.txt"
#You can also just run sendMail.py and it'll prompt you for the inputs along the way.

PROPERFORMAT = "sendMail.py [-v] -s=\"SMTP Server\" [-SSL] -u=\"Username\" [-p=\"Password\"] -t=\"Comma, Divided, Recepients\" -f=\"From <Email>\" [-sub=\"Subject\"] -m=\"File\" for command line mode"

commands = ['s', 'h', 'v', 'ssl','u','p','t','f','sub','m']

SMTPServer = " "
SSL = False
verbose = False
SMTPUsername = " "
SMTPPassword = " "
Recepients = " "
Sender = " "
Subject = " "
Message = ""
f = " "

#Minor redundancy in error checking
if len(sys.argv) != 1:
  for i in range(len(sys.argv)):
		if i == 0:
			continue
		command = sys.argv[i]
		if command[0] != '-':
			print("Error: Command not in form: " + PROPERFORMAT)
			print("Please type sendMail.py -h for help")
			quit()
		else:
			if command.find('=') == -1:
				realCommand = command[command.find('-')+1:]
			else:
				realCommand = command[command.find('-')+1:command.find('=')]
			realCommand = realCommand.lower()
			if not commands.__contains__(realCommand):
				print("Error: invalid arguments.")
				print("Please type sendMail.py -h for help")
				quit()
			elif realCommand == 's':
				SMTPServer = command[command.find('=')+1:]
			elif realCommand == 'u':
				SMTPUsername = command[command.find('=')+1:]
			elif realCommand == 'p':
				SMTPPassword = command[command.find('=')+1:]
			elif realCommand == 't':
				Recepients = command[command.find('=')+1:]
			elif realCommand == 'f':
				Sender = command[command.find('=')+1:]
			elif realCommand == 'sub':
				Subject = command[command.find('=')+1:]
			elif realCommand == 'm':
				f = fileinput.input(files = command[command.find('=')+1:])
			elif realCommand == 'ssl':
				SSL = True
			elif realCommand == 'v':
				verbose = True
			elif realCommand == 'h':
				print("Sends and email\n")
				print(PROPERFORMAT)
				print("[-v]"+"\t\t\t\tRuns in verbose mode")
				print("-s=\"SMTP Server\""+"\t\tThe name of the SMTP Server")
				print("[-SSL]"+"\t\t\t\tAutomatically starts up with SSL Connection")
				print("-u=\"Username\""+"\t\t\tThe Username for the SMTP Server")
				print("[-p=\"Password\"]"+"\t\t\tThe Password for the SMTP Server")
				print("\t\t\t\t(If omitted, requests nonechoed password)")
				print("-t=\"Comma, Divided, Recepients"+"\tThe desired recepients")
				print("-f=\"From <Email>\""+"\t\tThe desired Sender and Sender Email")
				print("[-sub=\"Subject\"]"+"\t\tThe desired Email Subject")
				print("\t\t(If omitted, first line of file will be used as Subject)")
				print("-m=\"File\""+"\t\t\tSpecifies file content to Email")
				print("-h"+"\t\t\t\tOpens this dialogue")
				quit()
			#Redundant, but nice to have
			else:
				print('-' + realCommand + ' is not a proper flag! Please format command as ' + PROPERFORMAT)
				print("Please type sendMail.py -h for help")
				quit()

	#After commands have been processed
	if SMTPServer == " " or SMTPUsername == " " or Recepients == " " or Sender == " " or f == " ":
		print("Error: Not enough arguments for a proper execution")
		print("Please type sendMail.py -h for help")
		quit()
	try:
		if (Subject == " "):
			Subject = f.readline()
		else:
			Message = f.readline()
	except IOError:
		print("Error: Invalid file path for message")
		quit()
	if SMTPPassword == " ":
		SMTPPassword = getpass.getpass("Password:")
	
	#Connect to Server
	if verbose:
		print("Connecting to server...")
	if (SSL):
		server = smtplib.SMTP_SSL(SMTPServer)
	else:
		server = smtplib.SMTP(SMTPServer)
	
	#Authenticate
	if verbose:
		print("Logging in...")
	try:
		server.login(SMTPUsername, SMTPPassword)
	except smtplib.SMTPAuthenticationError:
		print ("Error: Incorrect username or password")
		quit()
	except smtplib.SMTPException:
		print ("Unknown error has occured")
		quit()
	
	#Message creation
	if verbose:
		print("Creating message...")
	for line in f:
		Message += line
	
	msg = MIMEText(Message)
	msg['Subject'] = Subject
	msg['To'] = Recepients
	
	#Don't ask about this part. It only seems to adjust both the name and the email if I do it like this.
	msg['From'] = Sender
	From = Sender[Sender.find('<'):]
	msg['From'] = From
	
	#Send the actual email
	if verbose:
		print("Sending Email...")
	try:
		server.send_message(msg)
	except smtplib.SMTPRecipientsRefused:
		print ("Error: Unknown Recepient")
		quit()
	except smtplib.SMTPDataError:
		print ("Unknown error has occured")
		quit()
	
	print("Email sent successfully!")
	
	quit()
#(else:) Unnecessary because of quit()
#Login to SMTP Server
SMTPServer = input("Please enter SMTP Server: ")
loginAttempts = 3 #Maximum number of login failures
#Attempts that many logins
for i in range(loginAttempts+1):
	loginFailure = False;
	
	#Username for login
	SMTPUser = input("Please enter username: ")
	
	#Allows someone to change SMTP servers if they mess up the first time
	if (SMTPUser.lower() == "Change SMTP Server".lower()):
		SMTPServer = input("Please reenter SMTP Server: ")
		i -= 1
		continue
	
	#Password for login. getpass means the password won't display in console
	SMTPPassword = getpass.getpass("Please enter password: ")
	
	#Allow for choosing automatic SSL connection
	SSL = 'Maybe'
	while SSL[0] != 'y' and SSL[0] != 'n':
		SSL = input("SSL? (y/n)\n")
		SSL = SSL.lower()
	if SSL[0] == 'y':
		server = smtplib.SMTP_SSL(SMTPServer)
	else:
		server = smtplib.SMTP(SMTPServer)
	
	#The actual login. If fails, displays message.
	#Console messages make this section pretty self-explanitory
	try:
		server.login(SMTPUser, SMTPPassword)
	except smtplib.SMTPAuthenticationError:
		print ("Error: Incorrect username or password")
		loginFailure = True
	except smtplib.SMTPException:
		loginFailure = True
		print ("Unknown error has occured")
	if (loginFailure):
		if (i == loginAttempts):
			print ("Too many failed attempts. Closing.")
			quit()
		else:
			print (str(loginAttempts-i) + " Attempts remaining. Enter \"Change SMTP Server\" to change SMTP Server.")
	
	else:
		print ("Connected successfully!\n")
		break

#Messaging time
command = "c"
failed = True
while command[0] != 'n' and failed :
	if command[0] == 'c': #Entering in the necessary parameters
		#Recepients
		Recepients = input("Please enter recepients, separated by commas: ")
		#Name of Sender
		Sender = input("Please enter sender: ")
		#Email of sender
		SenderEmail = input("Please enter sender's email: ")
		
		#File input. Allows retrying if they mislink the file.
		tryAgain = 'yes'
		while tryAgain[0] == 'y':
			tryAgain = 'm'
			content = input("Please enter path to message: ")
			f = fileinput.input(files = (content))
			try:
				message = f.readline()
			except IOError:
				print ("Error: Invalid file name")
				while tryAgain[0] != 'n' and tryAgain[0] != 'y':
					tryAgain = input("Enter a new file? (y/n)")
					tryAgain = tryAgain.lower()
		if (tryAgain[0] == 'n'):
			print("Quitting.")
			quit()
		
		#Allows creating of Subject field if desired
		newSubject = 'maybe'
		while (newSubject[0] != 'y' and newSubject[0] != 'n'):
			newSubject = input("Enter new Subject? If no, defaults to first line of message (y/n)\n")
			newSubject = newSubject.lower()
		if (newSubject[0] == 'y'):
			Subject = input("Please enter the Subject of the email: ")
		else:
			Subject = message
			message = ""
		
		#Creates the message to be sent
		for line in f:
			message += line
		msg = MIMEText(message)
		msg['Subject'] = Subject
		msg['To'] = Recepients
		
		#Don't ask about this part. It only seems to adjust both the name and the email if I do it like this.
		msg['From'] = Sender + ' <' + SenderEmail + '>'
		From = "<" + SenderEmail + ">"
		msg['From'] = From
	
	#Tries sending the actual message. Can sometimes fail.
	#If it fails, allows user to choose to retry, reenter information and retry, or just give up
	try:
		failed = False
		server.send_message(msg)
	except smtplib.SMTPRecipientsRefused:
		print ("Error: Unknown Recepient")
		failed = True
	except smtplib.SMTPDataError:
		print ("Unknown error has occured")
		failed = True
	if failed:
		command = "false"
		while (command[0] != 'y' and command[0] != 'n' and command[0] != 'c'):
			print ("\nWould you like to try again?")
			print ("(y) - Try again with same settings")
			print ("(c) - Change settings")
			print ("(n) - Do not try again")
			command = input()
			command = command.lower()

#Only gets out if the email sending didn't fail or if the user gave up
#If they didn't give up, it means the sending didn't fail and the email was sent successfully.
if command[0] != 'n':
	print ("Email sent successfully!")