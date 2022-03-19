import copy
from pprint import pprint as pp
from itertools import combinations #부부집합 구하기 위한 라이브러리

def find_first_scan(fin):
    first_scan = {}
    total_list = []
    for line in fin:
        transaction = set()
        arr = line.strip('\n').split('\t')
        for item in arr:
            transaction.add(item)
            if item in first_scan:
                first_scan[item] = first_scan.get(item) + 1
            else:
                first_scan[item] = 1
        total_list.append(transaction)
    print("###total list", total_list)
    pp("print", first_scan)
    return first_scan

def cal_support(scan, row_count, min_support):

    for i in scan:
        scan[i] = (scan[i]/row_count)*100
    del_scan = []
    del_list = []
    for j in scan.keys():
        if scan[j] < min_support:
            del_scan.append(j)
            del_list.append(set(j))

    for del_key in del_scan:
        del(scan[del_key])
    pp(scan)

    print("del scan : ", del_list)
    return del_list

def cal_union(scan, del_scan, order):
    list_key = []
    for i in scan.keys():
        list_key.append(i)
    print(list_key)

    new_scans = {}
    del_scan_update = []
    new_union_list = []
    for j in range(len(list_key)-1):
        for k in range(j+1, len(list_key)):
            set_keys1 = set(list_key[j])
            set_keys2 = set(list_key[k])
            #print("set key", set_keys1, set_keys2)
            ss = set_keys1.union(set_keys2)
            if len(ss) > order: #order이 현재 각 set의 원소의 개수를 말한다. 더 많으면 order개로 쪼개야한다.
                tmp_list = list(combinations(ss, order))
                print("larger than order ", ss)
                print("tmp_list ", tmp_list)
                for tmp in tmp_list:
                    new_union_list.append(set(tmp))
            #print(ss) #합집합 잘 되었음
            else :
                new_union_list.append(set(ss))
    return new_union_list

def prunning_set(new_union_list, del_set, order):

    prunning_union = set()
    prunning_list = []
    after_prunning_list = []
    print("rrrrppruning set new ", new_union_list, del_set)
    for i in range(len(new_union_list)):
        for l in range(len(del_set)):
            if del_set[l].issubset(new_union_list[i]):
                print("issubset ", del_set[l])
                break
            else:
                if l == len(del_set)-1:
                    print("here", new_union_list[i])
                    prunning_list.append(new_union_list[i])

    print("after prunning ", prunning_list)


            #sub_list = set(combinations(new_union_list[i], order-1)) #한 행씩 부분집합을 만들어서 del_set인 것이 있는지 확인
            # for l in range(len(sub_list)):
            #     for ll in range(len(del_set[ll])):
            #         if del_set[ll]
            # if sub_list.issubset(new_union_list[i]):
            #     continue
            # else:
            #     prunning_list.append(new_union_list[i])

    tmp_list = copy.deepcopy(prunning_list)
    count = 0
    for j in range(len(tmp_list)):
        for k in range(len(prunning_list)):
            if len(tmp_list[j].intersection(prunning_list[k])) == order:
                #print("len tmp", len(tmp_list[j].intersection(prunning_list[k])))
                count += 1
                if count >= 2:
                    del prunning_list[k]
                    break
        count = 0
    # set->list->set
    print("prunning ", prunning_list)
    return prunning_list


def count_in_total(total_list, new_union_list):
    new_scan = {}
    for i in range(len(total_list)):
        for j in range(len(new_union_list)):
            if new_union_list[j].issubset(total_list[i]):
                tmp = tuple(new_union_list[j])
                if tmp in new_scan:
                    new_scan[tmp] = new_scan.get(tmp) + 1
                else:
                    new_scan[tmp] = 1
    return new_scan
def main():
    fin = open('input.txt', "r")
    fout = open('output.txt', "w")

    min_support = 50
    row_count = 0

    first_scan = {}
    total_list = []
    for line in fin:
        transaction = set()
        arr = line.strip('\n').split('\t')
        for item in arr:
            transaction.add(item)
            if item in first_scan:
                first_scan[item] = first_scan.get(item) + 1
            else:
                first_scan[item] = 1
        row_count += 1
        total_list.append(transaction)
    pp(first_scan)

    del_scan = cal_support(first_scan, row_count, min_support)

    new_scan = copy.deepcopy(first_scan)
    order = 1
    while True:
        order += 1
        length = len(new_scan)
        if length == 0:
            print("length is 0")
            break
        elif length == 1:
            print("answer is ", new_scan)
            break
        new_union_list = cal_union(new_scan, del_scan, order)
        new_scan = count_in_total(total_list, prunning_set(new_union_list,del_scan,order))
        pp(new_scan)
        del_scan = cal_support(new_scan, row_count, min_support)


    fin.close()
    fout.close()

if __name__== "__main__":
    main()