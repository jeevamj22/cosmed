import requests
from bs4 import BeautifulSoup

def extract_ingredient_structure_from_url(url):
    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        # Fetch the HTML content from the URL with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with id 'important-information' which contains the Ingredients section
        important_info_div = soup.find('div', id='important-information')

        if important_info_div:
            # Find the <h4> element containing "Ingredients:"
            ingredients_heading = important_info_div.find('h4', text='Ingredients:')
            
            if ingredients_heading:
                # Get the next <p> element containing the ingredients
                ingredients_paragraph = ingredients_heading.find_next_sibling('p')
                
                if ingredients_paragraph:
                    return ingredients_paragraph.get_text(strip=True)  # Return the text of the paragraph
                else:
                    return None  # Ingredients paragraph not found
            else:
                return None  # Ingredients heading not found
        else:
            return None  # Div with id 'important-information' not found
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None

# URL
url = "https://www.amazon.in/Garnier-Bright-Complete-VITAMIN-Facewash/dp/B094RQ7BQ8/ref=sxin_15_pa_sp_search_thematic?content-id=amzn1.sym.37bad8da-0499-4510-838e-af217f0a67c4%3Aamzn1.sym.37bad8da-0499-4510-838e-af217f0a67c4&cv_ct_cx=face%2Bwash&keywords=face%2Bwash&pd_rd_i=B094RQ7BQ8&pd_rd_r=87d76841-f26a-4edb-8142-33d312224585&pd_rd_w=cdoRI&pd_rd_wg=9Z7gR&pf_rd_p=37bad8da-0499-4510-838e-af217f0a67c4&pf_rd_r=8KNMNMD7EJPZ0JB65YDB&qid=1708277688&s=beauty&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-4-ced4eeeb-b190-41d6-902a-1ecb3fb8b7c4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&th=1"

ingredient_structure = extract_ingredient_structure_from_url(url)
if ingredient_structure:
    print(ingredient_structure)
else:
    print("Ingredients section not found or failed to fetch the webpage.")
