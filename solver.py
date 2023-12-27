from game.constants import DEFAULT_N, DEFAULT_MAX_GUESSES, DEFAULT_GAME_CONFIG, DEFAULT_SOLVER_SETTINGS, DEFAULT_DICT, DEFAULT_CAND_DICT
from game.solver.solver import guess_next_word
from game.util import read_words_of_length
from typing import Dict

def verify(chosen: str, answer: str):
    result = ''
    for letter in range(len(chosen)):
        current_letter = chosen[letter]
        if current_letter not in answer:    # gray check
            result += '0'
        
        # at this point, the chosen letter is SOMEWHERE in the answer
        elif answer.count(current_letter) > 1:
            if answer[letter] == current_letter:
                result += '2'
            else:
                result += '1'
        else: 
            if answer.find(current_letter) == letter:
                result += '2'
            else:
                result += '1'
        
    return result 

def solve(game_config: Dict[str, str], solver_settings: Dict[str, str], answer=None):
    clues = []
    choices = []
    guesses = 0
    
    while guesses < int(game_config['max_guesses']):
        chosen, cands, lencands = guess_next_word(clues, solver_settings=solver_settings, debug=0)
        if not chosen:
            return choices

        feedback = verify(chosen, answer)
        feedback = feedback.strip()
        if len(set(feedback + '012')) <= 3:
            feedback_parsed = [ord(f) - ord('0') for f in feedback]

        guesses += 1
        choices.append((chosen, feedback))
        clues.append((chosen, feedback_parsed)) 

    return choices

def solver(answer: str):
    try:
        word_set = read_words_of_length(DEFAULT_N, fname=DEFAULT_DICT)
        candidate_set = read_words_of_length(DEFAULT_N, fname=DEFAULT_CAND_DICT)
    except Exception as e:
        return None
    
    game_config = DEFAULT_GAME_CONFIG
    game_config['max_guesses'] = str(DEFAULT_MAX_GUESSES)
    game_config['candidate_set'] = candidate_set
    game_config['guess_set'] = word_set
    solver_settings = DEFAULT_SOLVER_SETTINGS
    solver_settings['max_guesses'] = str(DEFAULT_MAX_GUESSES)
    solver_settings['non_strict'] = False
    solver_settings['candidate_set'] = candidate_set
    solver_settings['guess_set'] = word_set

    return solve(game_config=game_config, solver_settings=solver_settings, answer=answer)



