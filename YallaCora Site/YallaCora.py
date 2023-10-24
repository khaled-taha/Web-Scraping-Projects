import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime


date = input('Enter the date in the following format M/DD/YYYY : ')
format = "%m/%d/%Y"


try:
    datetime.strptime(date, format)
    print("Valid date format")
except ValueError:
    print("Invalid date format")


page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}");

if (page.status_code == 200):
    # Get the content of the request
    src = page.content

    # convert the content from byte code for readable code
    soup = BeautifulSoup(src, "lxml")
    
    # creaet a list for your contents (rows of CSV)
    matches_details = []

    championships = soup.find_all('div', {'class':'matchCard'})

    for championship in championships:
        title = championship.contents[1].find('h2').text.strip()
        matches = championship.contents[3].find_all('li')
        for match in matches:
            teamA = match.find('div', {'class' : 'teamA'}).find('p').text.strip()
            teamB = match.find('div', {'class' : 'teamB'}).find('p').text.strip()
            result_time = match.find('div', {'class' : 'MResult'})

            result = result_time.find_all('span', {'class':'score'})
            score = f"{result[1].text.strip()}" + '--' + f"{result[0].text.strip()}"

            time = result_time.find('span', {'class':'time'}).text.strip()
            
            matches_details.append({'نوع البطولة' : title,  'الفريق الأول' : teamA, 'الفريق الثاني' : teamB
                                    , 'النتيجة' : score, 'التاريخ' : time})
            
    
header = matches_details[0].keys()
with open('E:\Courses\Web Scraping\matches.csv', 'w') as output:
    output_writer = csv.DictWriter(output, header)
    output_writer.writeheader()
    output_writer.writerows(matches_details)


        



    



