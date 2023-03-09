import WebBots as wb

scraper = wb.Reddit_Scraper()
posts = []
scraper.initialize()
scraper.goto_subreddit('popular')
posts = scraper.get_posts()
print(posts[0])
post = posts[0]
aHTML = scraper.get_webelement_HTML(post)
print(aHTML)
# scraper.fill_posts_list()



