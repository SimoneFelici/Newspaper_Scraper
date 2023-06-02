import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from transformers import BartTokenizer, BartForConditionalGeneration
from consolemenu import SelectionMenu

def generate_summary(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    inputs = tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=1024)
    summary_ids = model.generate(inputs, num_beams=4, max_length=150, early_stopping=True)

    summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    return summary

def scrape_and_display(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all('p')

        text = ''
        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(strip=True)
            if paragraph_text:
                formatted_text = re.sub(r'\.(\s|$)', '.\n', paragraph_text)
                text += formatted_text + '\n'

        # Display the scraped text
        print('-------------------')
        print(text)

        # Prompt the user to generate a summary
        generate_summary_prompt = input("Would you like to generate a summary? (y/n): ")
        if generate_summary_prompt.lower() == "y":
            summary = generate_summary(text)
            print("Summary:")
            print(summary)

            # Prompt the user to choose an action
            action = input("Press 'r' to return to the article selection or 'Enter' to exit: ")
            if action.lower() == "r":
                return False  
            elif action.lower() == "":
                exit()

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

    return True  # Continue with the program

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

while True:
    # Create the website selection menu
    website_menu = SelectionMenu(site_names, "Select the website to scrape:")
    website_menu.show()
    selected_site_option = website_menu.selected_option  
    
    if selected_site_option == len(site_names) - 1:  # Last option is "Enter custom URL..."
        site_url = input("Enter the website URL: ")
        if not site_url:
            print("No website URL entered. Exiting...")
            exit()
        parsed_url = urlparse(site_url)
        site_name = parsed_url.netloc.replace("www.", "").split(".")[0]
        print(f"You have entered the website: {site_name}")
    else:
        if selected_site_option < len(site_urls):
            site_url = site_urls[selected_site_option]
            site_name = site_names[selected_site_option]
            print(f"You have selected the website: {site_name}")
        else:
            print("Exiting...")
            exit()
    urls = extract_urls_from_site(site_url)

    titles = {re.sub(r'\W+', ' ', url): url for url in urls}

    return_to_selection = False

    while True:
        # Create the news title selection menu
        if site_url == "https://nascecresceignora.it/":
            menu_options = list(titles.keys())[14:-1]
        elif site_url == "https://www.everyeye.it/":
            menu_options = list(titles.keys())[27:-12]
        else:
            menu_options = list(titles.keys())

        title_menu = SelectionMenu(menu_options, "Select a news title:")
        title_menu.show()
        selected_title_option = title_menu.selected_option

        print("Selected title option:", selected_title_option)

        if selected_title_option == len(menu_options):
            print("Returning to the website selection...")
            break

        if selected_title_option >= 0 and selected_title_option < len(menu_options):
            selected_title = menu_options[selected_title_option]
            if scrape_and_display(titles[selected_title]):
                return_to_selection = True
        else:
            print("Invalid selection. Returning to the article selection.")

# The code will continue running if `return_to_selection` is False