from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
<<<<<<< Updated upstream
=======

from bs4 import BeautifulSoup
import soupsieve as sv

import os.path

import requests

>>>>>>> Stashed changes
import pandas as pd
import numpy as np 
import time


#Items to add:
<<<<<<< Updated upstream
#Reorganize classes, use inheritance, follow good coding practices
#Create methods to parse through and create comments.
#Change all implicit waits to expected conditions
=======
#Change all implicit waits to expected conditions
#Download Image or post text, attach to post


>>>>>>> Stashed changes





class Chrome_Browser():

    def initialize(self): #creates webdriver to operate chrome. Make sure initialize any Browser child classes.
        self.driver = webdriver.Chrome()     
    
    def goto_site(self, URL):     #goes to site
        self.driver.get(URL)
        WebDriverWait(self.driver,10).until( #waits for page to be loaded
            EC.url_contains(URL))
    
    def get_URL(self): #returns current web URL
        return self.driver.current_url
<<<<<<< Updated upstream
           
    def tear_down(self): #discards driver
        self.driver.quit()
        
class Reddit():
=======
    
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
>>>>>>> Stashed changes
    
    # def login(self, username , password): #takes a reddit account username or password
        
    #     self.driver.get("https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F") #gets log in page
    #     WebDriverWait(self.driver, 10).until(EC.title_contains('reddit.com'))
    #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))) #Checks for username
        
    #     element = self.driver.find_element(By.NAME, "username")
    #     element.send_keys(username) #sends username
        
    #     element = self.driver.find_element(By.NAME, "password")
    #     element.send_keys(password)
        
    #     element = self.driver.find_element(By.TAG_NAME, "button").click()
    #     WebDriverWait(self.driver, 10) #just waits to ensure smooth runtime                   

    def initialize(self, pages):
        self.driver = Chrome_Browser()
        self.driver.initialize('https://old.reddit.com/r/popular/')
        self.posts = self.get_pages(pages)
    
    def click_next_page(self): #clicks the next page button on reddit
        element = self.driver.find_element(By.CSS_SELECTOR, "a[rel$='next']")
        element.click()
        self.driver.implicitly_wait(2)    
        
<<<<<<< Updated upstream
    def get_pages(self, times): #gets this many pages worth of posts
        returnlist = []
        for i in range(times):
            returnlist.append(self.get_posts()) #gets post from page
            
            # for item in posts:
            #     tempDict = .init_post(item) #create a dictionary containing post data
            #     returnlist.append(tempDict)
            
            self.click_next_page()
            
        return returnlist   
    
    def get_posts(self): #finds all posts on current page
        self.posts = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='even  link']")
        self.posts1 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='odd  link']")
        posts = self.posts + self.posts1
        return posts
 

    def goto_comments(self, post): #goes to comments on post given
        comments = post.find_element(By.CSS_SELECTOR, "a[data-event-action^='comments']")
        comments.click()
        WebDriverWait(self.driver,10).until(EC.url_contains('comments'))
        return self.driver.current_URL

    # def get_comments(self, commentssection):
    #     comments = commentssection.find_elements(By.CSS_SELECTOR, "div[id^='thing']") 
    #     return comments #returns list of comments
        

class Reddit_Post_List(): 
    
    def init_post(self, item, driver): #initializes a post object with all post information
            
        title = self.get_title(item)
        score = self.get_upvotes(item)
        subreddit = self.get_subreddit(item)
        posttime = self.get_post_time(item)
        poster = self.get_OP(item)
        comments = self.get_comment_number(item)
        commentsURL = self.get_comments_URL(driver, item)
        
        returnDict = {"score":score, "title":title, "subreddit":subreddit, "post time":posttime, "OP":poster, "Number of Comments":comments, "Comments URL":commentsURL}
        
        return returnDict #returns a dictionary of all info
        
    # def get_comments_URL(self, driver, post):
    #     driver.goto_comments(post)
        
    #     return commentsURL      
    
    def get_title(self, post): #gets title
        title = post.find_element(By.CSS_SELECTOR, "p[class^= 'title']" )
        return title.text
        
    def get_upvotes(self, post): #gets score
        score = post.find_element(By.CSS_SELECTOR, "div[class^= 'score unvoted']" )
        return score.text
        
    def get_subreddit(self, post): #gets subreddit
        subreddit = post.find_element(By.CSS_SELECTOR, "a[class^= 'subreddit']" )
        return subreddit.text
    
    def get_post_time(self, post): #gets posted time
        posttime = post.find_element(By.CSS_SELECTOR, "time[class^= 'live-timestamp']" )
        return posttime.text
        
    def get_OP(self, post): #gets OP
        poster = post.find_element(By.CSS_SELECTOR, "a[class^= 'author']" )
        return poster.text
    
    def get_comment_number(self, post): #gets number of comments
        comments = post.find_element(By.CSS_SELECTOR, "a[class*= 'comments']" )
        return comments.text   

# class file_generator():
    
=======
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
    
            

>>>>>>> Stashed changes
        
