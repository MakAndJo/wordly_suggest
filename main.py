"""
    Wordle suggestion
"""
from random import randint

def main():
    """Main function"""

    words = [] # list of words
    alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)] # russian alphabet
    colors_dict = ('с', 'ж', 'з') # colors (no, partial, exact)

    with open('rus.txt', encoding='UTF-8') as file: # read the word bank from file
        for line in file:
            for word in line.split():
                words.append(word) # store the words

    def is_russian_word(word: str) -> bool:
        """Check if word is russian"""
        for symbol in word:
            if symbol not in alphabet:
                return False
        return True

    def is_valid_colors(colors: list) -> bool:
        """Check if colors are valid"""
        for color in colors:
            if color not in colors_dict:
                return False
        return True

    def check_word(word: str, require: list, ignore: list) -> bool:
        """Check if word is matches to our dynamic rules"""
        for symbol in require:
            if symbol not in word:
                return False
        for (pos, symbol) in enumerate(word):
            if symbol in ignore[pos]:
                return False
        return True

    def run():
        """Run quest loop"""

        required = [] # list of required symbols
        ignored = [[] for i in range(5)] # list of ignored symbols

        while True:
            print("\033[H\033[J", end="") # clear the screen

            answers = [] # list of answers

            for _ in range(100): # fast search
                word: str = words[randint(0, len(words) - 1)] # match the random one
                if check_word(word, required, ignored): # check if it matches to our rules
                    answers.append(word) # append if it does

            if len(answers) < 10: # if fast search sucks
                for i in words: # check all words
                    if check_word(i, required, ignored): # check if it matches to our rules
                        answers.append(i) # append if it does
                        if len(answers) >= 20: # break if more than 20 words
                            break

            if len(answers) == 0: # if no words found
                print('Не знаю таких слов!')
            else:
                print("Могу предложить тебе эти слова:\r")
                print("+\xa0-----\xa0+")
                answers.sort(key=lambda x: -len(set(x))) # sort words
                if len(answers) > 10: # if more than 10 words
                    answers = answers[:10] # only last 10 words
                for answer in answers:
                    print(f'|\xa0{answer.capitalize()}\xa0|')
                print("+\xa0-----\xa0+")
                if len(answers) == 1:
                    input("Нажмите Enter для продолжения...")
                    break

            while True:
                word: str = input('Слово:\xa0').lower()
                if not is_russian_word(word):
                    print("Ты шо на пендосском базаришь? Твоя моя не понимать.\n\rДавай ещё раз, но только по русски.")
                elif len(word) != 5:
                    print("Бля, нее. Я могу угадывать слова только из 5 символов. Не больше, не меньше!")
                else: break

            while True:
                colors: list = list(filter(str.strip, list(input('Цвета:\xa0').lower())))
                if not is_valid_colors(colors):
                    print("Invalid colors!", f"({colors})")
                elif len(colors) != 5:
                    print("Invalid colors length!")
                else: break

            for (pos, color) in enumerate(colors): # on each color
                symbol = word[pos] # current word symbol
                if color == colors_dict[0]: # [no match]
                    for (i, ignore) in enumerate(ignored): # on each position
                        ignore.append(symbol) # add symbol to ignore list
                elif color == colors_dict[1]: # [partial match]
                    ignored[pos].append(symbol) # add symbol to ignore list at that position
                    required.append(symbol) # add symbol to required list
                elif color == colors_dict[2]: # [exact match]
                    for letter in alphabet: # each letter in alphabet
                        if letter != symbol: # except current
                            ignored[pos].append(letter) # add to ignore list
    run()
    return False

if __name__ == '__main__':
    while True:
        main()
