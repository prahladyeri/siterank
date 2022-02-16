#!/usr/bin/env python3
##
# Script to fetch alexa ranks for one or more websites.
# Usage: siterank <url1> <url2> ....
#
# @author Prahlad Yeri
#
import time, pickle, sysconfig
import urllib.request
import sys, os
import argparse
import xml.etree.ElementTree as ET
from siterank import __title__, __version__

#@todo: move this to a common util library
def get_install_path():
    tpath = sysconfig.get_path('purelib') + os.sep + "siterank"
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    return tpath

# check/load local cache
cache = {}
pkl_path = get_install_path() + os.sep + "siterank.pkl"
if os.path.exists(pkl_path):
    cache = pickle.load(open(pkl_path, 'rb'))
    print("successfully imported cache. %d records found.." % len(cache.keys()))
else:
    cache = {}
    pickle.dump(cache, open(pkl_path, 'wb'), -1) 
    print("cache doesn't exist, created cache..")


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

def get_ranks(url_list, refresh=False):
    ranks = {}
    #for url in url_list:
    cnt = len(url_list)
    for i in range(cnt):
        url = url_list[i]
        if not refresh:
            # check local cache, if found, no need of requesting
            if url in cache: # found
                print("found in cache:", url)
                ranks[url] = cache[url]
        if url not in ranks:
            print("fetching live:", url)
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
                cache[url] = ranks[url] # also save to cache
                pickle.dump(cache, open(pkl_path,'wb'), -1)
        ss = "%d/%d. %s" % (i+1,cnt, url.ljust(100))
        print(ss, end='\r', flush=True)
        if i>0 and i%30 == 0:
            #print(i, 'wait')
            time.sleep(3)
    print("")
    return ranks
    
def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        print( "%s version %s" % (__title__, __version__) )
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('list', nargs='+', default=[], help='List of URLs EX: www.google.com www.yahoo.com etc.')
    parser.add_argument('-r', '--refresh', help='Refresh cache', action='store_true')
    parser.add_argument('-v', '--version', help='Display Version', action='store_true')
    args = parser.parse_args()
    
    ranks = get_ranks(args.list, args.refresh)
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
