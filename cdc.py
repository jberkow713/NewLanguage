import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse
import json
import re 
from collections import defaultdict

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
    return info 

       
print(find_text_per_page())









    







# # print(data[0])
# # for page in data[0]:
# print(data[30])
# print(get_human_readable_scrolling_text(data[30]))
# # print(data[8])
# # print(get_human_readable_scrolling_text(data[8]))
# # # print(data[0:10])