import enchant


# function for checking spelling english words
def check_spelling(word):
    dictionary = enchant.Dict('en_US')
    check_result = dictionary.check(word)
    return check_result
