import copy
import itertools
import sys
from pprint import pprint as pp
from itertools import combinations #부부집합 구하기 위한 라이브러리

global total_list, min_support
total_list = []
min_support = 0
def find_first_scan(fin, frequent):
    global total_list, min_support

    for line in fin:
        transaction = set()
        arr = line.strip('\n').split('\t')
        for item in arr:
            item = int(eval(item))
            transaction.add(item)
            if item in frequent:
                frequent[item] = frequent.get(item) + 1
            else:
                frequent[item] = 1
        total_list.append(transaction)

    for freq in frequent:
        frequent[freq] = round((frequent[freq]/len(total_list))*100,2)

    new_frequent = {key: value for key, value in frequent.items() if value >= min_support}

    return new_frequent


def frequent_count_and_support(list):
    global total_list
    new_frequent = {}
    for total_row in total_list:
        for list_item in list:
            list_set = set(list_item)
            if list_set.issubset(total_row):
                make_tuple = tuple(list_set)
                if make_tuple in new_frequent: #튜플 형태로 new_frequent에 넣기
                    new_frequent[make_tuple] = new_frequent[make_tuple] + 1
                else:
                    new_frequent[make_tuple] = 1

    for freq in new_frequent:
        num = new_frequent[freq]/len(total_list)*100
        new_frequent[freq] = round(num,2)

    change_frequent = {key: value for key, value in new_frequent.items() if value >= min_support}

    if len(change_frequent) < 0:
        exit()
    return change_frequent

def join_and_pruning(frequent, order):
    new_frequent_list = []
    list_key = []
    for i in frequent.keys():
        if isinstance(i, tuple):
            i = set(i)
        list_key.append(i)

    #print(list_key)
    for j in range(len(list_key) - 1):
        for k in range(j + 1, len(list_key)):
            set_keys1 = list_key[j]
            set_keys2 = list_key[k]
            if isinstance(set_keys1, int):

                tmp = set()
                tmp.add(list_key[j])
                set_keys1 = tmp
                tmp2 = set()
                tmp2.add(list_key[k])
                set_keys2 = tmp2
            else:  # order가 2일때 한개씩 합치는것
                set_keys1 = set(list_key[j])
                set_keys2 = set(list_key[k])

            union = set_keys1.union(set_keys2)
            subset_list = list(combinations(union, order))
            for l in subset_list:
                change_set = set(l)
                cnt = 0
                for key_set in list_key:
                    if isinstance(key_set, int):
                        temp = set()
                        temp.add(key_set)
                        key_set = temp
                    if key_set.issubset(change_set):
                        cnt += 1
                        if cnt == order and change_set not in new_frequent_list:
                            new_frequent_list.append(change_set)
                            break

    return new_frequent_list

def association_rule(frequent, order, fout):
    copy_order = order
    frequent_list = list(frequent.keys())

    while copy_order > 1 :
        for list_item in frequent_list:
            comb = list(itertools.combinations(set(list_item),copy_order-1))
            for comb_item in comb:
                diff = set(list_item) - set(comb_item)
                count = 0
                for total_item in total_list:
                    if set(comb_item).issubset(set(total_item)):
                        count+= 1
                freq = frequent.get(list_item) / 100 * len(total_list)
                fout.write(str(set(comb_item)) +'\t' + str(diff) + '\t' + str('%.2f' % round(frequent[list_item],2)) + '\t' +  str('%.2f' % round(freq/count*100,2)) + '\n')
        copy_order -= 1

def main():
    global min_support

    if len(sys.argv) == 4:
        min_support = int(sys.argv[1])
        fin = open(sys.argv[2], "r")
        fout = open(sys.argv[3], "w")
    else:
        print("다시 입력하세요.")
        exit()
    frequent = {}
    frequent = find_first_scan(fin, frequent)

    order = 2
    while True:
        list = join_and_pruning(frequent,order)
        if len(list) == 0:
            print("finish")
            break

        frequent = frequent_count_and_support(list)
        association_rule(frequent, order, fout)
        order += 1
    fin.close()
    fout.close()

if __name__== "__main__":
    main()