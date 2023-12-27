import sys

def verify(chosen: str, answer: str):
    check = [0, 0, 0, 0, 0]
    result = ''
    for letter in range(len(chosen)):
        current_letter = chosen[letter]
        if current_letter not in answer:    # gray check
            check[letter] = 0
        
        # at this point, the chosen letter is SOMEWHERE in the answer
        elif answer.count(current_letter ) > 1:
            if answer[letter] == current_letter:
                check[letter] = 2
            else:
                check[letter] = 1
        else: 
            if answer.find(current_letter) == letter:
                check[letter] = 2
            else:
                check[letter] = 1 

    for number in check:
        result += str(number)
    
    return result 

def main():
    answer = sys.argv[1]
    chosen = sys.argv[2]

    print(verify(chosen, answer))

main()