import re
import easygui
from bs4 import BeautifulSoup
import requests

def on_click(title):
    selected_link = titles[title]
    scrape_and_display(selected_link)

def scrape_and_display(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all('p')

        print('-------------------')
        for paragraph in paragraphs:
            text = paragraph.text.strip()
            if text:
                formatted_text = re.sub(r'\.(\s|$)', '.\n', text)
                print(formatted_text)

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

def extract_urls_from_site(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all('a', href=True)
        urls = [link['href'] for link in links]
       
        return urls
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return []

site_url = input("Enter the URL of the website to scrape: ")

urls = extract_urls_from_site(site_url)

titles = {}
for url in urls:
    title = re.sub(r'\W+', ' ', url)  
    titles[title] = url

title_list = list(titles.keys())

selected_title = easygui.choicebox("Select a news title:", "News Titles", title_list)

if selected_title:
    selected_link = titles[selected_title]
    scrape_and_display(selected_link)
