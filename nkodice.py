import random
from collections import Counter

dice = ("う", "お", "こ", "ち", "ま", "ん")

words = ["うんこ", "ちんこ", "まんこ", "うんち",
         "ちんちん", "おまんこ", "おちんちん"]
words_en = ["UNKO", "CHINKO", "MANKO", "UNCHI",
            "CHINCHIN", "OMANKO", "OCHINCHIN"]


def rollDice(number):
    result = ""
    for i in range(number):
        result += dice[random.randrange(1, 6, 1)]
    return result


def analyseDice(result):
    resultToWord = []
    for i in range(len(words)):  # every word in words
        point = 0
        ochinchin = 0
        for j in range(len(words[i])):  # every char in word
            c = Counter(result)
            if c["ち"] >= 2 and c["ん"] >= 2:
                ochinchin = 1

            if list(words[i])[j] in result:
                point += 1

            if point == 5 and i == 6 and ochinchin == 1:
                resultToWord.append(words_en[i])
                break
            elif point == 4 and i == 4 and ochinchin == 1:
                resultToWord.append(words_en[i])
                break
            elif point == 4 and i == 5:
                resultToWord.append(words_en[i])
                break
            elif point == 3 and i <= 3:
                resultToWord.append(words_en[i])
                break
    return resultToWord


for i in range(10):
    sixDice = rollDice(6)
    print(f"{sixDice}: {analyseDice(sixDice)}")
