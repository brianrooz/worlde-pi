import requests
import re
import sys
from bs4 import BeautifulSoup
from datetime import date

content_headers = {
    'difficulty': "average difficulty is",
    'word': "word is"
}

def parse_content(crumb: str, difficulty: bool):
    if difficulty:
        crumb = crumb.split(' ')
        header_split = content_headers.get('difficulty').split(' ')
        
        failed = False
        for word in range(1, 4):
            if crumb[word] != header_split[word - 1]:
                failed = True
                break
        if not failed:
            return crumb[4]
        else:
            return None
                
    else:
        crumb = crumb.split(' ')
        header_split = content_headers.get('word').split(' ')
        
        failed = False
        for word in range(1, 3):
            if crumb[word] != header_split[word - 1]:
                failed = True
                break
        if not failed:
            return crumb[3].replace(',', '')
        else:
            return None

def main():
    # year, month, day = str(date.today()).split('-')
    # if len(day) == 1:
    #     day = '0' + day
    
    year = 2023
    month = sys.argv[1]
    day = sys.argv[2]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Wind64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = [None, None]
    
    url = f'https://www.nytimes.com/{year}/{month}/{day}/crosswords/wordle-review.html'
    page = requests.get(url, headers=headers)
    results = BeautifulSoup(page.content, "html.parser" ).find(id="app")
    content = results.find_all("p", class_="css-at9mc1 evys1bk0")
    
    for crumb in content:
        crumb = re.sub(r'<[^>]*>', '', str(crumb))
        
        if content_headers.get('difficulty') in crumb:
            response[1] = parse_content(crumb, True)
        elif content_headers.get('word') in crumb:
            response[0] = parse_content(crumb, False)
    
    print(response)
    
main()