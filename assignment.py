import requests
from bs4 import BeautifulSoup as bs
import xlsxwriter

# In the given link ,295 tabs are there, so we can iterate to every file by just adjusting "whole" variable
# for now we will only see data till 10 tabs

whole=100
count=0
linked=[]

while(count!=whole):
    url = f"https://www.hopkinsmedicine.org/profiles/search?query=&page={count}"
    response = requests.get(url)
    soup=bs(response.text,'lxml')
    store=soup.find("ul",class_="faculty-results-list")
    data=store.find_all("li")
    for li in data:
        inside = li.find("a")

        href = inside.get("href") if inside else None
        if href:
            if(href):
                linked.append("https://www.hopkinsmedicine.org"+href)
    count+=1

allData=[]
for link in linked:
    newdata = requests.get(link)
    sour = bs(newdata.text, 'lxml')
    entry = {}

# Name
    try:
        file = sour.find("div", class_="name")
        name = (file.h1.text.split(",")[0].strip())
        entry["Name"] = name
    except AttributeError:
        entry["Name"] = None
# Title
    try:
        file = sour.find("div", class_="name")
        title = file.h1.text.split(",")[1].strip()
        entry["Title"] = title
    except IndexError:
        entry["Title"] = None
# Gender
    try:
        file = sour.find("div", class_="gender")
        gender = file.text
        entry["Gender"] = gender
    except AttributeError:
        entry["Gender"] = None
# expertise
    try:
        file = sour.find("div", class_="expertise")
        p = file.find('p')
        expertise = p.get_text()
        if '...read more' in expertise:
            expertise = expertise.replace('...read more', '')

        entry["Expertise"] = expertise
    except AttributeError:
        entry["Expertise"] = None
# Phone
    try:
        file = sour.find("div", class_="phone")
        phone_text = file.text.strip()

        if "Phone:" in phone_text:
            phone = phone_text.split("Phone:")[1].strip().split("|")[0].strip()
        else:
            phone = phone_text.strip()

        entry["Phone"] = phone

    except AttributeError:
        entry["Phone"] = None
# location
    try:
        file = sour.find("div", class_="practice loc-chosen")
        add = file.find("h3")
        additional = sour.find("div", class_="address")
        additional = additional.text.replace("map", "")
        location = (add.text.strip() + " " + additional.strip().replace(" ", ""))
        entry["Location"] = location
    except AttributeError:
        entry["Location"] = None
# education
    try:
        collect = sour.find("div", class_="section education")
        file = collect.find("li")
        education_list = file.text.split("; ")
        if len(education_list) >= 2:
            education = education_list[1]
        else:
            education = None
        entry["Education"] = education
    except AttributeError:
        entry["Education"] = None


    allData.append(entry)
print("Scraping done successfully!!!")
# we can use this to print all key value pairs 
# for data in allData:
#     for key, value in data.items():
#         print("{}: {}".format(key, value))
#     print()

workbook = xlsxwriter.Workbook("Assignment.xlsx")
worksheet = workbook.get_worksheet_by_name('AssignmentSheet')
if worksheet is None:
    worksheet = workbook.add_worksheet('AssignmentSheet')

worksheet.write(0, 0, "#")
worksheet.write(0, 1, "Name")
worksheet.write(0, 2, "Title")
worksheet.write(0, 3, "Gender")
worksheet.write(0, 4, "Expertise")
worksheet.write(0, 5, "Phone")
worksheet.write(0, 6, "Location")
worksheet.write(0, 7, "Education")

for index, entry in enumerate(allData):
    worksheet.write(index + 1, 0, str(index))
    worksheet.write(index + 1, 1, entry["Name"])
    worksheet.write(index + 1, 2, entry["Title"])
    worksheet.write(index + 1, 3, entry["Gender"])
    worksheet.write(index + 1, 4, entry["Expertise"])
    worksheet.write(index + 1, 5, entry["Phone"])
    worksheet.write(index + 1, 6, entry["Location"])
    worksheet.write(index + 1, 7, entry["Education"])

workbook.close()
print("Added to xlsx file!!")