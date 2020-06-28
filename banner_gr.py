#!/usr/bin/env python3

import re
import sys
import requests
import ipaddress
import threading, time
from queue import Queue

print_lock = threading.Lock()

# User Agent (OS: FreeBSD Browser: Chrome 40 Arch: 64bit)
UA = "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"

if len(sys.argv) !=3:
	print ("{} <rango ip> <puerto>".format(sys.argv[0]))
	sys.exit(1)

def get_banner(host, port):
	try:
		r = requests.get("http://" + str(host) + ":" + port, headers={'User-Agent':UA}, timeout=5.0)
		# Obteniendo el valor de la etiqueta "title"
		title = re.findall(r'<title>(.*?)</title>', r.text)[0]
		# Obteniendo nombre del servidor
		server = r.headers['server']

		print ("HOST: " + str(host) +" Title: " + title + " Server: " + server)

	except Exception as ex:
		pass

def threader():
	while True:
		worker = q.get()
		get_banner(worker, sys.argv[2])
		q.task_done()

q = Queue()

for x in range(100):
	t = threading.Thread(target=threader)
	t.daemon = True
	t.start()
		
print ("\n[+] Escaneando...\n")

# Recorriendo rango de IPs
ipv4 = ipaddress.ip_network(sys.argv[1])
for ips in ipv4.hosts():
	q.put(ips)

q.join()

