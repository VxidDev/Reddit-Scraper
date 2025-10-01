from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from colorama import Fore , Style
from random import uniform
from time import sleep
from selenium.common import exceptions
import pathlib , csv , subprocess , datetime

def Message(text , clear: bool = True):
    if clear:
        subprocess.run("clear")
    print(Style.BRIGHT + Fore.WHITE + text + Style.RESET_ALL)

def Ask(text , clear: bool = True):
    if clear:
        subprocess.run("clear")

    user_input = input(Style.BRIGHT + Fore.WHITE + text + Style.RESET_ALL)

    return user_input

Message("Resolving running path...")

path = pathlib.Path(__file__).resolve().parent

headless = Ask(Style.BRIGHT + Fore.WHITE + "Do you wish to run browser in headless mode?(y/n): " + Style.RESET_ALL).lower()

while headless not in ["y" , "n"]:
    headless = Ask(Style.BRIGHT + Fore.WHITE + "Do you wish to run browser in headless mode?(y/n): " + Style.RESET_ALL).lower()

subreddit = Ask(Style.BRIGHT + Fore.WHITE + "Choose subreddit for scrape: " + Style.RESET_ALL)

while True:
    try:
        page_amount = int(Ask(Style.BRIGHT + Fore.WHITE + "Please select amount of pages to scrape: " + Style.RESET_ALL))
        break
    except ValueError:
        print(f"{Style.BRIGHT + Fore.WHITE}Input {Fore.RED}must{Fore.WHITE} be a number!")

Message("Preparing options for browser...")

options =  Options()

if headless == "y":
    options.add_argument(f"--headless")

Message("Initializing browser...")

browser = webdriver.Firefox(options=options)
try:
    browser.get(f'https://old.reddit.com/r/{subreddit}')
except Exception as error:
    Message(Fore.RED + f"Error while going on reddit: {Fore.WHITE}{str(error)}")

pagesScraped = 0

output = []

subprocess.run("clear")

while pagesScraped < page_amount:
    posts = browser.find_elements(By.XPATH , "//div[contains (@class , 'thing') and contains (@class , self) and contains (@class , link) and not (contains (@class , 'promoted'))]")
    
    if len(posts) >= 1:
        for post in posts:
            title = post.find_element(By.XPATH , ".//div[@class='top-matter']//p[@class='title']//a[contains (@class , 'title') and contains (@class , may-blank)]").text
            score = post.find_element(By.XPATH , ".//div[contains (@class , 'score') and contains(@class , 'unvoted')]").text
            author = post.get_attribute("data-author")
            url = post.get_attribute("data-url")

            try:
                date = datetime.datetime.fromtimestamp(int(post.get_attribute("data-timestamp")) / 1000).strftime("%D @ %H:%M")
            except ValueError:
                date = "Unknown"

            try:
                score = int(score)
            except ValueError:
                score = 0

            output.append([author , score , date , title , url])
            
            Message("Scraping...")

        pagesScraped += 1
        
        sleeping_time = uniform(1 , 5)
        print(f"{Style.BRIGHT + Fore.BLUE}Sleeping {Fore.WHITE}{round(sleeping_time , 2)}s...")
        sleep(sleeping_time)
    else:
        Message("Empty page, Finishing scraping...")
        break
    
    if pagesScraped != page_amount:
        try:
            browser.find_element(By.XPATH , "//span[@class='next-button']//a").click()
        except Exception:
            print(f"{Style.BRIGHT + Fore.RED}Couldn't locate 'next' button...\n{Fore.WHITE}Finishing scraping...{Style.RESET_ALL}")

browser.quit()

with open(f"{path}/results.csv" , "w") as file:
    writer = csv.writer(file)
    for author , score , date , title , url in output:
        writer.writerow([f"By {author} " , f" Score: {score} " , f" {date} " f" {title} " , f" {url} "])

Message(f"{Fore.GREEN}Done!{Fore.WHITE} Results at 'results.csv'.")

