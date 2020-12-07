from csv import reader
import urllib2
from urllib2 import HTTPError
from bs4 import BeautifulSoup
import re
import unicodedata
import os
import metapy
import json
import subprocess

compiled_bios_path = "./data/compiled_bios/"

def crawler(email_table):
    # variables
    urls = []
    unis = []
    depts = []

    # GET THE CURRENT MAX NUMBER OF .TXT BIOS FILE
    start_index = len(os.listdir(compiled_bios_path)) - 5

    # GET LIST OF URLS FROM SIGNUP SHEET
    signupSheets = "./data/MP2_Part1 Signup - Sheet1.csv"

    with open(signupSheets, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader, None)
        for row in csv_reader:
            unis.append(row[1])
            depts.append(row[2])
            urls.append(row[3]) 
    print('Found ' + str(len(urls)) + ' URLs.')
    
    # GET NEW FACULTY MEMBER'S BIO PAGE URL
    bios, emails, new_unis, new_depts = getNewFacultyBiosURL(urls, email_table, unis, depts)

    # UPDATE DATA FILES
    updateNewBios(bios, emails, new_unis, new_depts, start_index)
    updateOtherFiles(start_index)

def updateOtherFiles(start_index):
    path = os.path.dirname(os.path.realpath(__file__))
    path_extract_name = path + "/extraction/extract_names.py"
    path_extract_location = path + "/extraction/get_location.py"
    path_write_file_names = path + "/write_file_names.py"
    path_index_folder = path + "/FacultyDataset-idx"

    # RUN EXTRACTION FILES
    print("\nStart name extraction from " + str(start_index) + ".txt")
    subprocess.call(('python3', path_extract_name, str(start_index)))

    #print("\nStart location extraction")
    #subprocess.call(('python3', path_extract_location))
    #os.system('python3 ' + path_extract_name)
    #os.system('python3 ' + path_extract_location)

    # RUN write_file_names.py
    print('\nStart write_file_names.py')
    subprocess.call(('python3', path_write_file_names, str(start_index)))
    #os.system('python3 ' + path_write_file_names)

    # DELETE THE INDEX
    print('\nDeleting FacultyDataset-idx folder...')
    os.system('rm -rf ' + path_index_folder)

    # REBUILD THE INDEX
    print('\nRebuilding index...')
    dataconfig = json.loads(open("config.json", "r").read())
    environ = 'development'
    searchconfig = dataconfig[environ]['searchconfig']
    index = metapy.index.make_inverted_index(searchconfig)

def updateNewBios(bios, emails, unis, depts, start_index):
    filename = start_index
    new_bios_file = open("new_bios.txt", "a")
    fail_add_bios_file = open("fail_bios.txt", "a")
    email_file = open("./data/emails", "a")
    unis_file = open("./data/unis", "a")
    depts_file = open("./data/depts", "a")
    location_file = open("./data/location", "a")

    for i in range(len(bios)):
        bio = bios[i]
        email = emails[i]
        uni = unis[i]
        dept = depts[i]
        
        try:
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
        except HTTPError as err:
            # WRITE BIOS TO FILE
            new_file = compiled_bios_path + str(filename) + ".txt"
            f = open(new_file, "w")
            f.write("")
            f.close()

            # RECORD FAILED BIOS
            fail_add_bios_file.write(bio + "\n")

        # UPDATE EMAIL, DEPTS, UNIS, AND LOCATION
        email_file.write(email + "\n")
        depts_file.write(dept + "\n")
        unis_file.write(uni + "\n")
        location_file.write("Illinois" + "\tUnited States\n")

        # RECORD NEW BIOS
        new_bios_file.write(bio + "\n")

        # INCREMENT FILENAME
        filename += 1

    new_bios_file.close()
    fail_add_bios_file.close()
    email_file.close()
    depts_file.close()
    unis_file.close()
    location_file.close()

def getNewFacultyBiosURL(urls, email_table, unis, depts):
    new_faculty_bios_url = []
    found = 0
    for i in range(1):
        url = urls[i]
        uni = unis[i]
        dept = depts[i]
        print("\nWorking on: " + url)
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        emails = []
        new_unis = []
        new_depts = []

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
                            new_unis.append(uni)
                            new_depts.append(dept)
                            found += 1
                            break
                    element = element.parent
                    if element is None:
                        break
            if found == 2:
                break

    total_new = len(new_faculty_bios_url)
    print("Found " + str(total_new) + " new faculty members.")
    return new_faculty_bios_url, emails, new_unis, new_depts

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