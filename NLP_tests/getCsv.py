#данные на основе постматчевых интервью
import json
import csv

with open('tennis.csv', 'w') as outfile:
    csvWriter = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    with open('transcripts_matchinfo.json', 'r') as infile:
        datastore = json.load(infile)
        result = {}
        for i in range(0, 6465):
            elem = datastore[str(i)]
            result[i] = ""
            print(i)
            for arr in elem["QandA"]:
                result[i] += arr[1]
            csvWriter.writerow([elem["result"], result[i]])
            del result[i]

    # print(datastore[str(0)]["QandA"][0][0])
    # result[str(i)]
