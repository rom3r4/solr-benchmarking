#!/usr/bin/python




from random import choice
import subprocess, os, sys, getopt


def global_consts():


    global MAX_CONNS
    global MAX_CONCURRENT
    
    global HOSTNAME
    global MAX_TESTS


    MAX_CONNS = '3'
    MAX_CONCURRENT = '1'
    # include 'http://' and a trailing '/' at the end    
    HOSTNAME = "http://voa3r7.appgee.net/"
    

    MAX_TESTS = 2
    
    
    
def generate_dictionary():


  LIMIT_PER_ROOT = 30


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
      

  print '--> generated '+ str(len(DICT)) +' words in dictionary'      
  return DICT



def init_settings():


  os.system("echo '10240' > /proc/sys/net/core/somaxconn")
  os.system("ulimit -n 65535")
  
def clean_caches():
  
  print '--> restarting Varnish daemon'
  subprocess.call(["service", "varnish", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  print '--> restarting Memcache damemon #1'
  subprocess.call(["service", "memcached", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  print '--> restarting Memcache damemon #2'
  subprocess.call(["service", "memcached", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  print '--> restarting php'
  subprocess.call(["service", "php", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  print '--> restarting Web server'
  subprocess.call(["service", "nginx", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);

  
def tests(dict, op):
  
  
  if (op == 'v'):
    # Vertical Scalability.
    MAX_CONNS = 100
    MAX_CONNS_ORIG = 100
    MAX_CONCURRENT = '1'
    mode='vertical'
  elif (op == 'h'):
    # Horizontal scalability.
    MAX_CONNS = '10000'
    MAX_CONCURRENT = '10000'
    mode='horizontal'     
  else:
    # Cache test.
    # 3 x 400 should be lower that the total
    # number of words in dictionary, to avoid
    # colisions.
    MAX_CONNS = '3'
    MAX_CONCURRENT = '1'
    mode='cache'
  
  print '--> tests using 1 word in search (1/3)'
  for i in range(1, MAX_TESTS):
    if (mode == 'vertical'):
      MAX_CONNS = MAX_CONNS_ORIG * i
    type = '1word'
    rnd = choice(dict)
    title = '(1word)selected random word: '+rnd
    if (mode == 'vertical'):
      filename = mode+'_result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    else:
      filename = mode+'_result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    
    print '---'
    print '--> '+title
    if (mode == 'vertical'):
      print '--> command-line: ab -k -n '+str(MAX_CONNS)+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent.txt'
    else:
      print '--> command-line: ab -k -n '+MAX_CONNS+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent.txt'
          
    try:
      # f=open('result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt','wb')
      if (mode == 'vertical'):
        subprocess.call(["ab", "-g"+filename, "-n "+str(MAX_CONNS), "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      else:
        subprocess.call(["ab", "-g"+filename, "-n "+MAX_CONNS, "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
      # subprocess.call(["gnuplot", "-e FILENAME='"+filename+ "',TITLE='"+title+"'", "creategraphs.gp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
      # f.close()  
      None

  print '--> cleaning caches ...'
  clean_caches()
  if (mode == 'vertical'):
    MAX_CONNS = MAX_CONNS_ORIG

    
  print '--> tests using 2 word in search (2/3)'
  for i in range(1, MAX_TESTS):
    if (mode == 'vertical'):
      MAX_CONNS = MAX_CONNS_ORIG * i
    type = '2word'
    rnd1 = choice(dict)
    rnd2 = choice(dict)
    title = '(2words)selected random word: '+rnd1+', '+rnd2
    if (mode == 'vertical'):
      filename = mode+'_result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    else:
      filename = mode+'_result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    
    print '---'
    print '--> '+title
    if (mode == 'vertical'):
      print '--> command-line: ab -k -n '+str(MAX_CONNS)+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent.txt'
    else:
      print '--> command-line: ab -k -n '+MAX_CONNS+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent.txt'
    try:
      # f=open('result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt','wb')
      if (mode == 'vertical'):
        subprocess.call(["ab", "-g"+filename, "-n "+str(MAX_CONNS), "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd1+"/"+rnd2+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
      else:
        subprocess.call(["ab", "-g"+filename, "-n "+MAX_CONNS, "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd1+"/"+rnd2+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
          
      # subprocess.call(["gnuplot", "-e FILENAME='"+filename+ "',TITLE='"+title+"'", "creategraphs.gp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
      # f.close()  
      None

  print '--> cleaning caches ...'
  clean_caches()
  if (mode == 'vertical'):
    MAX_CONNS = MAX_CONNS_ORIG

 
  print '--> tests using 3 words in search (3/3)'
  for i in range(1, MAX_TESTS):
    if (mode == 'vertical'):
      MAX_CONNS = MAX_CONNS_ORIG * i
           
    type = '3word'
    rnd1 = choice(dict)
    rnd2 = choice(dict)
    rnd3 = choice(dict)
    title = '(3words)selected random words: '+rnd1+ ', '+rnd2+', '+rnd3
    if (mode == 'vertical'):
      filename = mode+'_result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    else:
      filename = mode+'_result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt'
    
    print '('+filename+')'
    print '---'
    print '--> '+title
    if (mode == 'vertical'):
      print '--> command-line: ab -k -n '+str(MAX_CONNS)+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+str(MAX_CONNS)+'conns_'+MAX_CONCURRENT+'concurrent.txt'
    else:
      print '--> command-line: ab -k -n '+MAX_CONNS+' -c '+MAX_CONCURRENT+' ___ > result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent.txt'
    try:
      # f=open('result_'+type+'_'+MAX_CONNS+'conns_'+MAX_CONCURRENT+'concurrent-'+str(i)+'.txt','wb')
      if (mode == 'vertical'):
        subprocess.call(["ab", "-g"+filename, "-n "+str(MAX_CONNS), "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd1+"/"+rnd2+"/"+rnd3+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      else:
        subprocess.call(["ab", "-g"+filename, "-n "+MAX_CONNS, "-c "+MAX_CONCURRENT, HOSTNAME+"search/apachesolr_search/"+rnd1+"/"+rnd2+"/"+rnd3+"/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
      # subprocess.call(["gnuplot", "-e FILENAME='"+filename+ "',TITLE='"+title+"'", "creategraphs.gp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
      # f.close()  
      None
      

def options(argv):
   try:
      opts, args = getopt.getopt(argv, "vhcH")
   except getopt.GetoptError:
      print 'test.py [-v|--vertical] | [-h|--horizontal] | [-c|--cache] | -H "Help"'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-H':
         print 'test.py [-v|--vertical] | [-h|--horizontal] | [-c|--cache] | -H "Help"'
         sys.exit()
      elif opt in ("-v", "--vertical"):
         op = 'v'
         mode = 'Vertical Scalability.'
      elif opt in ("-h", "--horizontal"):
         op = 'h'
         mode = 'Horizontal scalability.'
      elif opt in ("-c", "--cache"):
         op = 'c'
         mode = 'Cache.'
      else:
         op = 'c'
         mode = 'Cache.'         
   print '   * testing: ', mode
   return op
   

if __name__ == "__main__":

    print '1. initializing global settings ...'
    global_consts()
    init_settings()
    
    print '2. generating dictionary ...'
    dict = generate_dictionary()
    
    print '3. cleaning caches ...'
    clean_caches()
    
    print '4. starting tests ...'
    op = options(sys.argv[1:])
    tests(dict, op)
    
    print '5. ...done.'
















