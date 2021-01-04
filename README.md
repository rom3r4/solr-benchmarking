## [solr-benchmarking]()

Benchmarking script for Solr

### Requirements

- Python
- ab (Apache Benchmarks)
- gnuplot

### Installation 

(Installation tested on Debian wheezy GNU/Linux)

    $ wget https://github.com/julianromera/solr-benchmarking/archive/master.zip
    $ unzip master.zip
    $ cd apachesolr-benchs
    
    $ python tests.py
    
Command-line arguments:

    tests.py [-v|--vertical] | [-h|--horizontal] | [-c|--cache] | -H "Help"'
    
    -v Vertical Scalability tests
    -h Horizontal scalability tests
    -c Cleans caches
    -H this help

### Features

- Adjustable search words domain
- Graphic results (.jpeg)

### Author

University of Alcala

### LICENSE

This is free and unemcumbered software released into the public domain. For more information, see the accompanying UNLICENSE file.

If you're unfamiliar with public domain, that means it's perfectly fine to start with this skeleton and code away, later relicensing as you see fit.
