from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os.path
import pandas as pd



#Items to add:
#Reorganize classes, figure out what to do with Chrome_Browser() class
#Create class/methods to parse through and create comments.
#Change all implicit waits to expected conditions
#Find more efficient way to get post comment URL's




class Chrome_Browser():

    def initialize(self): #creates webdriver to operate chrome
        self.driver = webdriver.Chrome()     
    
    def goto_site(self, URL):     
        self.driver.get(URL)
        WebDriverWait(self.driver,10).until(
            EC.url_contains(URL))
    
    def get_URL(self):
        return self.driver.current_url
    
    def get_page_HTML(self):
        self.HTML = self.driver.page_source
    
    
    
    def tear_down(self): #discards driver
        self.driver.quit()
        
class Reddit(Chrome_Browser):
    
    def login(self, username , password): #takes a reddit account username or password
        
        self.driver.get("https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F") #gets log in page
        WebDriverWait(self.driver, 10).until(EC.title_contains('reddit.com'))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))) #Checks for username
        
        element = self.driver.find_element(By.NAME, "username")
        element.send_keys(username) #sends username
        
        element = self.driver.find_element(By.NAME, "password")
        element.send_keys(password)
        
        element = self.driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(self.driver, 10) #just waits to ensure smooth runtime  
                             
    def click_next_page(self): #clicks the next page button on reddit
        element = self.driver.find_element(By.CSS_SELECTOR, "a[rel$='next']")
        element.click()
        self.driver.implicitly_wait(2)
        

                

        
class Reddit_Scraper(Reddit): #Reddit Scraper class
            
    def get_webelement_HTML(self,element): #gets HTML of selenium web element
        webelementHTML = element.get_attribute("innerHTML")
        return webelementHTML        
        
    def initialize_lists(self): #initializes all primary lists for scraper
        self.parser = Reddit_Post()
        
    def get_posts(self): #finds all Non-AD posts on current page
        posts2 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='even  link']")
        posts1 = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='odd  link']")
        posts = posts1 + posts2
        return posts

    

class Pandas_DataFrame():
    
    def initialize(self,posts):
        self.dataFrame = pd.DataFrame(posts)
        
    def write_to_csv(self):
        self.dataFrame.to_csv(r"C:\Users\Ethan\Documents\Coding\Web Scraper\Post Data\postdata.csv")



class HTML_Parser():
    
    def initialize(self, HTML):
        self.HTML = BeautifulSoup(HTML)
        
    def get_attribute(self, CSS_Attribute):
        attribute = self.HTML.select(CSS_Attribute)
        return attribute
        
class Reddit_Post(HTML_Parser):
    
    def create_post_dictionary(self):
        self.title = self.get_attribute("[class^= 'title']")
        self.score = self.get_attribute("[class^= 'score unvoted']")
        self.subreddit = self.get_attribute("[class^= 'subreddit']")
        self.posttime = self.get_attribute("[class^= 'live-timestamp']")
        self.poster = self.get_attribute("[class^= 'author']")
        self.comments = self.get_attribute("[class*= 'comments']")
        # self.commentsURL = self.get_post_comments_URL()
        
        return {'title':self.title, 'score':self.score, 'subreddit':self.subreddit, 
                'posttime':self.posttime, 'OP':self.poster, 'comments':self.comments
                # , 'URL':self.commentsURL
                }
            
    # def get_post_comments_URL(self):
    #     URLparser = HTML_Parser()
    #     URLparser.initialize(self.comments)
    #     URLparser.HTML.find('a',href=True)
        
        
        