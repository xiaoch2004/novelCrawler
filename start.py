#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import copy,pdb
import csv,smtplib

# This script grabs the novel from www.biqugex.com

def getOneChapter(addr):
    try:
        res = urlopen(addr)
        soup = BeautifulSoup(res,"html5lib")
        target = soup.find_all(id="content")
    except IncompleteRead as e:
        print("IncompleteRead!\n")
        return e.partial
    for br in target[0].find_all("br"):
        br.replace_with("\n")
    return target[0].get_text()
    

def DeleteNoiseInfo(s):
    pos = s.find("http:")
    return s[:(pos-1)]+'\n'
    
def GoToFile(fid,s):
    fid.write(DeleteNoiseInfo(s))
    
def AppendUrlToFile(fid,url):
    content = getOneChapter(url)
    output = DeleteNoiseInfo(content)
    GoToFile(fid,output)

def GetChapterUrlList(addr,startchap):
    res = urlopen(addr)
    soup = BeautifulSoup(res,"html5lib")
    target = soup.find_all('a')
    startpos = startchap + 31
    target = target[startpos:1414]
    addrlist = []
    for t in target:
        addrlist.append("http://www.biqugex.com"+t['href'])
    return addrlist
    
if __name__=="__main__":
    fid = open("novel655-.txt","a")
    addr = "http://www.biqugex.com/book_795/"
    i = 663
    addrlist = GetChapterUrlList(addr,i)
    for url in addrlist:
        AppendUrlToFile(fid,url)
        i = i + 1
        print("第 "+str(i)+" 章抓取完毕!")
        time.sleep(2)
    fid.close()