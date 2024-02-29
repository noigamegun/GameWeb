# Tested On My Mac. Not GitHub Actions.
# Need to fix the code to work with GitHub Actions.

import requests
import os
from bs4 import BeautifulSoup

html_files = []

# Specify the path to your repository
repo_path = '/Users/game/github/GameWeb'

# Traverse through all directories and files in the repository
for root, dirs, files in os.walk(repo_path):
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('.html'):
            # Add the file path to the list
            html_files.append(os.path.join(root, file))

# Print the list of HTML files for debugging
print(html_files)
print("\n")

# Iterate through each HTML file
for file_path in html_files:
    # Open the HTML file
    with open(file_path, 'r') as file:
        # Read the contents of the file
        html_content = file.read()
    # Remove Local Path
    true_path = os.path.relpath(os.path.dirname(file_path), start="/Users/game/github/GameWeb") + "/"
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all anchor tags AKA href lines
    anchor_tags = soup.find_all('a')

    # Iterate through each anchor tag
    for anchor_tag in anchor_tags:
        # Get the href attribute value AKA the link
        href = anchor_tag.get('href')
        # Check if the href attribute exists and is not empty
        if href is not None and href != '':
            # Check if the link is a "#"
            if href == '#':
                print(f"Link in file {file_path} Leads to nothing. Skipping...")
            # If the link is not a "#"
            else:
                # Check if the link is an external link
                if href.startswith('http://') or href.startswith('https://'):
                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if response.status_code == 404:
                        print(f"Link {href} in file {file_path} is broken.")
                    else:
                        print(f"Link {href} in file {file_path} is working.")

                # Check if the link is an email link
                elif href.startswith('mailto:'):
                    print(f"Link in file {file_path} Leads to mailto. Skipping...")

                # If the link is not an external link or an email link and it a local file in the repository
                else:
                    href = "https://thapat.me/" + true_path + href

                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if response.status_code == 404:
                        print(f"Link {href} in file {file_path} is broken.")
                    else:
                        print(f"Link {href} in file {file_path} is working.")
