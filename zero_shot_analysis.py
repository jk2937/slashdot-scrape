'''
Copyright 2024 Jonathan Kaschak

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
'''
import sqlite3
import datetime
from transformers import pipeline


connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ZeroShotAnalysis ( ID INTEGER PRIMARY KEY AUTOINCREMENT, ArticleID INTEGER, AnalysisDate TEXT, Label TEXT, Score REAL );")
connection.commit()

cursor.execute("SELECT * FROM articles;")
data = cursor.fetchall()

connection.commit()


date = datetime.datetime.now()
date_str = date.strftime("%m-%d-%Y %I:%M %p")

classifier = pipeline("zero-shot-classification")
label = "cybersecurity"

for row in data:
    id_, scrape_date, title, description, link = row
    row_data = {
        "id": id_,
        "scrapep_date": scrape_date,
        "title": title,
        "description": description,
        "link": link
    }

    cursor.execute("SELECT COUNT(1) FROM ZeroShotAnalysis WHERE ArticleID = ? AND Label = ?;", (row_data["id"], label))
    count = cursor.fetchone()[0]

    if count == 0:
        print("Classifying.")

        analysis = classifier(
            row_data["title"] + "\n" + row_data["description"],
            candidate_labels=[label]
        )
        score = analysis["scores"][0]

        cursor.execute("INSERT INTO ZeroShotAnalysis ( ArticleID, AnalysisDate, Label, Score ) VALUES ( ?, ?, ?, ? );", (row_data["id"], date_str, label, score)) 
        connection.commit()

    else:
        print("Skipping duplicate database entry: " + row_data["title"])


cursor.execute("SELECT articles.title, ZeroShotAnalysis.Score FROM articles INNER JOIN ZeroShotAnalysis ON articles.id = ZeroShotAnalysis.ArticleID;")
data = cursor.fetchall()

for row in data:
    print(row)

print(str(len(data)) + " rows total.")

cursor.close()
connection.close()
