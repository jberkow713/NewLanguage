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

def get_nccdphp_urls(start_url):
    """
    Scrapes the CDC website starting from start_url, traverses clickable links,
    and returns a unique list of URLs containing '/nccdphp/' in their path.
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

            if '/nccdphp/' in current_url:
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
                        if '/nccdphp/' in parsed_url.path:
                            nccdphp_urls.add(absolute_url)
                        
                        # Add to queue for further exploration if not already visited
                        if absolute_url not in visited_urls:
                            queue.append(absolute_url)

    return sorted(list(nccdphp_urls))

def store_all_nccdphp_site():

    start_link = "https://www.cdc.gov/nccdphp/index.html"
    nccdphp_sites = get_nccdphp_urls(start_link)
    with open('nccdphp.json', 'w') as f:
        json.dump(nccdphp_sites , f, indent=4)
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
                tag.decompose() # Remove the tag and its contents

        for tag_name in boilerplate_tags:
            for tag in soup.find_all(tag_name):
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


with open('nccdphp.json', 'r') as file:
    data = json.load(file)


def find_text_per_page():
    with open('nccdphp.json', 'r') as file:
        data = json.load(file)
    
    info = {}
    Text = []
    for link in data:
        text = get_human_readable_scrolling_text(link)
        if text not in Text:
            print(f'adding text from {link}')
            Text.append(text)
            info[link]=text
    with open('nccdphp_Text.json', 'w') as f:
        json.dump(info , f, indent=4)        
    return info 


# find_text_per_page()

with open('nccdphp_Text.json', 'r') as f:
    data = json.load(f)

print(data)
for k,v in data.items():
    print(f'text for {k} is {v}')


find_and_download_pdfs('https://www.cdc.gov/healthy-schools/parents/index.html')


    










    







# # print(data[0])
# # for page in data[0]:
# print(data[30])
# print(get_human_readable_scrolling_text(data[30]))
# # print(data[8])
# # print(get_human_readable_scrolling_text(data[8]))
# # # print(data[0:10])