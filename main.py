from find_wordle import find_wordle
from solver import solver
import sys

def main():
    month = None
    day = None
    year = None

    try:
        month = sys.argv[1]
        day = sys.argv[2]
        year = sys.argv[3]
        print(f'using wordle from: {month}-{day}-{year}')
    except:
        print(f"using wordle from today")

    word, difficulty = find_wordle(month, day, year)
    results = solver(word)
    print(results)

main()