#!/usr/bin/env python3

import coap
import os
import sys

c = coap.coap()

# argv[1] -> IP
# argv[2] -> PORT
# argv[3] -> Resource
# argv[4] -> Payload

resposta = c.PUT(sys.argv[1], sys.argv[2]) #aplicacao que se vira com o numero
print(resposta)
resposta = c.GET(sys.argv[1], b'\x13') #aplicacao que se vira com o numero
print(resposta)