from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np 
import time









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

    def initialize(self):
        self.driver = webdriver.Chrome() 
        self.driver.get('https://old.reddit.com/r/popular/')
    
    def click_next_page(self): #clicks the next page button on reddit
        element = self.driver.find_element(By.CSS_SELECTOR, "a[rel$='next']")
        element.click()
        self.driver.implicitly_wait(2)
        
    def get_pages(self, times): #gets this many pages worth of posts
        self.pages = []

        for i in range(times):
            posts = self.get_posts() #gets post from page
            for post in posts:
                tempPost = Reddit_Post()
                self.pages.append(tempPost.init_post(post, self.driver))
            
            self.click_next_page()
                
    def get_posts(self): #finds all posts on current page
        self.posts = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='even  link']")
        self.posts1 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='odd  link']")
        posts = self.posts + self.posts1
        return posts
 
        

    

class Reddit_Post(): 
    
    def init_post(self, item, driver): #initializes a post object with all post information
        self.driver = driver        
        title = self.get_title(item)
        score = self.get_upvotes(item)
        subreddit = self.get_subreddit(item)
        posttime = self.get_post_time(item)
        poster = self.get_OP(item)
        comments = self.get_comment_number(item)
        commentsURL = self.get_comments_URL(item)
        
        self.driver.back()
        
        returnDict = {"score":score, "title":title, "subreddit":subreddit, "post time":posttime, "OP":poster, "Number of Comments":comments, "URL":commentsURL}
        
        return returnDict #returns a dictionary of all info
        
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

    def get_comments_URL(self, post): #goes to comments on post given
        comments = post.find_element(By.CSS_SELECTOR, "a[data-event-action^='comments']")
        comments.click()
        WebDriverWait(self.driver,10).until(EC.url_contains('comments'))
        return self.driver.current_url

class Pandas_DataFrame(): 
    
    def initialize(self,data): #creates a Data Frame out of the Reddit posts
        self.dataFrame = pd.DataFrame(data)
        
    def write_to_csv(self): #writes Data Frame to file
        self.dataFrame.to_csv(r"C:\Users\Ethan\Documents\Coding\Web Scraper\Post Data\postdata.csv")
