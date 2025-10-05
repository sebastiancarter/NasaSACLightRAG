import xml.etree.ElementTree as ET
import os
import PyPDF2
import csv
import json
# Path of csv containing links and article titles
# if not using the usual one, have to modify this so it matches your csv
def getTitleIdJson(csvPath):
    titleIdDict = dict()
    with open(csvPath) as csvFile:
        reader = csv.DictReader(csvFile)
        print(reader.fieldnames)
        for row in reader:

            articleTitle = row['\ufeffTitle']
            articleLink = row['Link'].rstrip()
            articleID = articleLink.split("/")[-2]


            titleIdDict[articleID] = articleLink
    return titleIdDict

def getTextAndTitles():
    currentWorkingDir = os.getcwd()
    textList = []
    nameList = []

    initialDir = currentWorkingDir + os.sep + "nasa_papers" + os.sep + "extractedFiles"
    csvPath = currentWorkingDir + os.sep + "nasa_papers" + os.sep + "SB_publication_PMC.csv"
    print(f"Looking for articles in {initialDir}")
    titleIdDict = getTitleIdJson(csvPath)


    
    for articleDir in os.scandir(initialDir):
        if not os.path.isdir(initialDir + os.sep + articleDir.name):
            continue

        # HERE IT IS SEB
        articleTitle = titleIdDict[articleDir.name]
        print(f"Processing article: {articleTitle}")
        for item in os.scandir(initialDir + os.sep + articleDir.name):
            if item.name.endswith(".pdf"):
                wholeItemPath = initialDir + os.sep + articleDir.name + os.sep + item.name

                reader = PyPDF2.PdfReader(wholeItemPath)
                fullText = ""
                for page in reader.pages:
                    fullText += page.extract_text()


                textList.append(fullText)
                nameList.append(articleTitle)
    return textList, nameList
            

if __name__ == "__main__":
    texts, titles = getTextAndTitles()
    for i in range(len(texts)):
        print(f"Title: {titles[i]}")
        print(f"Text snippet: {texts[i][:500]}")
        print("========================================\n\n")
