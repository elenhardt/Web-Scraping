from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup
import soupsieve as sv

import os.path

import requests

import pandas as pd
import numpy as np 
import time




#Change all implicit waits to expected conditions
#Download Image or post text, attach to post







class Chrome_Browser():

    def initialize(self): #creates webdriver to operate chrome. Make sure initialize any Browser child classes.
        self.driver = webdriver.Chrome()     
    
    def goto_site(self, URL):     #goes to site
        self.driver.get(URL)
        WebDriverWait(self.driver,10).until( #waits for page to be loaded
            EC.url_contains(URL))
    
    def get_URL(self): #returns current web URL
        return self.driver.current_url

    
    def get_page_HTML(self): #gets HTML data of webpage
        self.HTML = self.driver.page_source
    
    def get_webelement_HTML(self, webelement): #gets HTML of selenium web element
        webelementHTML = webelement.get_attribute("innerHTML")
        return webelementHTML        
    
    def wait(self):
        self.driver.implicitly_wait(2)
    
    def tear_down(self): #discards driver
        self.driver.quit()
        
        
class HTML_Parser(): #creates parser for HTML data of posts
    
    def initialize(self, HTML): #creates an HTML parser
        self.HTML = BeautifulSoup(HTML, "html.parser")        
        
        
class Pandas_DataFrame(): #Allows for creation of Pandas DataFrame
    
    def initialize(self, postslist): #creates dataFrame of organized post data
        self.dataFrame = pd.DataFrame(postslist)
        
    def write_to_csv(self): #writes the dataframe to csv
        if(os.path.exists(r"\postdata.csv")):
            self.dataFrame.to_csv(r'postdata.csv', mode='a', index=False, header = False)
        self.dataFrame.to_csv(r"C:\Users\Ethan\Documents\Coding\Web Scraper\Post Data\postdata.csv", mode='w', index=False, header=True)   
             

class Reddit(Chrome_Browser):            

    def initialize(self):
        self.driver = webdriver.Chrome() 
        self.driver.get('https://old.reddit.com/r/popular/')
    
    def click_next_page(self): #clicks the next page button on reddit
        element = self.driver.find_element(By.CSS_SELECTOR, "a[rel$='next']")
        element.click()
        self.driver.implicitly_wait(2)    

    def goto_subreddit(self, subreddit): #goes to specific subreddit
        self.goto_site('https://old.reddit.com/r/' + subreddit + '/')
        
    def goto_reddit_comments(self, URL):
        self.goto_site('https://old.reddit.com' + URL)

        
class Reddit_Scraper(Reddit): #Reddit Scraper class
                   
    def create_HTML_list(self): #creates a list of HTML code of each reddit post
        self.HTMLlist = []
        for post in self.posts:
            self.HTMLlist.append(self.get_webelement_HTML(post))  
        
    def initialize_lists(self): #initializes all primary lists for scraper
        self.postslist = []
        self.posts = []
        self.parser = Reddit_Post()
        
    def get_posts(self): #finds all Non-AD posts on current page
        posts2 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='even  link']")
        posts1 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='odd  link']")
        posts = posts1 + posts2
        return posts
        
        
    def get_page(self): #gets this many pages worth of posts
        self.get_posts()
        self.postslist.append(self.create_HTML_list()) 
        
        
    def get_pages(self, times):
        for i in range(times):
            self.get_page()
            self.fill_posts_list()
            self.click_next_page()
        
    def fill_posts_list(self): #fills postslist with data about each reddit post
        for post in self.postslist:
            self.parser.initialize(post)
            self.postslist.append(self.parser.create_post_dictionary())  
        
        
class Reddit_Post(HTML_Parser): #allows for creation of Reddit Post Objec
    
    def create_post_dictionary(self): #creates a dictionary of Reddit Data
        self.title = self.get_title()
        self.score = self.get_score()
        self.subreddit = self.get_subreddit()
        self.posttime = self.get_posttime()
        self.poster = self.get_poster()
        self.comments = self.get_comments()
        self.commentsURL = self.get_post_comments_URL()
        
        return {'title':self.title, 'score':self.score, 'subreddit':self.subreddit, 
                'posttime':self.posttime, 'OP':self.poster, 'comments':self.comments
                , 'URL':self.commentsURL #returns a dictionary representing the reddit post
                }

    
    def get_title(self):
        title = self.HTML.find('p', class_='title').get_text()
        return title
    
    def get_score(self):
        returnvalue = self.HTML.find('div', class_='score unvoted')
        return returnvalue.get('title')    
            
    def get_subreddit(self):
        returnvalue = self.HTML.find('a', class_='subreddit hover may-blank').get_text()
        return returnvalue    
            
    def get_posttime(self):
        returnvalue = self.HTML.find('time', class_='live-timestamp')
        return returnvalue.get('title')
            
    def get_poster(self):
        returnvalue = self.HTML.find('a', href=lambda href: href and 'user' in href)
        return returnvalue.get('href')    
            
    def get_comments(self):
        returnvalue = self.HTML.find('a', class_='bylink comments may-blank').get_text()
        return returnvalue    
            
    def get_post_comments_URL(self): #gets the URL to go to posts comments
        link = self.HTML.find('a', href=lambda href: href and 'comments' in href)
        return link.get('href')
    
            

