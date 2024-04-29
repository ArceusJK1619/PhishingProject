import pickle 
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
with open('LogisticModel.pkl', 'rb') as model_file:#logistic reggression model
    log_reg_model = pickle.load(model_file)
def url_length(url):
    a = len(url)
    return a
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain
def domain_length(domain):
    a = len(domain)
    return a 
def is_https(url):
    if url[0:5]=="https":
        return 1
    else:
        return 0
def count_letters_in_url(url):
    url_lower = url.lower()
    num_letters = sum(c.isalpha() for c in url_lower)
    return num_letters
def count_digits_in_url(url):
    num_digits = sum(c.isdigit() for c in url)
    return num_digits
def count_equals_in_url(url):
    num_equals = url.count("=")  
    return num_equals
def count_QMarks_in_url(url):
    num_qmark = url.count("?")
    return num_qmark
def count_ampersand_in_url(url):
    num_ampersand = url.count("&")
    return num_ampersand
def count_specialCharachters_in_url(url):
    special_characters = "!@#$%^&*()-_+=[]{}|;:,.<>?/~"
    num_special_chars = sum(1 for char in url if char in special_characters)   
    return num_special_chars
def count_css_files_in_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        css_links = soup.find_all('link', rel='stylesheet')
        num_css_files = len(css_links)
        return num_css_files
    except Exception as e:
        print(f"Error fetching or parsing HTML content: {e}")
        return None
def count_js_files_in_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tags = soup.find_all('script')
        external_js_files = [tag['src'] for tag in script_tags if 'src' in tag.attrs]
        num_js_files = len(external_js_files)
        return num_js_files
    except Exception as e:
        print(f"Error fetching or parsing HTML content: {e}")
        return None
def count_self_referencing_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        anchor_tags = soup.find_all('a', href=True)
        num_self_refs = sum(1 for tag in anchor_tags if urlparse(tag['href']).netloc == '' or urlparse(tag['href']).netloc == urlparse(url).netloc)
        
        return num_self_refs
    except Exception as e:
        print(f"Error fetching or parsing HTML content: {e}")
        return None
def count_external_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        anchor_tags = soup.find_all('a', href=True)
        num_external_links = sum(1 for tag in anchor_tags if urlparse(tag['href']).netloc != base_url)
        return num_external_links
    except Exception as e:
        print(f"Error fetching or parsing HTML content: {e}")
        return None
def count_empty_references(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        empty_ref_tags = soup.find_all('a', href=False)
        num_empty_refs = len(empty_ref_tags)
        return num_empty_refs
    except Exception as e:
        print(f"Error fetching or parsing HTML content: {e}")
        return None
    
def get_params(url):
    url_len = url_length(url)
    domain = extract_domain(url)
    domain_len = domain_length(domain)
    ishttps= is_https(url)
    count_letters = count_letters_in_url(url)
    count_digits= count_digits_in_url(url)
    count_equals= count_equals_in_url(url)
    count_qmarks = count_QMarks_in_url(url)
    count_ands = count_ampersand_in_url(url)
    count_specialChar = count_specialCharachters_in_url(url)
    count_css = count_css_files_in_url(url)
    count_js  = count_js_files_in_url(url)
    count_selfref  = count_self_referencing_links(url)
    count_externalref = count_external_links(url)
    count_emptyref= count_empty_references(url)

    inputs = [[url_len,domain_len,count_letters,count_digits,count_equals,count_qmarks,count_ands,count_specialChar,ishttps,count_css,count_js,count_selfref,count_emptyref,count_externalref]]
    return inputs

def predict(url):
    inputs = get_params(url)
    color = None
    image = "default.jpg"
    try:
        predict = log_reg_model.predict(inputs)
        if predict == [1]:
            prediction = "Doesnt Look good 💀💀💀"
            color = "Red"
            image = "trap.jpg"
        if predict == [0]:
            prediction = "Looks safe 👍👍👍"
            color = "Green"
            image = "images.jpg"
    except Exception as e:
        prediction = f"Scince error: \n{e} \n we think the site is not safe 🚫🚫🚫"
        color = "Red"
        image= "trap.jpg"
    
    print(prediction , color , image)
    return prediction , color , image