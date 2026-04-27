import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(phonetic_dict)


word = input("Enter a word: ").upper()
while True:
    try:
        output_list = [phonetic_dict[letter] for letter in word]
        print(output_list)
        break
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
    word = input("Enter a word: ").upper()
    