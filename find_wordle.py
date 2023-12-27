import requests
import re
from bs4 import BeautifulSoup
from datetime import date

content_headers = {
    'difficulty': "average difficulty is",
    'word': "word is"
}
        
difficulty_decoder = {
    'one': 1.0,
    'two': 2.0,
    'three': 3.0,
    'four': 4.0,
    'five': 5.0,
    'six': 6.0
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
            if crumb[4] in difficulty_decoder:
                return difficulty_decoder.get(crumb[4])
            else:
                return float(crumb[4])
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
            return crumb[3].replace(',', '').lower()
        else:
            return None

def find_wordle(month: str = None, day: str = None, year: str = None):
    if not month or not day or not year: 
        year, month, day = str(date.today()).split('-')
    if len(day) == 1:
        day = '0' + day
        
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.65 Mobile Safari/537.36'}
    difficulty = None
    word = None
    
    url = f'https://www.nytimes.com/{year}/{month}/{day}/crosswords/wordle-review.html'
    page = requests.get(url, headers=headers)
    results = BeautifulSoup(page.content, "html.parser" ).find(id="app")
    content = results.find_all("p", class_="css-at9mc1 evys1bk0")
    
    for crumb in content:
        crumb = re.sub(r'<[^>]*>', '', str(crumb))
        
        if content_headers.get('difficulty') in crumb:
            difficulty = parse_content(crumb, True)
        elif content_headers.get('word') in crumb:
            word = parse_content(crumb, False)
    
    return word, difficulty