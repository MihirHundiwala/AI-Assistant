from urllib.parse import urlparse
import webbrowser
import re
import lxml
from lxml import etree
from bs4 import BeautifulSoup
from utilities.speech_functions import * 
import urllib
import requests
from utilities.confirm import *
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

def checkconn():
    try:
        requests.get('https://www.google.com/').status_code
        print('Connected')
        return True
    except:
        print('Not Connected')
        speak('Please connect to internet')
        return False

def parse_results(response):    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)
    # print(results)

    output = []
    
    for result in results:
        # print('in for')

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href']             
        }
        try: 
            result.find(css_identifier_text, first=True).text
            item['text']=result.find(css_identifier_text, first=True).text
        except:
            item['text']=''
        
        output.append(item)
        
    return output

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    
    return response

def google_search(query):
    response = get_results(query)
    return parse_results(response)

def search_for():
    if checkconn():
        print("What should I search for?")
        speak("What should I search for?")
        statement = listen()
        query = statement.replace("search", "")
        results = google_search(query)
        result = ''
        j=''
        # print(results)
        for a in results:
            desc= a['text']
            if not(desc==''):
                if len(desc) > 100:
                    text = desc.partition('.')[0] + '.'
                    t = urlparse(a['link']).netloc
                    titl=t.split('.')[-2:][0]
                    result = "According to "+titl+" : "+text
                    j=a['link']
                    break;

        print(result)
        speak(result)
        print('Do you want to open the site?')
        if confirm(speech="Do you want to open the site?", abort_txt="Okay task aborted"):
            webbrowser.open_new_tab(j)
            return


def youtube():
    if checkconn():
        print("What should I play?")
        param = listen()
        chelen = param.split()
        if len(chelen)>1:
            param=param.replace(' ','+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + param)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        final = "https://www.youtube.com/watch?v=" + video_ids[0]   
        response = get_source(final)
        # execute Javascript
        response.html.render(sleep=1, timeout=60)
        # create beautiful soup object to parse HTML
        soup = bs(response.html.html, "html.parser")
        title=soup.find("meta", itemprop="name")['content']
        s="Found "+title
        print(s)
        speak(s)
        speak('Do you want to view on youtube?')
        print('Do you want to view on youtube?')
        while True:
            stat= listen()
            if 'yes' in stat:
                webbrowser.open_new_tab(final)
                return
            else:
                return
