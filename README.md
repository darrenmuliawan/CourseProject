# Project Overview

This project is made to improve the existing ExpertSearch system. My goal was to update the dataset used by ExpertSearch by creating a script that checks the URLs in the ```data/MP2_Part1 Signup - Sheet1.csv``` if they have new faculty members that wasn't added to the current ExpertSearch's dataset. 

# Implementation 

In order to find new faculty members, first I get the original email list that the current ExpertSearch used from ```data/emails```. I used faculty member's email to identify unique faculty member, since each person will most likely only have 1 email, and store it in Python dictionary for fast lookup. The next step is to crawl each faculty homepage URL from ```data/MP2_Part1 Signup - Sheet1.csv```, and scrape each page to get the list of faculty member's email addresses. If the email address does not exist in the dictionary key, then I assume that this faculty member was new (added after ExpertSearch was created). For each new faculty member, the crawler will get their bio URL, updates the dataset, and update other files which then will be used to create the index.

# Algorithm

1. Get the list of faculty homepage URLs from ```data/MP2_Part1 Signup - Sheet1.csv```
2. Scrape each URL and grab the ```a``` element that has href ```mailto:``` prefix, which is an indicator for an email address.
3. Look for their personal page URL by recursively check its HTML structure. The crawler will use the ```email_element``` found in step 1, grab its parent, then iterate its children to find another ```a``` element with ```href``` that starts with either ```/``` or ```http``` which, possibly, contains the link for their personal page.

Codeblock for recursively checks HTML structure,
```
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
```
4. Scrape the new member's bio page and store it in ```data/compiled_bios/n.txt```, where n is some number.
5. Update ```data/email```, ```data/depts```, ```data/location```, and ```data/unis``` with the new member's information
6. Use the modified ```extraction/extract_names.py``` to update ```data/names.txt```
7. Use the modified ```write_file_names.py``` to update ```data/compiled_bios/dataset-full-corpus.txt``` and ```data/compiled_bios/metadata.dat```
8. Rebuild the index with ```metapy.index.make_inverted_index(searchconfig)```

# Limitations

There are some limitations for this improvement due to the limitation of time since I am working on this project solo, such as,

1. When the crawler looks for the faculty member's bio URL, it assumes that the URL is located somewhere in other ```a``` element's href. If the link is not in the href, then it won't be able to find the bio URL. It may also find an incorrect URL if the link is not in other element's href.
2. ExpertSearch's script to get the faculty member's name uses Stanford Named Entity Recognizer (NER) Tagger, which doesn't 100% correctly detect the faculty member's name
3. ExpertSearch's script to get the location relies on Google Maps API which may not be free since we are dealing with thousands of faculty members. So for the new faculty members, I set the location to be UNKNOWN, United States
4. There is a mismatch in the number of records for ```data/urls```
5. Need to restart the app everytime the crawler finished to view the new faculty members

# How to run the code
Note: Make sure you have both Python 2.7 and Python3 since some of ExpertSearch script does not work on Python 2.7 and some of them does not work on Python 3. For reference, I am using Python 2.7.16 and Python 3.7.7

### Run crawler scripts
```
python crawler.py [max_found] [run_forever]
```
```max_found``` is the maximum number of new faculty members that you want to find before it updates the dataset.
```run_forever``` sets to ```true``` if you want the crawler to loop forever.

For example,
```
python crawler.py 10 true
```

For continuous checking and without limit, either set ```max_found``` to be ```-1``` and ```run_forever``` to be ```true``` or run ```python crawler.py```.

### Run ExpertSearch app
```
gunicorn server:app -b 127.0.0.1:8095
```

# How to check this project
Open the original ExpertSearch ```http://timan102.cs.illinois.edu/expertsearch//``` and open the updated ExpertSearch at ```localhost:8095```. Find the name of recently added faculty members by looking at ```new_bios/trial-n.txt``` and open the bio URL. The new members should only appear in the updated ExpertSearch.

# Video Link
https://mediaspace.illinois.edu/media/t/1_ybtlfoxk
