
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#import pandas as pd
#from matplotlib import pyplot as plt
#import numpy as np 
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException



debug=False

# check if filename exist in cache
def cache_exists(filename):
    try:
        # write current page in cache
        with open('cache/'+filename, 'r') as cache_file:
            if debug:
                print('cache for this page exists')
            return cache_file.read()
    except:
        if debug:
            print('cache for this page doesn\'t exist yet!')
        return False

# split url in multiple parts
def get_url_path(url):
    if debug:
        print('call: get_url_path() '+url)
    parse = urlparse(url)
    if debug:
        print('url.path: '+parse.path)
    return parse.path

# get protocol and domain name from an url
def get_url_location(url):
    if debug:
        print('call: get_url_path() '+url)
    parse = urlparse(url)
    if debug:
        print('url.scheme: '+parse.scheme)
        print('url.netloc: '+parse.netloc)
    return parse.scheme+'://'+parse.netloc

# download page content and create cache if not exists
def get_page(url):
    if debug:
        print('call: get_page() '+url)
    # get the filename from the complete url
    filename = get_url_path(url)
    if debug:
        print('filename: '+filename)
    cache_page_content = cache_exists(filename)
    if cache_page_content:
        if debug:
            print('le cache existe')
        return cache_page_content
    else:
        if debug:
            print('le cache n\'existe pas')
        # cache doesn't exits
        # download the page content
        page_content = urllib.request.urlopen(url).read()
        # create empty cache file
        cache_file=open('cache/'+filename, 'wb')
        # write page content in cache
        cache_file.write(page_content)
        cache_file.close()
        return page_content


# count ratings (ex: note_client = 3)
def nb_rating(note_client):
    # ratings[3] = ratings[3] + 1
    ratings[note_client] = ratings[note_client]+1


# count ratings answers
def nb_rating_answer(note_client):
    ratings_answer[note_client] = ratings_answer[note_client]+1

# define comments and answers function
def get_comments_and_answers(soup):
    print("")
    print("Commentaires : ")
    print("===============")
    comment_id = 0
    
    ##add list object element2
    
    global nb_com
    global nb_rep
    global skipnext
    while comment_id < len(soup.find_all(class_="reviewSelector")):
        if skipnext:
            comment_id = comment_id+1
            #index=index+1
            skipnext = Falsenote
            continue;
        # get the node member in html
        member = soup.find_all(class_="reviewSelector")[comment_id].find(class_="info_text").find('div').get_text()
        print("Auteur : "+member)
        # get the node badge "number of reviews of each member" in html
        badge = soup.find_all(class_="reviewSelector")[comment_id].find(class_="badgeText").get_text().replace('avis', '')
        print("Avis : "+badge)
        # get the node date in html
        date = soup.find_all(class_="reviewSelector")[comment_id].find(class_="ratingDate").get_text()
        print(date)
        # get the node note_client (individual note) in html
        note_client = get_note(soup.find_all(class_="reviewSelector")[comment_id].find(class_="ui_bubble_rating").get("class")[1])
        print("Note client : "+note_client)
        # get the node title (verbatim) in html
        title = soup.find_all(class_="reviewSelector")[comment_id].find(class_="noQuotes").get_text()
        print("Titre : "+title)
        # get the node commentaire in html
        #commentaire = soup.find_all(class_="reviewSelector")[comment_id].find(class_="prw_reviews_text_summary_hsx").find('div').find('p')
        element2=browser.find_elements_by_class_name("partial_entry")
        #commentaire= soup.find_all(class_="partial_entry")[comment_id]
        commentaire = soup.find_all(class_="reviewSelector")[comment_id].find(class_="prw_reviews_text_summary_hsx").find('div').find('p')
        nb_com=nb_com+1
        #print("Commentaire : "+commentaire.get_text())
        print("Commentaire: " +element2[comment_id].text)
        print("")
        # get the node reponse in html
        #reponse = commentaire.parent.parent.parent.find(class_="mgrRspnInline")
        reponse = commentaire.parent.parent.parent.find(class_="mgrRspnInline")

        # if comment had an answer from the restaurant
        if reponse is not None:
            print("=== Reponse du restaurant : ===")
            print("")
            #print(reponse.find(class_="partial_entry").get_text())
            print(reponse.text)
            nb_rep=nb_rep+1
            comment_id=comment_id+1
            #index=index+1
            nb_rating_answer(note_client)
        else:
            print("Pas de reponse a ce commentaire")
        print("")
        print("---")
        print("")
        comment_id = comment_id + 1
        #index=index+1

# translate classname into integer note
def get_note(arg):
    if arg == "bubble_50":
        return "5"
    if arg == "bubble_45":
        return "4.5"
    if arg == "bubble_40":
        return "4"
    if arg == "bubble_35":
        return "3.5"
    if arg == "bubble_30":
        return "3"
    if arg == "bubble_25":
        return "2.5"
    if arg == "bubble_20":
        return "2"
    if arg == "bubble_15":
        return "1.5"
    if arg == "bubble_10":
        return "1"
    if arg == "bubble_05":
        return "0.5"
    if arg == "bubble_00":
        return "0"

# Starting !!!!!

url_to_scrap = "https://www.tripadvisor.fr/Restaurants-g187147-c20-Paris_Ile_de_France.html"
# child pages
#url_to_scrap = "https://www.tripadvisor.fr/Restaurant_Review-g187147-d19318900-Reviews-La_Table_de_Colette-Paris_Ile_de_France.html"
#url_to_scrap = "https://www.tripadvisor.fr/Restaurant_Review-g187147-d6575305-Reviews-Il_Etait_Un_Square-Paris_Ile_de_France.html"

# set the page content into a html variable
page_content = get_page(url_to_scrap)

# use BeautifulSoup to parse our html variable
soup = BeautifulSoup(page_content, "html.parser")

# _15_ydu6b => class for restaurant title
links = soup.find_all(class_="_15_ydu6b")
nb_com=0
nb_rep=0
skipnext=False
colonnes = 5
ratings = {"1":0,"2":0,"3":0,"4":0,"5":0}
ratings_answer = {"1":0,"2":0,"3":0,"4":0,"5":0}
print(ratings)

resto = 0
# loop for each links as link

for link in links:
    ###
    #resto=resto+1
    #if resto < 23:
    #    continue;
    ###
    # define variable restaurant_title with the content of the html tag
    restaurant_title = link.get_text()
    print ("")

    if restaurant_title[0].isdigit() == True:
        print(restaurant_title)
        print(link['href'])
        # scrap child pages
        page_content = get_page(get_url_location(url_to_scrap)+link['href'])
        soup = BeautifulSoup(page_content, "html.parser")
        print("")
        
        restaurant_name = soup.find_all(class_="_3a1XQ88S")[0].get_text()
        print("Restaurant : "+restaurant_name)
        note = soup.find_all(class_="r2Cf69qf")[0].get_text().replace(',','.')
        print("Note : "+note)
       
        page = 0
        # old 
        while page <= 1:
        #while page <= 6:
            # get comments
            if page == 0:
        #while page <= 6:
            # get comments
            
                # get comment for the first page
                #browser.find_element_by_css_selector('.taLnk.ulBlueLinks').click()
                ##add this after find_element_by_css
               browser=webdriver.Chrome('./chromedriver_win32/chromedriver')
               url =get_url_location(url_to_scrap)+link['href']###
               browser.get(url)
               browser.find_element_by_css_selector('.taLnk.ulBlueLinks').click()
               element2=browser.find_elements_by_class_name("partial_entry")
               get_comments_and_answers(soup)
               browser.close()
               
               
            
            else:

                # split url with "Reviews-"
                # link['href'] = 'Restaurant_Review-g187147-d19318900-Reviews-La_Table_de_Colette-Paris_Ile_de_France.html'
                # url_splited = ['Restaurant_Review-g187147-d19318900-',     'La_Table_de_Colette-Paris_Ile_de_France.html']
                url_splited = link['href'].split('Reviews-', 1)
                # new_url = 'Restaurant_Review-g187147-d19318900-' + 'Reviews-or' + str(page) + '0-' + 'La_Table_de_Colette-Paris_Ile_de_France.html'
                new_url = url_splited[0]+'Reviews-or'+str(page)+'0-'+url_splited[1]
                # get page content
                page_content = get_page(get_url_location(url_to_scrap)+new_url)
                
                   
                try:
                    browser=webdriver.Chrome('./chromedriver_win32/chromedriver')
                    browser.get(get_url_location(url_to_scrap)+new_url)
                    browser.find_element_by_css_selector('.taLnk.ulBlueLinks').click()
                    element2=browser.find_elements_by_class_name("partial_entry")
                    soup = BeautifulSoup(page_content, "html.parser")
                    # get comments for this page
                    get_comments_and_answers(soup)
                    browser.close()
                except NoSuchElementException:
                            
                                element2=browser.find_elements_by_class_name("partial_entry")
                                soup = BeautifulSoup(page_content, "html.parser")
                                # get comments for this page
                                get_comments_and_answers(soup)
                                browser.close()
                                
                
                
                
                
               

                    
            page = page + 1
                # Append our list with the values:

    else:
        print ("=== AD DETECTED ===")
        print (restaurant_title+" is ignored from our scrapping")
        print ("=== AD DETECTED ===")
    # print("nb_com: "+str(nb_com))
    # print("nb_rep: "+str(nb_rep))
    # for i in 1,2,3,4,5:
    #     print("commentaires avec "+str(i)+": "+str(ratings[str(i)]))
    #     print("reponses avec "+str(i)+": "+str(ratings_answer[str(i)]))
