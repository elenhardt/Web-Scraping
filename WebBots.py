from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np 
import time


#Items to add:
#Reorganize classes, use inheritance, follow good coding practices
#Create methods to parse through and create comments.
#Change all implicit waits to expected conditions





class Chrome_Browser():

    def initialize(self): #creates webdriver to operate chrome
        self.driver = webdriver.Chrome()     
    
    def goto_site(self, URL):     
        self.driver.get(URL)
        WebDriverWait(self.driver,10).until(
            EC.url_contains(URL))
    
    def get_URL(self):
        return self.driver.current_url
           
    def tear_down(self): #discards driver
        self.driver.quit()
        
class Reddit():
    
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
    
        
