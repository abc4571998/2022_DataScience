import math
import copy
global attribute
def main():
    global attribute
    print('Hi')  # Press ⌘F8 to toggle the breakpoint.
    fin = open('data-2/dt_train1.txt', 'r')
    fin_test = open('data-2/dt_test1.txt', 'r')
    fout = open('output.txt','w')
    attribute = []
    attribute_value = []
    train_data = []
    total_data_count = 0

    for row in fin:
        if not attribute:
            attribute = row.split()
            for j in range(len(attribute)):
                attribute_value.append({})
            continue
       #print("value ", attribute_value)
        list_row = row.split()
        train_data.append(list_row)
        for i in range(len(list_row)):
            if list_row[i] in attribute_value[i]:
                attribute_value[i][list_row[i]] += 1
            else:
                attribute_value[i][list_row[i]] = 1
        total_data_count += 1

    print(attribute)
    print(attribute_value)

    tmp = [label_ for label_ in attribute_value[-1].values()]
    info = cal_info(tmp)
    gain = cal_gain_ratio(info, attribute_value, train_data)

    remove_index = gain.index(max(gain))
    print("split attribute is ", attribute[remove_index])
    root = remove_index

    decision_tree = []
    for a in range(len(attribute)):
        decision_tree.append({})

    split_attribute_list = [k for k in attribute_value[gain.index(max(gain))]]
    split_train_data = []
    for sp in split_attribute_list:
        split_node = []
        for td in train_data:
            if sp in td[remove_index]:
                split_node.append(td)
        split_train_data.append(split_node)

    make_decision_tree(split_attribute_list, split_train_data, remove_index, attribute, decision_tree)

        #print(cal_gain_ratio(info, copy_attribute_value, split_train_data[sp_dt]))

    attribute_check = False
    for test_row in fin_test:
        test_data = test_row.strip('\n').split('\t')
        if not attribute_check:
            test_data = copy.deepcopy(attribute)
            test_data.append('\n')
            fout.writelines('\t'.join(test_data))
            attribute_check = True
            continue
        label = test_decision_tree(decision_tree,test_data, root)
        test_data.append(label)
        test_data.append('\n')
        print("test data", test_data)
        fout.writelines('\t'.join(test_data))

    fin.close()
    fin_test.close()
    fout.close()


def test_decision_tree(decision_tree, test_data, root):
    go = root
    while True:
        next_attr = decision_tree[go].get(test_data[go])
        if type(next_attr) == int:
            print("go", next_attr)
            go = next_attr
        else:
            label = next_attr
            print("label", label)
            return label


def make_decision_tree(split_attribute_list, split_train_data, remove_index, attribute_, decision_tree ):

    remove_attr = attribute_[remove_index]
    attribute.index(remove_attr)
    for sp_dt in range(len(split_attribute_list)):
        print("hh", remove_attr, attribute.index(remove_attr), split_attribute_list, sp_dt)
        copy_train_data = cal_train_data(split_train_data[sp_dt], remove_index)
        copy_attribute = cal_attribute(attribute_, remove_index)
        copy_attribute_value = cal_attribute_value(copy_train_data, len(copy_attribute))
        print("sp_dt", sp_dt)
        print("attribute ",copy_attribute)
        #print("copy attribute value ", copy_attribute_value)
        label_count = find_label_count(copy_train_data)
        if cal_info(label_count) == 0:
            label = list(copy_attribute_value[-1].keys())
            print("this is 0",label, sp_dt)
            decision_tree[attribute.index(remove_attr)][split_attribute_list[sp_dt]] = label[0]
        elif len(copy_attribute)-1 == 0:
            print("length is 0")
        elif len(copy_train_data) == 0:
            print("train data is 0")
        else:
            print("else")
            tmp_ = [label_ for label_ in copy_attribute_value[-1].values()]
            info_ = cal_info(tmp_)
            gain_ = cal_gain_ratio(info_, copy_attribute_value, copy_train_data)
            print(tmp_)
            print(info_)
            print(gain_)
            if len(gain_) == 0:
                print("******info", info_)
                print(gain_)
                print(copy_attribute_value)
                break
            remove_index_ = gain_.index(max(gain_))
            #print("@@@split attribute is ", copy_attribute[remove_index_], attribute_.index(copy_attribute[remove_index_]))
            split_attribute_list_ = [k for k in copy_attribute_value[remove_index_]]
            split_train_data_ = []
            for sp in split_attribute_list_:
                split_node_ = []
                for td in copy_train_data:
                    if sp in td[remove_index_]:
                        split_node_.append(td)
                split_train_data_.append(split_node_)
            #print("#split_attribute_list : ", split_attribute_list_)
            #print("#split_train_data: ", split_train_data_, attribute, remove_attr, attribute.index(remove_attr))
            decision_tree[attribute.index(remove_attr)][split_attribute_list[sp_dt]] = attribute.index(copy_attribute[remove_index_])
            make_decision_tree(split_attribute_list_, split_train_data_, remove_index_, copy_attribute, decision_tree)
        print("decision tree", decision_tree)

def cal_train_data(train_data, remove):
    copy_train_data = copy.deepcopy(train_data)
    for i in copy_train_data:
        del i[remove]
    return copy_train_data

def cal_attribute(attribute, remove):
    copy_attribute = copy.deepcopy(attribute)
    del(copy_attribute[remove])
    return copy_attribute

def cal_attribute_value(train_data, attribute_count):
    attr_value = []
    for i in range(attribute_count):
        attr_value.append({})
    #print(train_data)
    for td in train_data:
        for j in range(len(td)):
            if td[j] in attr_value[j]:
                attr_value[j][td[j]] += 1
            else:
                attr_value[j][td[j]] = 1
    #print("print attribute value :", attr_value)
    return attr_value

def find_label_count(split_list):
    label_count = {}
    for sl in split_list:
        if sl[-1] in label_count:
            label_count[sl[-1]] += 1
        else:
            label_count[sl[-1]] = 1
    return [l for l in label_count.values()]

def cal_gain_ratio(info, attribute_value, train_data):
    gain = [] #모든 attribute의 gain을 구하기 위한 list
    gain_ratio = [] #gain ratio 구하기 위한 list
    for c in range(len(attribute_value) - 1): #class label 빼고 attribute 돌기
        info_a = 0 #나누어질 attribute
        sum_of_attribute_value = sum(attribute_value[c].values())
        gain_split = []
        gain_split_of_attribute = 0
        for key, value in attribute_value[c].items(): #각 attribute의 dictionary 꺼내기
            p = value / sum_of_attribute_value #Dj/D 구하기
            info_l = [] #attribute 범위안에서 label을 구하는 것
            gain_split_of_attribute -= p*math.log2(p)
            for label_key in attribute_value[-1].keys(): #class label을 볼건데
                count = 0
                for data_row in train_data: #뽑은 class label 과 train_data에 있는 row들을 하나씩 비교할거야
                    if key == data_row[c] and label_key == data_row[-1]: #일단 뽑은 attribute의 범위(?)가 같고, label 이 같다면 count 증가하자
                        count += 1
                info_l.append(count)
            info_a += p*cal_info(info_l) #범위에 맞는 label을 구한 걸로 info_a 에 더해주기
        gain_split.append(round(gain_split_of_attribute,3))
        info_a = round(info_a,3)
        gain.append(round(info-info_a,3))
        gain_ratio.append(round(round(info-info_a,3)/round(gain_split_of_attribute,3),3))
    print("gain ratio", gain_ratio)
    return gain_ratio

def cal_info(num_list):
    total_num = sum(num_list)
    if total_num == 0:
        return 0
    info = 0
    for num in num_list:
        if num == 0:
            info -= 0
        else:
            p = num / total_num
            info -= p*math.log2(p)
    return round(info,3)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
