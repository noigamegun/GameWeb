import requests
import os
from bs4 import BeautifulSoup

html_files = []
knownhtmlfiles = []
brokenlink = False
external = False
missingknownhtmlfile = False
unknownhtmlfile = False

# Specify the path to your repository
repo_path = '/home/runner/work/GameWeb/GameWeb/'

with open('/home/runner/work/GameWeb/GameWeb/.github/scripts/CheckLinks/knownhtmlfiles.txt', 'r') as f:
    for line in f:
        knownhtmlfiles.append(line.rstrip('\n'))
actualknownhtmlfilespath = []
actualknownhtmlfilescount = 0
for i in knownhtmlfiles:
    actualknownhtmlfilespath.append("/home/runner/work/GameWeb/GameWeb/" + knownhtmlfiles[actualknownhtmlfilescount])
    actualknownhtmlfilescount += 1

print("Known HTML Files: " + str(knownhtmlfiles))
print("\n")
print("Actual Known HTML Files Path: " + str(actualknownhtmlfilespath))

# Traverse through all directories and files in the repository
for root, dirs, files in os.walk(repo_path):
    for file in files:
        # Check if the file is an HTML file
        if file.endswith('.html'):
            # Add the file path to the list
            if os.path.join(root, file) not in actualknownhtmlfilespath:
                print("Expected html file : " + os.path.join(root, file) + " not found in knownhtmlfile.txt. Please check if the file exists in the repository and add it to knownhtmlfile.txt. Checking it anyway...")
                html_files.append(os.path.join(root, file))
                missingknownhtmlfile = True
            elif os.path.join(root, file) in actualknownhtmlfilespath:
                print("Expected html file : " + os.path.join(root, file) + " found in knownhtmlfile.txt.")
                html_files.append(os.path.join(root, file))
            else:
                print("Unknown html file : " + os.path.join(root, file) + " found. Please check if the file is valid in the repository and add it to knownhtmlfile.txt. Checking it anyway...")
                html_files.append(os.path.join(root, file))
                unknownhtmlfile = True

# Print the list of HTML files for debugging
print("html files that is going to be checked : " + str(html_files))
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

# DANG IM DUMB
print("All checks are done. Here are the results:")
if brokenlink:
    print()
    print("There are broken local files link or links in the repository.")
if external:
    print()
    print("There are broken external link or links in the repository.")
    print("This is moslty due to the fact that the website is not available as the time of this check.")
    print("If this is a false positive, please check the website manually and rerun the check.")
    print("If this is a false positive and a pull request, please contact the owner of the repository.")
if missingknownhtmlfile:
    print()
    print("There are missing known html files in the repository.")
    print("Please check if the file exists in the repository and add it to knownhtmlfile.txt.")
    print("Or if the file is invalid, please remove it from knownhtmlfile.txt.")
if unknownhtmlfile:
    print()
    print("There are unknown html files in the repository.")
    print("Please check if the file is valid in the repository and add it to knownhtmlfile.txt.")
    print("Or if the file is invalid, please remove it from the repository.")
