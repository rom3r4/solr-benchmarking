#!/usr/bin/python

# 
# 


import subprocess
import os


def global_consts():

    # set these to a low number and MAX_TESTS
    # to a hight number, to minimize caches and
    # get a more real approach 
    global MAX_CONNS
    global MAX_CONCURRENT
    
    global HOSTNAME
    global MAX_TESTS

    MAX_CONNS = 1
    MAX_CONCURRENT = 1    
    HOSTNAME = "http://voa3r.appgee.net"
    MAX_TESTS = 1000
    
    
    
def generate_dictionary():


  # how many sufixeds should i create per each root.
  # e.g: root_elephant1, root_elephant2 <-- 2
  LIMIT_PER_ROOT = 1000


  # add sample words here
  ROOT_LIST = [
        'test',
        'word',
        'car',
        'dog',
        'cat',
        'sun',
        'beer',
        'spider',
        'snake',
        'table',
        'window',
        'man',
        'pet',
        'dinosaur',
        'bee',
        'fork',
        'bike',
        'motorbike',
        'space',
        'web',
        'internet',
        'lion',
        'deer',
        'bear',
        'frog',
        'wolf',
        'pig',
        'chicken',
        'turkey',
        'bull',
        'plain',
        'mouse',
        'beer',
        'house']

  DICT = []
  for root in ROOT_LIST:
    for i in range(1, LIMIT_PER_ROOT):
      DICT.append(root + str(i))
  return DICT



def init_settings():
  # non permanent changes
  # this fixed the "too many open connections error"
  # of the Apache Bench command
  os.system("echo '10240' > /proc/sys/net/core/somaxconn")
  os.system("ulimit -n 65535")
  
def clean_caches():
  None
def tests(dict):
  None





if __name__ == "__main__":

    print '1. initializing global settings ...'
    global_consts()
    init_settings()
    
    print '2. generating dictionary ...'
    dict = generate_dictionary()
    
    print '3. cleaning caches ...'
    clean_caches()
    
    print '4. starting tests ...'
    tests(dict)
    
    print '5. ...done.'
