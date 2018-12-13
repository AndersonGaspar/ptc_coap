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
		self.tkl = b'\x04' # tkl é sempre zero.
		self.codigo = b'\x00'
		self.msg_id = b'\x23\x59'
		self.opcao_delta = b'\x00'
		self.opcao_len = b'\x00'
		self.opcoes = b'\x00' # campo de valor variavel.
		#self.payload_mac = b'\xff' # playload_mac e sempre ff.
		self.payload = b''
		self.quadro = b''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#self.sock.bind((socket.gethostname(), 5555))

	def GET(self, uri_path, server_adress, port):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.GET
		self.opcao_delta = OPTIONS_DELTA.URI_PATH
		self.opcao_len = len(uri_path)
		self.opcoes = uri_path
		self.payload = b''

		#println(self.versao)
		
		self.quadro = b''
		self.quadro = (self.versao[0] | self.tipo.value[0] | self.tkl[0]).to_bytes(1, byteorder='big') 
		self.quadro += self.codigo.value 
		self.quadro += self.msg_id 
		self.quadro += (self.opcao_delta.value[0] << 4 | self.opcao_len).to_bytes(1, byteorder='big') 
		self.quadro += self.opcoes 
		#self.quadro += self.payload_mac 
		self.quadro += self.payload

		self.sock.sendto(self.quadro, (server_adress, port))

		print(self.quadro)


		data, addr = self.sock.recvfrom(1024)

		print(data)
		print(addr)

	def POST(self, uri_path, server_adress, port):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.POST
		self.opcao_delta = OPTIONS_DELTA.URI_PATH
		self.opcao_len = len(uri_path)
		self.opcoes = uri_path
		self.payload = b''

		#println(self.versao)
		
		self.quadro = b''
		self.quadro = (self.versao[0] | self.tipo.value[0] | self.tkl[0]).to_bytes(1, byteorder='big') 
		self.quadro += self.codigo.value 
		self.quadro += self.msg_id 
		self.quadro += (self.opcao_delta.value[0] << 4 | self.opcao_len).to_bytes(1, byteorder='big') 
		self.quadro += self.opcoes 
		#self.quadro += self.payload_mac 
		self.quadro += self.payload

		self.sock.sendto(self.quadro, (server_adress, port))

		print(self.quadro)


		data, addr = self.sock.recvfrom(1024)

		print(data)
		print(addr)		

	def PUT(self, uri_path, server_adress, port):
		self.tipo = TIPOS.CONFIRMAVEL
		self.codigo = CODIGO_REQUISICAO.PUT
		self.opcao_delta = OPTIONS_DELTA.URI_PATH
		self.opcao_len = len(uri_path)
		self.opcoes = uri_path
		self.payload = b'TESTEE'

		#println(self.versao)
		
		self.quadro = b''
		self.quadro = (self.versao[0] | self.tipo.value[0] | self.tkl[0]).to_bytes(1, byteorder='big') 
		self.quadro += self.codigo.value 
		self.quadro += self.msg_id 
		self.quadro += (self.opcao_delta.value[0] << 4 | self.opcao_len).to_bytes(1, byteorder='big') 
		self.quadro += self.opcoes 
		#self.quadro += self.payload_mac 
		self.quadro += self.payload

		self.sock.sendto(self.quadro, (server_adress, port))

		print(self.quadro)


		data, addr = self.sock.recvfrom(1024)

		print(data)
		print(addr)	

	def DELETE(self):
		pass
