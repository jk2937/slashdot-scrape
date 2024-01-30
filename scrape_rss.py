'''
Copyright 2024 Jonathan Kaschak

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
'''
import requests
import datetime
from pathlib import Path
from xml.dom import minidom
import sqlite3

def scrape_slashdot():

    print("\n\nDownload slashdot.org rss feed and save to file or read existing file:\n")

    date = datetime.datetime.now()
    date_str = date.strftime("%m-%d-%Y %I:%M %p")

    filename = "xml/Slashdot RSS " + date_str + ".xml"
    filename_path = Path(filename)

    contents = ""

    if filename_path.is_file():
        print(filename + " exists. Reading data from file.")

        file = open(filename_path, "r")
        contents = file.read()

    else:
        print(filename + " does not exist. Downloading data.")

        url = "https://rss.slashdot.org/Slashdot/slashdotMain"
        response = requests.get(url)

        file = open(filename_path, "wb")
        file.write(response.content)

        contents = response.content


    print("\n\nParse xml:\n")

    dom = minidom.parseString(contents)
    items = dom.getElementsByTagName("item")

    def get_tag_content(dom, tag):
        content = dom.getElementsByTagName(tag)[0].childNodes[0].data
        return content

    articles = []

    for item in items:
        item_content = item.childNodes

        item_content = {
            "title": "",
            "description": "",
            "link": ""
        }

        for key in item_content:
            item_content[key] = get_tag_content(item, key)

        item_content["description"] = item_content["description"].split("<p>")[0]

        print("Got article: " + item_content["title"])

        articles.append( item_content )


    print("\n\nAdd to database:\n")

    sql_connection = sqlite3.connect("database.db")

    cursor = sql_connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS articles( id INTEGER PRIMARY KEY AUTOINCREMENT, scrape_date TEXT, title TEXT, description TEXT, link TEXT );")
    sql_connection.commit()

    for article in articles:
        cursor.execute("SELECT COUNT(1) FROM articles WHERE title = ?", (article["title"],))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("INSERT INTO articles( title, description, link ) VALUES ( ?, ?, ? );", (article["title"], article["description"], article["link"]) )
            sql_connection.commit()

        else:
            print("Skipping duplicate database entry. (" + article["title"] + ")")

if __name__ == "__main__":
    scrape_slashdot()
    print("\n\nExit.\n")
