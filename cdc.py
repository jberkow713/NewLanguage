import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse
import json
import re 
from collections import defaultdict
from fpdf import FPDF
import os
import sys
import html2text
import asyncio
from playwright.async_api import async_playwright

def find_and_download_pdfs(url, output_dir="downloaded_pdfs"):
    """
    Finds PDF links on a given URL, then downloads and saves them.

    Args:
        url (str): The URL of the webpage to scan for PDF links.
        output_dir (str): The directory where downloaded PDFs will be saved.
                          Defaults to "downloaded_pdfs".
    """
    print(f"Scanning URL: {url}")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    try:
        # Add a User-Agent header to mimic a browser and avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    found_pdfs = 0

    # Find all anchor tags (<a>)
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(url, href) # Resolve relative URLs to absolute URLs

        # Check if the link points to a PDF file
        # Check both the path extension and the content-type if available (though not always reliable before download)
        if absolute_url.lower().endswith('.pdf'):
            parsed_url = urlparse(absolute_url)
            filename = os.path.basename(parsed_url.path)

            # Sanitize filename to remove potentially invalid characters for file paths
            filename = "".join([c for c in filename if c.isalnum() or c in ('.', '_', '-')]).strip()
            if not filename: # If filename becomes empty after sanitization
                filename = "downloaded_pdf_" + str(found_pdfs + 1) + ".pdf"

            file_path = os.path.join(output_dir, filename)

            # Check if the file already exists to avoid re-downloading
            if os.path.exists(file_path):
                print(f"Skipping existing file: {filename}")
                continue

            print(f"Found PDF link: {absolute_url}")
            print(f"Downloading {filename}...")

            try:
                # Download the PDF file
                # Use stream=True for potentially large files and iterate over content
                pdf_response = requests.get(absolute_url, stream=True, headers=headers, timeout=20)
                pdf_response.raise_for_status()

                # Check Content-Type header to be more robust for PDFs
                if 'content-type' in pdf_response.headers and 'application/pdf' not in pdf_response.headers['content-type']:
                    print(f"Warning: {absolute_url} does not have 'application/pdf' content type. Skipping.")
                    continue

                with open(file_path, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {filename}")
                found_pdfs += 1

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {absolute_url}: {e}")
            except IOError as e:
                print(f"Error saving file {file_path}: {e}")

    if found_pdfs == 0:
        print("No PDF links found on the page.")
    else:
        print(f"\nFinished. Downloaded {found_pdfs} PDF(s) to '{output_dir}'.")

def get_urls(start_url,Filter):
    """
    Scrapes the CDC website starting from start_url, traverses clickable links,
    and returns a unique list of URLs containing the filter variable such as '/nccdphp/' in their path.

    """
    base_domain = urlparse(start_url).netloc
    visited_urls = set()
    nccdphp_urls = set()
    queue = deque([start_url])

    while queue:
        current_url = queue.popleft()

        if current_url in visited_urls:
            continue
        else:

            if Filter in current_url:
                visited_urls.add(current_url)
                print(f"Visiting: {current_url}")

                try:
                    response = requests.get(current_url, timeout=5)
                    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                except requests.exceptions.RequestException as e:
                    print(f"Error accessing {current_url}: {e}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all anchor tags (links)
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(current_url, href)
                    parsed_url = urlparse(absolute_url)

                    # Ensure we stay within the cdc.gov domain and avoid external links
                    if parsed_url.netloc == base_domain:
                        # Check if '/nccdphp/' is in the path of the URL
                        if Filter in parsed_url.path:
                            nccdphp_urls.add(absolute_url)
                        
                        # Add to queue for further exploration if not already visited
                        if absolute_url not in visited_urls:
                            queue.append(absolute_url)

    return sorted(list(nccdphp_urls))

def store_all_nccdphp_site():
    '''
    Stores all 'nccdphp' urls
    '''
    start_link = "https://www.cdc.gov/nccdphp/index.html"
    nccdphp_sites = get_urls(start_link,'/nccdphp/')
    with open('nccdphp.json', 'w') as f:
        json.dump(nccdphp_sites , f, indent=4)
    return     

def store_generic_links(start_link,Filter,name):
    sites = get_urls(start_link,Filter)
    with open(name, 'w') as f:
        json.dump(sites , f, indent=4)
    return 

def get_human_readable_scrolling_text(url):
    """
    Fetches the HTML content from a given URL, parses it using BeautifulSoup,
    and attempts to return all human-readable text that a user would find
    when scrolling down the page, excluding common boilerplate elements.

    Args:
        url (str): The URL of the web page to retrieve text from.

    Returns:
        str: A single string containing the consolidated, cleaned, human-readable text.
             Returns an empty string if there's an error fetching or parsing the page,
             or no relevant text is found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Strategy 1: Remove known boilerplate tags ---
        # List of tags that often contain non-content boilerplate.
        # This list can be expanded or refined based on typical website structures.
        boilerplate_tags = [
            'nav', 'header', 'footer', 'aside', 'form', 'style', 'script',
            'iframe', 'img', 'link', 'meta', 'svg', 'noscript', 'input',
            # Common classes/ids for ads or non-content if found
            # You might need to inspect specific websites for these
            # 'div', 'span', etc. if they have specific classes like 'ad-container'
        ]
        
        # Remove elements with common boilerplate roles/classes
        # (This is a heuristic and might need tuning per site)
        for selector in [
            '.header', '.footer', '.nav', '.sidebar', '.ad', '.ads',
            '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]',
            '[role="complementary"]', # for aside
            '[aria-hidden="true"]' # often used for decorative elements
        ]:
            for tag in soup.select(selector):
                # getting rid of unusable stuff
                tag.decompose() # Remove the tag and its contents

        for tag_name in boilerplate_tags:
            for tag in soup.find_all(tag_name):
                # getting rid of more unusable tags and information
                tag.decompose() # Remove the tag and its contents

        # --- Strategy 2: Focus on common content-bearing tags ---
        # These are tags typically used for main readable content.
        content_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'blockquote']

        all_readable_texts = []
        for tag in soup.find_all(content_tags):
            # Get text, separating content from nested tags with a space
            raw_text = tag.get_text(separator=' ', strip=True)
            
            # Clean up: replace multiple whitespaces with single space, strip overall
            cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
            
            if cleaned_text:
                all_readable_texts.append(cleaned_text)

        # Join all collected texts into a single string, separated by two newlines
        # for better readability, mimicking paragraphs.
        final_text = "\n\n".join(all_readable_texts)
        return final_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL '{url}': {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while processing '{url}': {e}")
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL '{url}': {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while processing '{url}': {e}")
        return {}

def find_text_per_page_generic(file_name):
        '''
    Finds all non-repeating text and stores {URL:Text} for 'nccdphp' sites
    '''
    with open(file_name, 'r') as file:
        # Loading in links
        data = json.load(file)
    
    info = {}
    Text = []
    for link in data:
        # Creates dictionary key with only the first links on the page,
        # As other links share readable text
        text = get_human_readable_scrolling_text(link)
        if text not in Text:
            print(f'adding text from {link}')
            Text.append(text)
            info[link]=text
         
    return [x for x in info.keys()]

def find_text_per_page():
    '''
    Finds all non-repeating text and stores {URL:Text} for 'nccdphp' sites
    '''
    with open('nccdphp.json', 'r') as file:
        # Loading in links
        data = json.load(file)
    
    info = {}
    Text = []
    for link in data:
        # Creates dictionary key with only the first links on the page,
        # As other links share readable text
        text = get_human_readable_scrolling_text(link)
        if text not in Text:
            print(f'adding text from {link}')
            Text.append(text)
            info[link]=text
    # Stores dictionary in json, can also add parameter to do this if needed for reusability for
    # other links/ files 
    with open('nccdphp_Text.json', 'w') as f:
        json.dump(info , f, indent=4)        
    return info 

def save_to_file(Folder, name,text):

    # Saves file to folder
    filename = f"{Folder}{name}.txt"
    print(filename)

    try:
        # Open the file in write mode ('w')
        # 'w' will create the file if it doesn't exist, or overwrite it if it does.
        # 'a' (append mode) would add to the end of an existing file.
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {filename}")

    except IOError as e:
        print(f"Error saving file: {e}")
    return 


def fetch_initial_html(url):
    """
    Fetches the raw HTML content from a given URL.
    This is a helper function for the Playwright part.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15) # Increased timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching initial HTML from {url}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while fetching HTML: {e}")

async def scrape_and_save_pdf(Folder,url,split_val):
    """
    Navigates to the URL using a headless browser, executes JavaScript
    to remove non-human-readable elements, and then saves the rendered
    page as a PDF file. Saves the file based on the split_val given to it, stores PDF in folder

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: The path to the generated PDF file, or raises an exception on error.
    """
    
    if not os.path.exists(Folder):
        os.makedirs(Folder)

    output_filename = ""
    try:
        sanitized_url = url.split(split_val)[1].split('.html')[0]
        output_filename = os.path.join(Folder, f"{sanitized_url}.pdf")
        print(output_filename)

        async with async_playwright() as p:
            browser = await p.chromium.launch() # Launch a Chromium browser
            page = await browser.new_page()

            # Navigate to the URL and wait for the page to be fully loaded
            try:
                await page.goto(url, wait_until="load", timeout=60000) # Increased timeout to 60 seconds
            except Exception as goto_error:
                # If 'load' fails, try 'domcontentloaded' as a fallback, with a longer timeout
                print(f"Initial page.goto failed with wait_until='load': {goto_error}. Retrying with 'domcontentloaded'...")
                await page.goto(url, wait_until="domcontentloaded", timeout=90000)

            # Execute JavaScript in the browser context to remove unwanted elements.
            # This ensures that original CSS and images are loaded, but then
            # non-content elements are removed before printing.
            await page.evaluate('''
                () => {
                    const selectorsToRemove = [
                        'script', 'style', 'noscript', 'meta', 'link[rel="stylesheet"]', 'form',
                        'nav', 'footer', 'header', 'aside', '.sidebar',
                        '[class*="ad"]', '[id*="ad"]', '[aria-hidden="true"]',
                        'iframe', '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]'
                    ];
                    selectorsToRemove.forEach(selector => {
                        document.querySelectorAll(selector).forEach(element => {
                            // Only remove elements if they are not direct children of <body> and don't contain main content
                            // This heuristic tries to avoid removing essential layout if a site uses semantic tags broadly
                            if (element.tagName !== 'BODY' && !element.contains(document.querySelector('article')) && !element.contains(document.querySelector('main'))) {
                                element.remove();
                            }
                        });
                    });

                    // Remove elements that are hidden or have zero dimensions (e.g., tracking pixels, empty divs)
                    document.querySelectorAll('*').forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.display === 'none' || style.visibility === 'hidden' || el.offsetWidth === 0 || el.offsetHeight === 0) {
                            el.remove();
                        }
                    });

                    // Optional: Remove empty paragraphs, divs etc.
                    document.querySelectorAll('p, div, span').forEach(el => {
                        if (el.textContent.trim() === '' && el.children.length === 0) {
                            el.remove();
                        }
                    });
                }
            ''')

            # Save the page as PDF
            await page.pdf(path=output_filename, format="A4", print_background=True)
            print(f"PDF successfully saved to {output_filename}")
            return output_filename

    except Exception as e:
        # Clean up any partially created file if an error occurred during PDF generation
        if os.path.exists(output_filename):
            os.remove(output_filename)
        raise Exception(f"Error during PDF generation for {url}: {e}")

class Scraper:
    '''
    class takes in keyword to search for in websites, starting website, a Filter to use for 
    file_name creation, a json_file to store links in, and a pdf_folder to save pdfs for non-replicated
    links to. 
              keyword example input: '/nccdphp/'
              starting_site example input: "https://www.cdc.gov/nccdphp/index.html"
              Filter example input: 'https://www.cdc.gov/nccdphp/'
              json_file example input: 'nccdphp.json'
              pdf_folder example input: 'generated_pdfs'
    '''
    def __init__(self, keyword, starting_site,Filter,json_file,pdf_folder):
        self.keyword = keyword 
        self.starting_site=starting_site
        self.Filter = Filter 
        self.json_file = json_file
        self.pdf_folder = pdf_folder
        self.links = None
        self.failed = []
        self.worked = [] 
    def find_usable_links(self):
        '''
        Returns a list of unique links to then be scraped for PDFS
        Gets all initial sites, then narrows them down based on finding unique text, and stores
        the outcome in self.links
        '''
        store_generic_links(self.starting_site,self.keyword,self.json_file)
        self.links = find_text_per_page_generic(self.json_file)
        return
    def create_pdfs(self):
        '''
        Creates PDFS for all usable non repetitive links using specified storage folder
        '''
        for link in self.links:
            try:
                asyncio.run(scrape_and_save_pdf(self.pdf_folder,link,self.Filter))
                self.worked.append(link)
            except Exception as e:
                print(f'{link} failed to generate PDF')
                self.failed.append(link)
                continue

'''
# TODO
# Better naming convention for PDF
'''

'''
# This block is for demonstrating how to use the scraper as for nccdphp files, where links were stored
# in 'nccdphp_Text.json'
if __name__ == '__main__':
    with open('nccdphp_Text.json', 'r') as file:
        # Loading in links
        data = json.load(file)
    for link in data.keys():
        try:
            pdf_path = asyncio.run(scrape_and_save_pdf("generated_pdfs",link,'https://www.cdc.gov/nccdphp/'))
            print(f"PDF saved to: {pdf_path}")
        except Exception as e:
            print(f'{link} failed to generate PDF')
            continue
'''
    