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

# Print the list of HTML files
print(html_files)

# Iterate through each HTML file
for file_path in html_files:
    # Open the HTML file
    with open(file_path, 'r') as file:
        # Read the contents of the file
        html_content = file.read()
    true_path = os.path.relpath(os.path.dirname(file_path), start="/Users/game/github/GameWeb") + "/"
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all anchor tags
    anchor_tags = soup.find_all('a')

    # Iterate through each anchor tag
    for anchor_tag in anchor_tags:
        # Get the href attribute value
        href = anchor_tag.get('href')

        if href is not None and href != '':
            if href == '#':

                print(f"Link in file {file_path} Leads to nothing. Skipping...")

            else:

                if href.startswith('http://') or href.startswith('https://'):
                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if response.status_code == 404:
                        print(f"Link {href} in file {file_path} is broken.")
                    else:
                        print(f"Link {href} in file {file_path} is working.")

                elif href.startswith('mailto:'):
                    print(f"Link in file {file_path} Leads to mailto. Skipping...")

                else:
                    href = "https://thapat.me/" + true_path + href

                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if response.status_code == 404:
                        print(f"Link {href} in file {file_path} is broken.")
                    else:
                        print(f"Link {href} in file {file_path} is working.")


