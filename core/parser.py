from bs4 import BeautifulSoup

def parse_redfin_property(html_content: str):
    '''
    Extract property listings from a Redfin search results page.
    '''

    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.select("div.HomeCardContainer") # Get all the cards with the property details

    properties = []

    for card in cards:
            # Price
            price_element = card.select_one("span.bp-Homecard__Price--value")
            price = price_element.get_text(strip=True) if price_element else "N/A"
            
            # Address
            address_div = card.select_one("div.bp-Homecard__Address--address")
            address = address_div.get_text(strip=True).replace("|", "").strip() if address_div else "N/A"

            # Beds
            beds_element = card.select_one("span.bp-Homecard__Stats--beds")
            beds = beds_element.get_text(strip=True) if beds_element else "N/A"

            # Baths
            baths_element = card.select_one("span.bp-Homecard__Stats--baths")
            baths = baths_element.get_text(strip=True) if baths_element else "N/A"

            # Sqft
            sqft_element = card.select_one("span.bp-Homecard__Stats--sqft .bp-Homecard__LockedStat--value")
            sqft = sqft_element.get_text(strip=True) if sqft_element else "N/A"

            # Only add the property if we found an address
            if address != "N/A":
                property_info = {
                    "address": address,
                    "price": price,
                    "beds": beds,
                    "baths": baths,
                    "sqft": sqft,
                }
                properties.append(property_info)

    
    return properties