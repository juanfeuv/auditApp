import csv
import codecs

def csvToJson(file):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    jsonArray = []

    for row in csvReader:             
       jsonArray.append(row) 
        
    file.file.close()

    return jsonArray