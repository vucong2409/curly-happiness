import os
from ssl import *
from socket import *
from dotenv import load_dotenv
import base64

#Load variable from .env file into virtual environment 
load_dotenv()

MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
TIMEOUT = os.getenv("TIMEOUT")
YOUR_MAIL_ADDRESS = os.getenv("YOUR_MAIL_ADDRESS")

log_file = open("log.txt", "w")

crlf = "\r\n"
endmsg = "\r\n.\r\n"

print("Enter your name: ",end="")
sender_name = input()

print("Subject: ", end="") 
mail_subject = input()

print("To: ", end="")
receiver = input()

#Port for SSL is 465 not 287
mailserver = (MAIL_SERVER, 465)

#Test connection with the server
clientSocket = socket(AF_INET, SOCK_STREAM)

#Wrap ssl before connect to mail server 
clientSocket = wrap_socket(clientSocket)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
log_file.write(recv.decode("utf-8"))

#Send HELO command to initate an email transaction
#More Detail:https://bit.ly/3dLnJRv 

heloMsg = "HELO " + sender_name + crlf 
clientSocket.send(heloMsg.encode('utf-8'))
recv = clientSocket.recv(1024)
log_file.write(recv.decode('utf-8'))

#List of all smtp command
#https://mailtrap.io/blog/smtp-commands-and-responses/
print("Connect to server " + MAIL_SERVER + " with username " + MAIL_USER)

clientSocket.send("AUTH LOGIN\r\n".encode('utf-8'))
recv = clientSocket.recv(2048)
log_file.write(recv.decode('utf-8'))


userb64 = base64.b64encode(MAIL_USER.encode('utf-8'))
passb64 = base64.b64encode(MAIL_PASS.encode('utf-8'))

clientSocket.send(userb64)
clientSocket.send("\r\n".encode('utf-8'))
recv = clientSocket.recv(1024)
log_file.write(recv.decode('utf-8'))

clientSocket.send(passb64)
clientSocket.send("\r\n".encode('utf-8'))
recv = clientSocket.recv(1024)
log_file.write(recv.decode('utf-8'))

print("Auth successfully!")

sender_msg = "MAIL FROM: <" + YOUR_MAIL_ADDRESS + ">\r\n"
clientSocket.send(sender_msg.encode('utf-8'))
recv = clientSocket.recv(1024)
log_file.write(recv.decode('utf-8'))


recv_msg = "RCPT TO:<"+ receiver + ">\r\n"
clientSocket.send(recv_msg.encode('utf-8'))
recv3 = clientSocket.recv(1024)
log_file.write(recv3.decode('utf-8'))

clientSocket.send("DATA\r\n".encode('utf-8'))
recv3 = clientSocket.recv(1024)
log_file.write(recv3.decode('utf-8'))

#Build mail content 
#More information: http://www.codestore.net/store.nsf/unid/EPSD-587VVX
sender_addr = "From: " + YOUR_MAIL_ADDRESS + crlf
mail_subject = "Subject: " + mail_subject + crlf 
enable_html = 'Content-Type: text/html; charset="ISO-8859-1"' + crlf
recv_addr = "To: " + receiver + crlf 
mail_header = sender_addr + mail_subject + enable_html + recv_addr 

mail_content = ""
with open("mail-content.html") as f:
    line_list = f.readlines()
    for x in line_list:
        size = len(x)
        mail_content = mail_content + x[:size - 1] + crlf 

mail = mail_header + crlf + mail_content

clientSocket.send(mail.encode('utf-8'))

clientSocket.send('\r\n.\r\n'.encode('utf-8'))
recv3 = clientSocket.recv(1024)
log_file.write(recv3.decode('utf-8'))


clientSocket.send('QUIT\r\n'.encode('utf-8'))
recv3 = clientSocket.recv(1024)
log_file.write(recv3.decode('utf-8'))

print("Send mail successfully!")

log_file.close()