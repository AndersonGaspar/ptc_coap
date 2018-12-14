import coap
import os
import sys

c = coap.coap()
c.GET(sys.argv[1], sys.argv[2], int(sys.argv[3]))
