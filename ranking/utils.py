from collections import Iterable
import re

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:
             yield item

def returnNum(current_answer, comp_type):
    numbers = []
    if comp_type == 'more_than' or comp_type == 'less_than':
        word_list = [num.strip() for num in current_answer.split('than')]
    elif comp_type == 'to':
        word_list = [num.strip() for num in current_answer.split('to')]
    for word in word_list:
        alnums = re.findall("\d", word)
        if word.isnumeric():
            if float(word) not in numbers:
                numbers.append(int(float(word)))
        elif alnums:
            word_list1 = [num.strip() for num in current_answer.split(' ')]
            for word1 in word_list1:
                if word1.isnumeric():
                    if float(word1) not in numbers:
                        numbers.append(int(float(word1)))
                elif '0.' in word1:
                    if float(word1) not in numbers:
                        numbers.append((float(word1))) 
    return numbers