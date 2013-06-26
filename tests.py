#!/usr/bin/python

# This test file aims test a Solr
# platform (Drupal + Solr in our case).
# the goail is to provide a realistic 
# scenario where all the searches dont get
# retrieved from cache. We do so by generating 
# a long list of unique words and query the server.
# At last, the server content has previously 
# populated with these unique words
# 


from random import choice
import subprocess, os, sys, getopt


def global_consts():

    # set these to a low number and MAX_TESTS
    # to a hight number, to minimize caches and
    # get a more real approach 
    global MAX_CONNS
    global MAX_CONCURRENT
    
    global HOSTNAME
    global MAX_TESTS

    # settig CONNS to 3 we will get more realistic 
    # mean/ average values. Also, imho this wont
    # affect cache hits and therefor, the Solr
    # performance test
    
    # MAX_CONNS value is set to 3. One of those values
    # comes from a empty cache, the rest 2/3 comes from
    # primed caches. This will result on a high standard 
    # deviation on the result, and, in the other side, 
    # a more realistic value, since the cache system 
    # is going to be present on that system
    MAX_CONNS = '3'
    MAX_CONCURRENT = '1'
    # include 'http://' and a triling '/' at the end    
    HOSTNAME = "http://voa3r7.appgee.net/"
    
    # using here number lower than the words in the
    # generated dictionary ( about 30000) will
    # ensure our test that the queryed words are 
    # not likely cached
    MAX_TESTS = 2
    
    
    
def generate_dictionary():


  # how many sufixeds should i create per each root.
  # e.g: root_elephant1, root_elephant2 <-- 2
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
      
  # 34 items x 30 iteraction = 1400 combinations      
  # about 1.000 with this setup
  print '--> generated '+ str(len(DICT)) +' words in dictionary'      
  return DICT



def init_settings():

  # non permanent changes
  # this fixed the "too many open connections error"
  # of the Apache Bench command
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
    # 3 x 400 should be lower (1400) that the total
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
















