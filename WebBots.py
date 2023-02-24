from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Test username: 696969qwerty696969
#Test Password: TestPassword123!

#Items to add:
#Check to see whether login is successful
#Check on whether posts could be found
#Ability to comment
#Ability to analyze post



class Reddit_Bot():

    def initialize(self): #creates webdriver to operate chrome
        self.driver = webdriver.Chrome()        
       
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
                   
    def goto_comments(self, post):
        comments = post.find_element(By.CSS_SELECTOR, "a[data-event-action^='comments']")
        comments.click()
        WebDriverWait(self.driver,10).until(EC.url_contains('comments'))
        
        commentsection = self.driver.find_element(By.CLASS_NAME, 'commentarea')
        return commentsection    

    def goto_subreddit(self, subreddit):
        URL = 'https://old.reddit.com/r/' + subreddit +'/'
        self.driver.get(URL)
        WebDriverWait(self.driver,10).until(
            EC.url_contains(subreddit))
    
    def get_posts(self):
        main = self.driver.find_element(By.ID, "siteTable") #finds all posts on current page
        posts = main.find_elements(By.CSS_SELECTOR, "div[id^='thing']")
        return posts #returns list of posts

    def get_comments(self, commentssection):
        comments = commentssection.find_elements(By.CSS_SELECTOR, "div[id^='thing']") 
        return comments #returns list of comments
        
    def tear_down(self): #discards driver
        self.driver.quit()



        
        
    
        
        


    

    
    



