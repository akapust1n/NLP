# считаем, что постматчевые интервью - предматчевые
# алгортм :
# ) ищем ближайший по дате матч(в большую стороны) и смотрим результат
#  находит всего 2107 из потенциально возможных 4207 -  можно находить больше
import json
import csv
import xlrd
from datetime import datetime, date, time

infile = open('tennis.csv', 'r')
outfile = open('tennis2.csv', 'w')
csvWriter = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
csvReader = csv.reader(infile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
book2007 = xlrd.open_workbook("data/2007.xls")
sheet2007 = book2007.sheet_by_index(0)
book2008 = xlrd.open_workbook("data/2008.xls")
sheet2008 = book2008.sheet_by_index(0)
book2009 = xlrd.open_workbook("data/2009.xls")
sheet2009 = book2009.sheet_by_index(0)
book2010 = xlrd.open_workbook("data/2010.xls")
sheet2010 = book2010.sheet_by_index(0)
book2011 = xlrd.open_workbook("data/2011.xls")
sheet2011 = book2011.sheet_by_index(0)
book2012 = xlrd.open_workbook("data/2012.xls")
sheet2012 = book2012.sheet_by_index(0)
book2013 = xlrd.open_workbook("data/2013.xlsx")
sheet2013 = book2007.sheet_by_index(0)
book2014 = xlrd.open_workbook("data/2014.xlsx")
sheet2014 = book2014.sheet_by_index(0)
book2015 = xlrd.open_workbook("data/2015.xlsx")
sheet2015 = book2015.sheet_by_index(0)


def getSheet(year):
    if(year == 2007):
        return sheet2007, book2007
    if(year == 2008):
        return sheet2008, book2008
    if(year == 2009):
        return sheet2009, book2009
    if(year == 2010):
        return sheet2010, book2010
    if(year == 2011):
        return sheet2011, book2011
    if(year == 2012):
        return sheet2012, book2012
    if(year == 2013):
        return sheet2013, book2013
    if(year == 2014):
        return sheet2014, book2014
    if(year == 2015):
        return sheet2015, book2015


founded = 0
for row in csvReader:
    mydate = row[2]
    surname = row[3].split(" ")[1]
    year = int(mydate[:4])
    month = int(mydate[5:7])
    day = int(mydate[8:10])
    sheet, book = getSheet(year)
    # print(day, month, year)
    print(surname)
    print(int(year))
    tournament = ""
    for row_num in range(sheet.nrows):
        if(row_num == 0):
            continue
        row_value = sheet.row_values(row_num)
        _, monthXls, dayXls, _, _, _ = xlrd.xldate_as_tuple(
            sheet.cell_value(row_num, 3), book.datemode)

        # print(day, dayXls, month, monthXls)
        if (monthXls == month and day == dayXls):
            # print("data match_____________________________-")
            surnameXls = row_value[9].split(" ")[0]

            if(surname == surnameXls):
                print(surname, surnameXls)
                tournament = row_value[9]
                break

    dates = {}
    if(len(tournament) > 0):
        for row_num in range(sheet.nrows):
            if(row_num == 0):
                continue
            row_value = sheet.row_values(row_num)
            _, monthXls, dayXls, _, _, _ = xlrd.xldate_as_tuple(
                sheet.cell_value(row_num, 3), book.datemode)
            #dayXls = int(dayXls)
            #monthXls = int(monthXls)
        # print(day, dayXls, month, monthXls)
            if (monthXls == month and day > dayXls or month < monthXls):
                # print("data match_____________________________-")
                surnameXls = row_value[9].split(" ")[0]
                surnameXlsLooser = row_value[10].split(" ")[0]

                if(surname == surnameXls):
                    matchDate = date(year=year, day=dayXls, month=monthXls)
                    dates[matchDate] = 1
                if(surname == surnameXlsLooser):
                    matchDate = date(year=year, day=dayXls, month=monthXls)
                    dates[matchDate] = 0

    if(len(dates) > 0):
        mymin = min(dates)
        print(min(dates), surname)
        csvWriter.writerow([dates[mymin], row[4]])

        founded += 1
    else:
        print("cant find matches!___")
print("found", founded)
