# coding: utf-8

"""
https://github.com/musikalkemist/midiget/
を参考に、python3で動かなくなっている部分を変更したもの
また、HTTPErrorやURLerrorも例外処理で避けられるように極力しています。by岩名
このコードのライセンスはMITライセンスのため商用可能だと思います。
"""

"""
(c) Valerio Velardo, velardovalerio@gmail.com, 2015

This program crawls the pages of a website and downloads all the midi files it
finds. The midi files are saved in a directory called 'savedmidi'. 
The program is launched from the command line. 2 parameters should be 
specified:
 1- the url of the start page 
 2- the max number of pages to crawl before the program stops

The second parameter is optional (default value = 1000 pages)
"""

import re
import time
import os
import errno
import sys
import socket
from socket import timeout
import urllib
from urllib.parse import *
from urllib.request import urlopen
import bs4 as bs 

"""
start_page 最初crawkingするURL
MAX_PAGES crawringから何ページ先のURLまで掘るか
save_folder:保存先のfolder名by 岩名
"""
def crawl_and_save(start_page, MAX_PAGES,save_folder):
    """ Crawl pages of website from start_page and save all midi files"""
    start_time = time.time()
    page = 1
    links_to_crawl = [start_page]
    links_crawled = []
    url_files = []
    url_start_page = urlparse(start_page)
    netloc = url_start_page.netloc    
    # loop over the pages of the website 
    while page <= MAX_PAGES:
        page_to_download = links_to_crawl[0]
        # page_to_download = page_to_download.replace(" ", "%20")
        sauce = urlopen(page_to_download).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        print(page_to_download)
        # loop over all links in a page
        for link_tag in soup.find_all('a'):
            href = str(link_tag.get('href'))
            href = str(handle_relative_link(page_to_download, href))
            # check link wasn't encountered before and is internal
            if (href not in links_crawled and 
                href not in links_to_crawl and
                is_internal_link(href, netloc) and 
                href not in url_files):
                # check if links takes to a midi file
                if is_midi(href):
                    file_name = href.split('/')[-1]
                    url_files.append(href)
                    save_file(href, file_name,save_folder)#変更箇所:save_fileの入力項目を追加したため、save_folderを加えてますby岩名
                    print("Saved: ", file_name)
                else:
                    links_to_crawl.append(href)
        links_crawled.append(links_to_crawl.pop(0))
        if page % 10 == True:
            pagesPerSec = (time.time() - start_time) / page
            print()
            print('Pages crawled:', page)
            print('Time so far:', time.time() - start_time, "sec") 
            print('Avg time per page:', pagesPerSec, "sec")
            print()
        page = page + 1
        # exit if MAX_pages is reached
        if page == MAX_PAGES:
            print()
            print("Max no. of pages reached!")
            print()
            sys.exit(0)
        # exit if all pages have been crawled
        if len(links_to_crawl) == 0:
            print()
            print("All the pages of the website have been crawled!")
            print()
            break
        
def is_internal_link(link, netloc):
    """ Check if a link belongs to the website"""
    
    return bool((re.search(netloc, link)))
    
# function needed to handle relative links
#変更箇所:保存先のfolderを記載する場所が変更前だと複数あったため、__main__でのsave_pathだけ変えれば反映できるようにsave_file関数の入力変数にsave_folderを追加しています。by岩名
def save_file(url_file, file_name,save_folder):  
    """ Save midi file in directory 'midisaves'"""
    # url_file = re.sub("\!|\'|\?|\t","",url_file)
    path = save_folder + file_name
    # path = re.sub("\!|\'|\?|\t| ","",path)
    #HTTPErrorやURLErrorで止まっていたので、例外処理してError起こっても無視して次に行くようにしてます。by岩名
    try:
        res=urllib.request.urlopen(url_file,timeout=10)
    except urllib.error.HTTPError as e:
        print("raise HTTPError")
    except urllib.error.URLError as e:
        print("raise URLError")
    
    else:
        try:
            data = urllib.request.urlopen(url_file,timeout=10).read()
        except urllib.error.URLError as e:
                if isinstance(e.reason,socket.timeout):
                    pass
        with open(path, mode="wb") as f:
            f.write(data)
    

# handle relative links
def handle_relative_link(base_link, link):
    """" If necessary, transform relative links into absolute links"""
    
    if bool(re.search('^http', link)):
        return link
    else:        
        return urljoin(base_link, link)

def is_midi(link):
    """ Check if a link leads to a midi file"""
    
    return bool(re.search('\.mid$|\.midi$', link))
    
def make_sure_path_exists(path):
    """ Check if 'savemidi' directory exists, otherwise create it"""
    
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def check_type_max_pages(MAX_PAGES):
    """ Check that max_pages argument input by user is int"""
    
    try:
        int(MAX_PAGES)
    except ValueError:
        print()
        print("The 2nd argument (i.e., max no. pages) must be an integer.")
        print()
        sys.exit(0)

def check_no_args(arguments):
    """ Check that user has input at least 1 argument"""
    
    if len(arguments) < 2:
        print()
        print("At least 1 argument (i.e., start page) must be provided.")
        print()
        sys.exit(0)
        
def check_start_page_url(start_page):
    """ Check that start_page argument input by the user is a valid url"""
    
    try:
        urlopen(start_page).read()
    except IOError:
        print()
        print("Insert valid url (e.g., http://google.com).")
        print()
        sys.exit(0)
        
if __name__ == "__main__":
    #指定したpath配下にスクレイピングで入手したmidiファイルを保存by岩名
    #使い方　python migdiget.py スクレイピングしたいURL　クローリングしたいページ最大数　
    # by岩名
    save_path="savedmidi_vgmusic/"
    # check args are ok
    check_no_args(sys.argv)
    start_page = sys.argv[1]
    check_start_page_url(start_page)
    if len(sys.argv) > 2:
        check_type_max_pages(sys.argv[2])
        MAX_PAGES = int(sys.argv[2])
    else:
        MAX_PAGES = 100
    #ここで保存したいフォルダのpathを入れる
    make_sure_path_exists(save_path)
    crawl_and_save(start_page, MAX_PAGES,save_path)    
    










