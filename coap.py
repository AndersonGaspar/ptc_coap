#from itertools import chain
import codecs
import collections
import copy
import random
import struct
import sys
import socket
from enum import Enum

class TIPOS(Enum):
    CONFIRMAVEL = b'\x00'
    NCONFIRMAVEL = b'\x10'
    ACK = b'\x20'
    RESET = b'\x30'

class CODIGO_REQUISICAO(Enum):
	EMPTY_MSG = b'\x00'
	GET = b'\x01'
	POST = b'\x02'
	PUT = b'\x03'
	DELETE = b'\x04'

class CODIGO_CONFIRMACAO(Enum):
	CREATED =  b'\x41'
	DELETED =  b'\x42'
	VALID =  b'\x43'
	CHANGED =  b'\x44'
	CONTENT = b'\x45'

class CODIGO_ERRO_CLIENTE(Enum):
	BAD_REQUEST =  b'\x80'
	UNAUTHORIZED = b'\x81'
	BAD_OPTION = b'\x82'
	FORBIDDEN =  b'\x83'
	NFOUND =  b'\x84'
	METHOD_NALLOW =  b'\x85'
	NACCEPTABLE =  b'\x86'
	PRECONDITION_FAILED =  b'\x8C'
	REQUEST_ENTITY_TLARGE =  b'\x8D'
	UNSUPPORTED_FORMAT =  b'\x8F'
	
class CODIGO_ERRO_SERVIDOR(Enum):
	INTERNAL_SERVER_ERR =  b'\xA0'
	NIMPLEMENT =  b'\xA1'
	BAD_GW =  b'\xA2'
	SERVICE_UNAVAILABLE =  b'\xA3'
	GW_TIMEOUT =  b'\xA4'
	PROXYING_NSUPPORTED =  b'\xA5'

class OPTIONS_DELTA(Enum):
	IF_MATC =  b'\x01'
	URI_HOST =  b'\x03'
	ETAG =  b'\x04'
	IF_NONE_MATCH =  b'\x05'
	URI_PORT =  b'\x07'
	LOCATION_PATH =  b'\x08'
	URI_PATH =  b'\x0B'
	CONTENT_FORMAT =  b'\x0C'
	MAX_AGE =  b'\x0E'
	URI_QUERY =  b'\x0F'
	ACCEPT =  b'\x11'
	LOCATION_QUERY =  b'\x14'
	PROXY_URI =  b'\x23'
	PROXY_SCHEME =  b'\x27'
	SIZE1 = B'\x3C'

class coap:

	def __init__(self):
		self.versao = b'\x40' # versao e sempre 40.
		self.tipo = b'\x00' #
		self.tkl = b'\x00' # tkl é sempre zero.
		self.codigo = b'\x00'
		self.msg_id = b'\x23\x59'
		self.opcao_delta = 0
		self.delta_anterior = 0
		self.opcao_len = b'\x00'
		self.opcoes = b'\x00' # campo de valor variavel.
		self.payload_mac = b'\xff' # playload_mac e sempre ff.
		self.payload = b''
		self.quadro = b''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.codes = {
			65:"2.01 - Created", 
			66:"2.02 - Deleted", 
			67:"2.03 - Valid", 
			68:"2.04 - Changed", 
			69:"2.05 - Content", 
			128:"4.00 - Bad Request", 
			129:"4.01 - Unauthorized", 
			130:"4.02 - Bad Option", 
			131:"4.03 - Forbidden", 
			132:"4.04 - Not Found", 
			133:"4.05 - Method Not Allowed", 
			134:"4.06 - Not Acceptable", 
			140:"4.12 - Precondition Failed", 
			141:"4.13 - Request Entity Too Large", 
			142:"4.14 - Unsupported Content-Format",
			160:"5.00 - Internal Server Error",
			161:"5.01 - Not Implemented",
			162:"5.02 - Bad Gateway",
			163:"5.03 - Service Unavailable",
			165:"5.04 - Gateway Timeout",
			166:"5.05 - Proxying Not Supported"
		}

	def FRAME(self, uri, msg=None):
		quadro = b''
		quadro = (self.versao[0] | self.tipo.value[0] | self.tkl[0]).to_bytes(1, byteorder='big') 
		quadro += self.codigo.value 
		quadro += self.msg_id

		uri =  uri.split('://')
		protocolo = uri[0]

		if(protocolo != 'coap'):
			return -1
		
		parametros = uri[1].split('/')

		addr = parametros[0].split(':')
		if(len(addr) > 1):
			port = int(addr[1])
			#is_valid = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", addr)
		else:
			port = 5683
		
		addr = addr[0]
		a = addr.split('.')
		for b in a :
			if(not b.isnumeric()):
				self.opcao_delta = OPTIONS_DELTA.URI_HOST.value[0] - self.delta_anterior
				self.delta_anterior = OPTIONS_DELTA.URI_HOST.value[0]
				quadro += (self.opcao_delta << 4 | len(addr)).to_bytes(1, byteorder='big')
				quadro += str.encode(addr)
				break

		
		resource_list = parametros[1:]
		for uri_path in  resource_list:
			self.opcao_delta = OPTIONS_DELTA.URI_PATH.value[0] - self.delta_anterior
			self.delta_anterior = OPTIONS_DELTA.URI_PATH.value[0]
			quadro += (self.opcao_delta << 4 | len(uri_path)).to_bytes(1, byteorder='big')
			quadro += str.encode(uri_path)

		if(msg != None):
			self.quadro += self.payload_mac
			self.quadro += msg.encode()

		self.delta_anterior = 0
		return (quadro, addr, port)



	def GET(self, uri):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.GET
		self.quadro, server_adress, port = self.FRAME(uri)
		self.sock.sendto(self.quadro, (server_adress, port))

		data, addr = self.sock.recvfrom(1024)
		print(data)
		resposta = self.receive(data)
		print(self.codes[resposta[1]], resposta[2])

		return(resposta)

	def POST(self, uri, msg):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.POST
		
		self.quadro, server_adress, port = self.FRAME(uri)
		self.sock.sendto(self.quadro, (server_adress, port))
		data, addr = self.sock.recvfrom(1024)
		
		print(data)
		#resposta = self.receive(data)
		#print(self.codes[resposta[1]], resposta[2])	

	def PUT(self, uri, msg):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.PUT
		
		self.quadro, server_adress, port = self.FRAME(uri)
		self.sock.sendto(self.quadro, (server_adress, port))
		data, addr = self.sock.recvfrom(1024)
		
		print(data)
		#resposta = self.receive(data)
		#print(self.codes[resposta[1]], resposta[2])
	

	def DELETE(self):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.DELETE
		
		self.quadro = self.FRAME(resource)
		self.sock.sendto(self.quadro, (server_adress, port))

		data, addr = self.sock.recvfrom(1024)
		print(data)
		#resposta = self.receive(data)

		#print(self.codes[resposta[1]], resposta[2])

	def receive(self, frame):
		octeto = frame[0]
		frame  = frame[1:]
		versao = octeto & 192
		tipo = octeto & 48
		TKL = octeto & 15

		if(tipo != 32):
			return (-1, None, None)

		codigo = frame[0]
		frame = frame[1:]

		if(codigo >= 128 and codigo <= 159):
			return (1, codigo, None)
		
		if(codigo >= 160 and codigo < 192):
			return (1,codigo, None)
		
		if(codigo >= 64 and codigo <96):
			MID = frame[0:2]
			frame = frame[2:]
			if(MID != self.msg_id):
				return (-2, None, None)

			frame = frame[TKL:]

			aux = True
			while aux:
				op = frame[0]
				frame = frame[1:]
				op_delta = op & 240
				op_length = op & 15
				op_delta = op_delta >> 4

				if (op_delta == 13):
					op_delta = frame[0]
					frame = frame[1:]
				if (op_delta == 14):
					op_delta = frame[0:2]
					frame = frame[2:]
				if (op_delta == 15):
					if (op_length != 15):
						return (-3, None, None)
					else:
						aux = False
					payload = frame

				if (op_delta < 13):		
					if (op_length == 13):
						op_length = frame[0]
						frame = frame[1:]
					if (op_length == 14):
						op_length = frame[0:2]
						frame = frame[2:]
					if (op_length == 15):
						return (-3, None, None)
					option = frame[0:op_length]

			return (1, codigo, payload)