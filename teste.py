import coap
import os
import sys

c = coap.coap()

# argv[1] -> IP
# argv[2] -> PORT
# argv[3] -> Resource
# argv[4] -> Payload

c.PUT(sys.argv[3], sys.argv[4], sys.argv[1], int(sys.argv[2]))
c.GET(sys.argv[3], sys.argv[1], int(sys.argv[2]))
