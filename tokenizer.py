import re

def tokenizer(text, tokens):
    # This ensures the longer tokens are processed before the shorter ones, so that consonant clusters 
    # are processed before individual consonants first.
    sortedTokens = sorted(tokens, key=len, reverse=True)
    result = []
    i = 0
    # Splits the text into tokens
    while i < len(text):
        matched = False
        for token in sortedTokens:
            tokenLen = len(token)
            if text[i:i + tokenLen] == token:
                result.append(token)
                i += tokenLen
                matched = True
                break
        if matched == False:
            char = text[i]
            result.append(char)
            i += 1    
    return result

# Ensures the text is in lowercase and without punctuation for the font renderer.
def processWords(text):
    lower = text.lower()
    return [i for i in re.split(r'[ ():;\u0027\u0022\u2018\u2019,.?!\u2014\u2013-]', lower) if len(i)]

# Linguistic post-processing.
def postProcess(words, consonants):
    for word in words:
        for i in range(len(word)):
            # 'yi,'  'ye,'  'wu,'  and 'wo' are changed into
            # 'gi,'  'ge,'  'gu,'  and 'go' or into
            # 'kki,' 'kke,' 'kku,' and 'kko.'
            if word[i] == 'g' or word[i] == 'kk':
                if word[i + 1] == 'i' or word[i + 1] == 'e':
                    word[i] = 'y'
                else:
                    word[i] = 'w'
        # Retains the alphasyllabary quality of a default vowel being unwritten.
        for i in range(len(word)):
            if i >= len(word):
                break
            if word[i] == 'a':
                if i == 0 or i == len(word) - 1:
                    pass
                else:
                    if word[i - 1] in consonants and word[i + 1] in consonants:
                        word.pop(i)
                        i -= 1

# Integrates the above logic into a final function.
def fullProcesser(text):
    tokens = ["gā", "gi", "g", "kk", "sh", "mb", "ng", "nk", "ky", "ksh", "nm"]
    consonants = ["k", "l", "m", "f", "s", "y", "h", "r", "sh", "w", "v", "mb", "ng", "n", "nk", "b", "ky", "ksh", "nm", "z", "j"]
    words = processWords(text)
    result = [tokenizer(word, tokens) for word in words]
    postProcess(result, consonants)
    return result
