import requests
import os
from bs4 import BeautifulSoup

html_files = []
brokenlink = False
external = False

# Specify the path to your repository
repo_path = '/home/runner/work/GameWeb/GameWeb/'

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
    true_path = os.path.relpath(os.path.dirname(file_path), start="/home/runner/work/GameWeb/GameWeb") + "/"
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
                print()
                print(f"Link in file {file_path} Leads to nothing. Skipping...")
                print()
            # If the link is not a "#"
            else:
                # Check if the link is an external link
                if href.startswith('http://') or href.startswith('https://'):
                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if response.status_code != 200:
                        print()
                        print(f"External link {href} in file {file_path} is broken.")
                        print("This is moslty due to the fact that the website is not available as the time of this check.")
                        print("If this is a false positive, please check the website manually and rerun the check.")
                        print("If this is a false positive and a pull request, please contact the owner of the repository.")
                        print("received status code: " + str(response.status_code))
                        print()
                        external = True
                    else:
                        print()
                        print(f"External link {href} in file {file_path} is working.")
                        print()

                # Check if the link is an email link
                elif href.startswith('mailto:'):
                    print()
                    print(f"Link in file {file_path} Leads to mailto. Skipping...")
                    print()

                # If the link is not an external link or an email link and it a local file in the repository
                else:
                    href = "/home/runner/work/GameWeb/GameWeb/" + true_path + href

                    # Make a request to the URL
                    response = requests.head(href)

                    # Check the response status code
                    if os.path.isfile(href):
                        print()
                        print(f"Local file link {href} in file {file_path} is working")
                        print()
                    else:
                        print()
                        print(f"Local file link {href} in file {file_path} is broken.")
                        print()
                        brokenlink = True

# Report the result of the link check. If there are broken links, exit with a non-zero status code to trip GitHub Actions.
if brokenlink:
    print("\n")
    print("All links have been checked.")
    print("One or more local links are broken.")
    exit(1)
elif external:
    print("\n")
    print("All links have been checked.")
    print("One or more external links are broken.")
    exit(1)
elif brokenlink and external:
    print("\n")
    print("All links have been checked.")
    print("One or more local and external links are broken.")
    exit(1)
else:
    print("\n")
    print("All links have been checked and passed.")
