# Reddit Scraper  

A Python Selenium scraper for old Reddit. Prompts for subreddit, page count, and headless mode, then collects post author, score, date, title, and URL, saving results to a CSV file. Includes random delays to reduce detection.  

## Features  
- Scrapes posts from any subreddit  
- Supports multiple pages  
- Option to run browser in headless mode  
- Saves results to `results.csv`  
- Handles missing data gracefully  

## Requirements  
- Python 3.8+  
- Selenium  
- Firefox + Geckodriver  
- Colorama  

## Installation  
1. Clone the repo  
2. Install dependencies:  
   pip install selenium colorama  
3. Ensure Firefox and Geckodriver are installed and in PATH  

## Usage  
1. Run the script:  
   python reddit_scraper.py  
2. Enter the subreddit, number of pages, and whether to use headless mode  
3. Wait for scraping to complete  
4. Results will be saved in `results.csv`  

## Notes  
- Avoid scraping too many pages too fast to prevent rate-limiting  
- Designed for learning and personal use, respect Reddit's terms  

## License  
MIT License  
