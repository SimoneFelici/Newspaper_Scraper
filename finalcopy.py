import re
import easygui
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def generate_summary(text, summary_length=100):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    input_ids = tokenizer.encode(text, return_tensors="pt")
    max_length = len(input_ids[0]) + summary_length
    output = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return summary

def scrape_and_display(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all('p')

        print('-------------------')
        text = ''
        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            if paragraph_text:
                formatted_text = re.sub(r'\.(\s|$)', '.\n', paragraph_text)
                text += formatted_text + '\n'

        print(text)

        # Prompt the user to generate a summary
        generate_summary_prompt = input("Would you like to generate a summary? (y/n): ")
        if generate_summary_prompt.lower() == "y":
            summary = generate_summary(text, summary_length=150)
            print("Summary:")
            print(summary)

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

def extract_urls_from_site(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all('a', href=True)
        urls = [link['href'] for link in links if link['href'].startswith('http')]

        return urls
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return []

site_urls = ["https://nascecresceignora.it/", "https://www.everyeye.it/"]
site_names = [urlparse(url).hostname.replace("www.", "").split(".")[0] for url in site_urls]

site_names.append("Enter custom URL...")  # Add option to enter a custom URL

selected_site = easygui.choicebox("Select the website to scrape:", "Website Selection", choices=site_names)

if selected_site == "Enter custom URL...":
    site_url = easygui.enterbox("Try your luck!:")
    if not site_url:
        easygui.msgbox("No website URL entered. Exiting...", "Error")
        exit()
    parsed_url = urlparse(site_url)
    site_name = parsed_url.netloc.replace("www.", "").split(".")[0]
    easygui.msgbox(f"You have entered the website: {site_name}", "Website Selection")
else:
    site_url = site_urls[site_names.index(selected_site)]
    site_name = selected_site
    easygui.msgbox(f"You have selected the website: {site_name}", "Website Selection")

urls = extract_urls_from_site(site_url)

titles = {re.sub(r'\W+', ' ', url): url for url in urls}

selected_title = easygui.choicebox("Select a news title:", "News Titles", choices=list(titles.keys()))

if selected_title:
    selected_link = titles[selected_title]
    scrape_and_display(selected_link)
