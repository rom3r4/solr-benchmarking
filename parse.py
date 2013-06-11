#!/usr/bin/python

#
#

#
# DEPRECATED. NOT USED
#

from os import listdir, walk
from os.path import isfile, join

def global_consts():
  global PATH
  global PREFIX 
  # number of n-uples in searches default is 3 <-- 1word 2words 3words
  global NUM_TYPES
  
  PREFIX = "result_"
  PATH = "./"
  NUM_TYPES = 3

def get_files():
  
  # method 1
  files = [ f for f in listdir(PATH) if (isfile(join(PATH,f)) and f.startswith(PREFIX)) ]

  # method 2
  # f = []
  # for (dirpath, dirname, filenames) in walk(PATH):
  #   f.extend(filenames)  
  #   break
    
  return files
  
  
if __name__ == "__main__":
  print '1. initializing variables ..'
  global_consts()
  
  print '2. retrieving files from filesystem...'
  f = get_files()
  
  print '3. ----'
  
  for a in f:
    print a
  
  print '4. ...ending.'
  
