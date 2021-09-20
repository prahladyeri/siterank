#!/usr/bin/env python3
##
# Script to fetch alexa ranks for one or more websites.
# Usage: siterank <url1> <url2> ....
#
# @author Prahlad Yeri
#
import time
import urllib.request
import sys, os
import argparse
import xml.etree.ElementTree as ET
from siterank import __title__, __version__

def split_dict(data, size=10):
    #s = {}
    s = []
    keys = list(data.keys())
    for i in range(0, len(keys), size):
        #s[i] = {}
        dct = {}
        for j in range(i, i+size):
            if j >= len(keys): break
            key = keys[j]
            dct[key] = data[key]
        s.append(dct)
    return s

def get_ranks(url_list):
    ranks = {}
    #for url in url_list:
    for i in range(len(url_list)):
        url = url_list[i]
        turl = "http://data.alexa.com/data?cli=10&url=" + url
        req = urllib.request.Request(turl)
        with urllib.request.urlopen(req) as fp:
            output = fp.read().decode('utf-8')
            tree = ET.ElementTree(ET.fromstring(output))
            root = tree.getroot()
            sd = root.find("SD")
            if sd != None:
                rnk = int(sd.find("POPULARITY").get("TEXT"))
                ranks[url] = rnk
            else:
                #not_found.append(url)
                ranks[url] = -1
        if i%30 == 0:
            #print(i, 'wait')
            time.sleep(3)
    return ranks
    
def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        print( "%s version %s" % (__title__, __version__) )
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('list', nargs='+', default=[], help='List of URLs EX: www.google.com www.yahoo.com etc.')
    parser.add_argument('-v', '--version', help='Display Version', action='store_true')
    args = parser.parse_args()
    
    ranks = get_ranks(args.list)
    sranks = [(k,ranks[k] if ranks[k]<1000 else str(int(ranks[k]/1000)) + "k") for k in sorted(ranks, key=ranks.get, reverse=False)]
    
    col_len = 40
    cols = 2
    #row_format ="{:>10}" * (len(sranks.keys()) + 1)
    row_format = ("{:<%d}" % col_len) * cols
    print("")
    print("*" * col_len * cols)
    print(" ", row_format.format("Website", "Rank"))
    print("*" * col_len * cols)
    for k,v in sranks:
        # rank = v
        # if rank > 1000:
            # rank = str(int(rank/1000)) + "K"
        #print(k, v)
        print(" ", row_format.format(k, v))


if __name__ == "__main__":
    main()
