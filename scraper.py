import requests
from bs4 import BeautifulSoup
import re

# The base URL of the website
BASE_URL = 'https://cetatenie.just.ro/ordine-articolul-1-1/'

# Function to get the webpage content
def get_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None

# Function to parse and extract all PDF links and categorize them
def extract_pdf_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all links with 'href' containing '.pdf'
    pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$'))
    
    # Dictionary to hold the PDFs categorized by year
    pdf_files = {}
    
    for link in pdf_links:
        pdf_url = link['href']
        
        # Try to infer the year from the URL or the link text
        text = link.get_text()
        match = re.search(r'(\d{4})', text)
        if match:
            year = match.group(1)
        else:
            # Default to unknown year if no year is found
            year = "Unknown"
        
        # Try to find the order number (e.g., 15661) from the link text
        number_match = re.search(r'\b(\d+)\b', text)
        if number_match:
            order_number = number_match.group(1)
        else:
            # Default to unknown number if no number is found
            order_number = "Unknown"
        
        # Add the PDF link to the dictionary
        if year not in pdf_files:
            pdf_files[year] = {}
        pdf_files[year][order_number] = pdf_url
    
    return pdf_files

# Main execution
if __name__ == "__main__":
    # Fetch the webpage
    html_content = get_webpage(BASE_URL)
    
    if html_content:
        # Extract and categorize PDF links
        pdf_data = extract_pdf_links(html_content)
        
        # Print the extracted data in the desired format
        print(pdf_data)
