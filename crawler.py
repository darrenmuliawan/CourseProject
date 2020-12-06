from csv import reader
import urllib2
from urllib2 import HTTPError
from bs4 import BeautifulSoup
import re
import unicodedata
import os

compiled_bios_path = "./data/compiled_bios/"

def crawler(email_table):
    # variables
    urls = []

    # GET LIST OF URLS FROM SIGNUP SHEET
    signupSheets = "./data/MP2_Part1 Signup - Sheet1.csv"

    with open(signupSheets, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader, None)
        for row in csv_reader:
            urls.append(row[3]) 
    print('Found ' + str(len(urls)) + ' URLs.')

    # START FOREVER LOOP
    #while (true):
    # GET NEW FACULTY MEMBER'S BIO PAGE URL
    bios, emails = getNewFacultyBiosURL(urls, email_table)
    updateNewBios(bios, emails)
    updateOtherFiles()

def updateOtherFiles():
    path = os.path.dirname(os.path.realpath(__file__))
    #path_extract_email = path + "/extraction/extract_email.py"
    path_extract_name = path + "/extraction/extract_name.py"
    print(path_extract_name)
    #os.system('cd extraction')
    #os.system('python3 ' + path_extract_name)

def updateNewBios(bios, emails):
    # GET THE CURRENT MAX NUMBER OF .TXT BIOS FILE
    filename = len(os.listdir(compiled_bios_path)) - 5

    new_bios_file = open("new_bios.txt", "a")
    fail_add_bios_file = open("fail_bios.txt", "a")
    email_file = open("./data/emails", "a")

    for i in range(len(bios)):
        try:
            bio = bios[i]
            email = emails[i]

            # PARSE BIO TEXT
            html = urllib2.urlopen(bio)
            soup = BeautifulSoup(html, 'html.parser')
            texts = soup.get_text()
            texts = re.sub('\s+',' ',texts)
            texts = texts.encode('ascii', 'ignore').decode()

            # WRITE BIOS TO FILE
            new_file = compiled_bios_path + str(filename) + ".txt"
            f = open(new_file, "w")
            f.write(texts)
            f.close()

            # WRITE EMAIL TO FILE
            # email_file.write(email + "\n")

            # RECORD NEW BIOS
            new_bios_file.write(bio + "\n")

            # INCREMENT FILENAME
            filename += 1
        except HTTPError as err:
            # RECORD FAILED BIOS
            fail_add_bios_file.write(bio + "\n")
    new_bios_file.close()
    fail_add_bios_file.close()

def getNewFacultyBiosURL(urls, email_table):
    new_faculty_bios_url = []
    for i in range(1):
        url = urls[i]
        print("\nWorking on: " + url)
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        emails = []

        for a in soup.select("a[href^=\"mailto:\"]"):
            email = a["href"].split("mailto:")[1]
            if email not in email_table:
                # NEW FACULTY MEMBER FOUND, FIND ITS PAGE LINK
                element = a.parent
                while True:
                    a2 = element.find("a")

                    # CHECK IF THE LINK IS (MAYBE) A FACULTY MEMBER'S PAGE
                    if a2.has_attr('href'):
                        href = a2['href'].encode('ascii')
                        if a2 != a and (href.startswith("/") or href.startswith("http")):
                            new_faculty_bios_url.append(href)
                            emails.append(email)
                            break
                    element = element.parent
                    if element is None:
                        break

    total_new = len(new_faculty_bios_url)
    print("Found " + str(total_new) + " new faculty members.")
    return new_faculty_bios_url, emails

def initHashTable():
    emails = "./data/emails"
    urls = "./data/urls"
    hash_table = {}
    with open(emails, 'r') as emails_obj:
        with open(urls, 'r') as urls_obj:
            emails_arr = []
            urls_arr = []
            for email in emails_obj:
                emails_arr.append(email.strip('\n'))
            for url in urls_obj:
                urls_arr.append(url.strip('\n'))
            for i in range(len(emails_arr)):
                cur_email = emails_arr[i]
                cur_url = urls_arr[i]
                if cur_email == "":
                    continue
                hash_table[cur_email] = cur_url
    return hash_table

def main():
    email_table = initHashTable()
    crawler(email_table)

if __name__ == '__main__':
    main()