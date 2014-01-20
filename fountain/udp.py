# Copyright (c) Alex Chamberlain 2012
import socket
import argparse
import threading
from threading import Thread

from pprint import pprint as pp
from ltcode import *
from struct import *

BUF_SIZE=512*2*2

lock = threading.Lock()

packet_b = ''

degree = 0

seed = 0

data = bytearray(504)

flag = 0
droplets = 0

bucket = lt_decode(10485760, 504)


def receiver(s, ip):
  global flag
  global bucket
  global droplets
  print("receiver"+ip)
#  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  s.bind((ip, 8000))
  while bucket.unknown_blocks > 0:
    lock.acquire()
    packet_b, a = s.recvfrom(BUF_SIZE)
    degree, seed, data = unpack('!II504s', packet_b)
    #flag = 1
   # print ("flag %d" %(flag))
  
    droplets += 1

    bucket.catch({'degree': degree, 'seed': seed, 'data': data})
    print("Caught {:d} droplets. There are {:d} unknown blocks.".format(droplets, bucket.unknown_blocks),
         end='\r')
    lock.release()

def fountain_client(ns):
  global flag
  global bucket
  global droplets
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  #s.bind(('127.0.0.2', 8000))
  s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  #s1.bind(('127.0.0.1', 8000))

  #s1.listen(10)

 # (clnt,ap) = s1.accept()

  # t1 = Thread(target=receiver, args=(s,"127.0.0.1"))
  # t1.start()

  # t2 = Thread(target=receiver, args=(s1,"127.0.0.1"))
  # t2.start()

 # s.sendto(b'', (ns.host, ns.port))
  s.sendto(b'aasdfsd', ('218.193.131.8', 8000))
  b, a = s.recvfrom(BUF_SIZE)
  print("Client received {} bytes from {}:{}".format(len(b), a[0], a[1]))


  i = 0
  while bucket.unknown_blocks > 0:
    b, a = s.recvfrom(BUF_SIZE)
    #print("Client received {} bytes from {}:{}".format(len(b), a[0], a[1]))
    degree, seed, data = unpack('!II504s', b)
    bucket.catch({'degree': degree, 'seed': seed, 'data': data})

 #   b, a = s1.recvfrom(BUF_SIZE)
     #print("Client received {} bytes from {}:{}".format(len(b), a[0], a[1]))
#    degree, seed, data = unpack('!II504s', b)

   #  lock.acquire()
   #  b, a = s1.recvfrom(BUF_SIZE)
   # # b = s1.recv(BUF_SIZE)
   #  degree, seed, data = unpack('!II504s', b)
   #  droplets += 1
   #  bucket.catch({'degree': degree, 'seed': seed, 'data': data})
    print("Caught {:d} droplets. There are {:d} unknown blocks.".format(i, bucket.unknown_blocks),
          end='\r')
   #  lock.release()

    # lock.acquire()
    # degree, seed, data = unpack('!II504s', packet_b)
    # lock.release()
    i += 1

  # t1.join()
  # t2.join()




  print("Decoded message of {:d} blocks using {:d} droplets ({:f}%).".format(bucket.N, droplets, (droplets*100)/bucket.N))
  #s.sendto(b' ', ('127.0.0.1', 8000))
 # s.sendto(pack('!II504s2323'), ('127.0.0.1', 8000))

  with open(ns.filename, 'wb') as f:
    o = memoryview(bucket.original)[:ns.length]
    f.write(o)

def over_transmiter(s):
  #self.s = s
  print("asdfsd")
  b, a = s.recvfrom(BUF_SIZE)
#  sys.exit(0)

def fountain_server(ns):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

 # s.bind((ns.host, int(ns.port)))
 # s.bind(('127.0.0.3', 8000))



  with open(ns.filename, 'rb') as f:
    buf = f.read()

  fountain = lt_encode(buf, 504)
  

  while True:
   # b, a = s.recvfrom(BUF_SIZE)
    #print("Server received {} bytes from {}:{}".format(len(b), a[0], a[1]))
    print("Starting fountain...")
  #  s.setblocking(0)l
    # t1 = Thread(target=over_transmiter, args=(s,))
    # t1.start()
    while 1:
      d = next(fountain)
    #  s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("127.0.0.1",8000))
      # d = next(fountain)
     # s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("127.0.0.1",8000))

   #   s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("192.168.8.177",8000))
      s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("192.168.5.2",8000))
      d = next(fountain)

      s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("192.168.4.2",8000))

      d = next(fountain)   
      s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("192.168.2.2",8000))

      d = next(fountain)   
      s.sendto(pack('!II504s', d['degree'], d['seed'], d['data']), ("192.168.3.2",8000))
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', action='store_true', default=False, dest='server')
  parser.add_argument('-H', default='', dest='host')
  parser.add_argument('-P', default=50005, dest='port')
  parser.add_argument('-l', '--length', dest='length', type=int)
  parser.add_argument('filename', nargs='?')
  ns = parser.parse_args()
  sys.setrecursionlimit(1000000)

  if(ns.server):
    fountain_server(ns)
  else:
    fountain_client(ns)
