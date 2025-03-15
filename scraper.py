import requests
from bs4 import BeautifulSoup
import re

# Function to remove emojis
def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Removes non-ASCII characters (including emojis)

# Base URL
base_url = "https://brainlox.com"

# Main category page
url = "https://brainlox.com/courses/category/technical"
headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser

# Get main page HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

courses = []

# Extract course cards
for course_card in soup.find_all("div", class_="single-courses-box"):
    try:
        # Extract course title
        title_tag = course_card.find("h3")
        title = remove_emojis(title_tag.text.strip()) if title_tag else "No title available"

        # Extract short description
        description_tag = course_card.find("p")
        description = remove_emojis(description_tag.text.strip()) if description_tag else "No description available"

        # Extract price
        price_tag = course_card.find("span", class_="price-per-session")
        price = remove_emojis(price_tag.text.strip()) if price_tag else "Price not available"

        # Extract course link
        link_tag = course_card.find("a", class_="BookDemo-btn")  # This is the 'View Details' button
        course_link = base_url + link_tag["href"] if link_tag else "Link not available"

        # Initialize course details
        course_details = {
            "title": title,
            "price_per_session": price,
            "number_of_lessons": "Not available",
            "duration": "Not available",
            "total_price": "Not available",
            "detailed_description": "Not available",
            "course_link":course_link
        }

        # Visit the course page for more details
        if course_link != "Link not available":
            course_response = requests.get(course_link, headers=headers)
            if course_response.status_code == 200:
                course_soup = BeautifulSoup(course_response.text, "html.parser")

                # Extract detailed description
                overview_div = course_soup.find("div", class_="courses-overview")
                if overview_div:
                    detailed_description_tag = overview_div.find("p")
                    course_details["detailed_description"] = (
                        remove_emojis(detailed_description_tag.text.strip()) if detailed_description_tag else "No detailed description available"
                    )

                # Extract course details (price, lessons, duration)
                info_list = course_soup.find("ul", class_="info")
                if info_list:
                    for li in info_list.find_all("li"):
                        text = remove_emojis(li.text.strip())

                        if "Lessons" in text:
                            course_details["number_of_lessons"] = text.split()[-1]
                        elif "Duration" in text:
                            course_details["duration"] = " ".join(text.split()[1:])
                        elif "Price" in text:
                            course_details["total_price"] = text.split()[-1]

        # Append course details to list
        courses.append(course_details)

    except Exception as e:
        print(f"Error processing a course: {e}")

import json

with open("courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=4)
