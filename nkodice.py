import random
from collections import Counter

dice = (("う", ["U"], 500), ("ま", ["M"], 500), ("ち", ["C"], 500),
        ("ん", ["U", "M", "C"], 50), ("こ", ["U", "M", "C"], 100),
        ("お", ["U", "M", "C"], 300), ("-", ["U", "M", "C"], -500))

words = [["うんこ", "U", 1000], ["ちんこ", "C", 1000], ["まんこ", "M", 1000],
         ["うんち", "U", 1000], ["ちんちん", "C", 3000],
         ["おまんこ", "M", 5000], ["おちんちん", "C", 10000]]
words_en = ["UNKO", "CHINKO", "MANKO", "UNCHI",
            "CHINCHIN", "OMANKO", "OCHINCHIN"]
triples = [["う", ["U"], 2], ["ま", ["M"], 2], ["ち", ["C"], 2],
           ["ん", ["U", "M", "C"], -3], ["こ", ["U", "M", "C"], 1.5],
           ["お", ["U", "M", "C"], 1.5]]

scoreTotal = {"U": 0, "M": 0, "C": 0}



def rollDice(number):
    result = ""
    faceScore = {"U": 0, "M": 0, "C": 0}
    for i in range(number):
        roll = dice[random.randrange(1, 7, 1)]
        result += roll[0]
        for j in roll[1]:
            faceScore[j] += roll[2]
    return result, faceScore


def analyseWords(result):
    resultToWord = []
    wordScore = {"U": 0, "M": 0, "C": 0}
    for i in range(len(words)):  # every word in words
        wordLength = 0
        ochinchin = 0
        for j in range(len(words[i][0])):  # every char in word
            c = Counter(result)
            if c["ち"] >= 2 and c["ん"] >= 2:
                ochinchin = 1

            if list(words[i][0])[j] in result:
                wordLength += 1

            # おちんちん
            if wordLength == 5 and i == 6 and ochinchin == 1:
                resultToWord.append(words_en[i])
                wordScore[words[i][1]] += words[i][2]
                break
            # ちんちん
            elif wordLength == 4 and i == 4 and ochinchin == 1:
                resultToWord.append(words_en[i])
                wordScore[words[i][1]] += words[i][2]
                break
            # おまんこ
            elif wordLength == 4 and i == 5:
                resultToWord.append(words_en[i])
                wordScore[words[i][1]] += words[i][2]
                break
            elif wordLength == 3 and i <= 3:
                resultToWord.append(words_en[i])
                wordScore[words[i][1]] += words[i][2]
                break
    return resultToWord, wordScore


def detectTriples(result):
    multiplier = {"U": 1, "M": 1, "C": 1}
    c = Counter(result)
    for triple in triples:
        if c[triple[0]] >= 3:
            for category in triple[1]:
                multiplier[category] *= triple[2]
    return multiplier

numToRoll = 3
numDice = 5
diceResetFlag = 0
lastWords = []

while numToRoll > 0:
    numToRoll -= 1
    if diceResetFlag == 0:
        numDice = 5
        roll = rollDice(numDice)
    else:
        roll = rollDice(number=numDice if numDice <= 10 else 10)
        diceResetFlag = 0
    analysed = analyseWords(roll[0])

    # 出目スコア、役スコアの加算
    for category in roll[1]:
        scoreTotal[category] += roll[1][category]
    for category in analysed[1]:
        scoreTotal[category] += analysed[1][category]
    
    # ぞろ目の乗算
    multi = detectTriples(roll[0])
    for category in multi:
        scoreTotal[category] *= multi[category]

    # 次回のダイス数
    if "OCHINCHIN" in analysed[0]:
        numDice = 10
        diceResetFlag = 1
    elif len(analysed[0]) >= 2:
        numDice += (len(analysed[0]) - 1)
        diceResetFlag = 1

    # ロール数
    if len(analysed[0]) != 0:
        numToRoll += 1
else:
    print(sum(scoreTotal.values()))
