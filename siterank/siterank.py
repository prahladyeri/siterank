#!/usr/bin/env python3
##
# Script to fetch alexa ranks for one or more websites.
# Usage: siterank <url1> <url2> ....
#
# @author Prahlad Yeri
#
import time, sysconfig
import urllib.request
import ssl, certifi
import sys, os
import argparse
import sqlite3, json
from siterank import __title__, __version__

ctx = ssl.create_default_context(cafile=certifi.where())


#@todo: move this to a common util library
def get_config_path():
    #tpath = sysconfig.get_path('purelib') + os.sep + "siterank"
    tpath = os.path.expanduser("~/.config/")
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    return tpath

def load_settings():
    global settings
    if os.path.exists(settings_path):
        settings = json.loads(open(settings_path, 'r').read())
    else:
        open(settings_path, 'w').write( json.dumps(settings) )
        
settings = {'api_key': ''} # default settings
db_path = os.path.join(get_config_path(), "siterank.db")
settings_path = os.path.join(get_config_path() , "siterank-settings.json")
sql = "select 1"
if not os.path.exists(db_path):
    sql = "create table sites(id integer primary key, domain varchar(255), rank int, unique(domain))"

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
conn.execute(sql)
print("successfully imported cache db..")

def get_ranks(url_list, refresh=False):
    ranks = {}
    #for url in url_list:
    cnt = len(url_list)
    for i in range(cnt):
        url = url_list[i]
        if not refresh:
            # check local cache, if found, no need of requesting
            rows=conn.execute("select * from sites where domain=?", [url]).fetchall()
            if len(rows)>0: # found
                print("found in cache:", url)
                ranks[url] = rows[0]['rank']
        if url not in ranks:
            print("fetching live:", url)
            turl = "https://api.similarweb.com/v1/similar-rank/%s/rank?api_key=%s" % (url, settings['api_key'])
            #print("fetching live:", turl)
            req = urllib.request.Request(turl)
            try:
                fp= urllib.request.urlopen(req, context=ctx)
                output = fp.read().decode('utf-8')
                obj = json.loads(output)
                #print('obj:', obj)
                if obj['meta']['status'] != 'Error':
                    rnk = int(obj['similar_rank']['rank'])
                    ranks[url] = rnk
                    conn.execute("delete from sites where domain=?", [url])
                    conn.execute("insert into sites(domain,rank) values(?,?)", [url, rnk])
                    conn.commit()
            except urllib.error.HTTPError as e:
                print("NOT FOUND:", url)
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
    load_settings()
    if settings['api_key'] == '':
        print("The API Key is empty!")
        print("[1] Please visit https://www.similarweb.com/corp/ranking-api/ and create a free account and generate an API Key.")
        print("[2] Once done, copy that API Key and put it in the below JSON file:\n\n" + settings_path)
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('list', nargs='+', default=[], help='List of domains EX: www.google.com www.yahoo.com etc.')
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
