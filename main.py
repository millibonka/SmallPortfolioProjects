# Morse code converter 
import sys
import pandas as pd

MORSE_CODE_PATH = "data\morse.csv"


class MorseCodeConverter:
    def __init__(self):
        data = pd.read_csv(MORSE_CODE_PATH)
        self.morse_dict = {row.letter: row.code for (index,row) in data.iterrows()}
    
    def convert(self, message):
        output = None
        try:
            morse_code = [self.morse_dict[letter.upper()] for letter in message]
            output =  " ".join(morse_code)
            print(f"The morse code for {message} is: ", output)
        except KeyError:
                print("Only latin letters and numbers are supported.")



if __name__ == "__main__":
    converter = MorseCodeConverter()
    try:
        # for reading in message to convert directly from the command line
        message = sys.argv[1]
    except IndexError:
        message = input("Type your message: ")
    
    converter.convert(message)

    