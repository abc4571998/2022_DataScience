import math
import copy

global attribute
def main():
    global attribute
    fin = open('data-2/dt_train1.txt', 'r')
    fin_test = open('data-2/dt_test1.txt', 'r')
    fout = open('result1.txt','w')
    attribute = [] #attribute name 저장하기
    attribute_value = [] #attribute 값들 저장하기  dictionary 형태로
    train_data = [] #train_data 저장하기

    for row in fin:
        if not attribute:
            attribute = row.split() #처음에 attribute name 넣을 거야
            for j in range(len(attribute)):
                attribute_value.append({}) #dictionary 만들어주기
            continue
        list_row = row.split() #train data 하나 읽어서 split 리스트로 저장하기
        train_data.append(list_row) #전체 train_data 리스트에 붙여넣기
        for i in range(len(list_row)): #data에서 i번째 attribute value는 i번째 attribute value 리스트 안에 있는 딕셔너리에 넣기
            if list_row[i] in attribute_value[i]:
                attribute_value[i][list_row[i]] += 1
            else:
                attribute_value[i][list_row[i]] = 1

    # 여기까지 하면 attribute_value는 0번째 배열에는 0번 attribute의 value와 그 수가 딕셔너리 형태로 들어감

    tmp = [label_ for label_ in attribute_value[-1].values()] #attribute value에서 맨 뒤가 label 이기 때문에 label의 개수들을 가져온다.
    info = cal_info(tmp) # info 구하기 ex) [9,5] 형태로 들어감
    gain = cal_gain_ratio(info, attribute_value, train_data) #gain ratio 구하기

    remove_index = gain.index(max(gain)) #선택할 attribute 이다. ex) buying이면 remove_index = 0

    #######여기까지 하면 처음 나눌 attribute를 뽑은 것이다.

    decision_tree = []
    for a in range(len(attribute)):
        decision_tree.append({})

    #split_attribute_list는 attribute 선택하고 나서 쪼개지는 value가 되는데,
    #예를 들어 buying을 뽑았다면 list에는 low, med, high가 들어간다.

    split_attribute_list = [k for k in attribute_value[gain.index(max(gain))]]
    #attribute에 따라 쪼갠 애들의 training data 만을 따로 보여줄 split_train_data
    split_train_data = []

    #low, med, high 돌아보는 for문
    for sp in split_attribute_list:
        split_node = []
        for td in train_data: #train data를 돌면서 low 에 해당하는 data들만 뽑아낼 for문
            if sp in td[remove_index]: #td[remove_index] 는 buying attribute의 값인데, low로 나누려는데 값이 low라면 이 data를 저장해준다.
                split_node.append(td)
        split_train_data.append(split_node)
    ####여기까지 첫 attribute로 나누었을 때 쪼개지는 attribute value와 그에 해당하는 data 들을 나누었다.

    path = []
    total_path = []
    make_decision_tree(split_attribute_list, split_train_data, remove_index, attribute, decision_tree, path, total_path)

    attribute_check = False
    label_success = False
    check = False
    for test_row in fin_test:
        test_data = test_row.strip('\n').split('\t')
        if not attribute_check:
            test_data = copy.deepcopy(attribute)
            test_data.append('\n')
            fout.writelines('\t'.join(test_data))
            attribute_check = True
            continue
        max_len = 0
        for path_row in total_path:
            count = 0
            for path_element in path_row:
                count += 1
                if path_element[0] == attribute[-1]:
                    test_data.append(path_element[1])
                    test_data = '\t'.join(test_data)
                    fout.write(test_data+'\n')
                    label_success = True
                if test_data[attribute.index(path_element[0])] != path_element[1]:
                    if max_len<count:
                        max_len = count
                    break
            if label_success:
                label_success = False
                check = True
                break
        if not check:
            tmp_label = {}
            #max_len = 3
            for p_row in total_path:
                for p in range(max_len-1):
                    if test_data[attribute.index(p_row[p][0])] != p_row[p][1]:
                        break
                    if p == max_len-2:
                        if p_row[-1][1] in tmp_label:
                            tmp_label[p_row[-1][1]] += 1
                        else:
                            tmp_label[p_row[-1][1]] = 1
            max_value = [t for t,v in tmp_label.items() if max(tmp_label.values()) == v]
            test_data.append(str(max_value[-1]))
            test_data = '\t'.join(test_data)
            fout.write(test_data + '\n')
        check = False
    fin.close()
    fin_test.close()
    fout.close()

def test_decision_tree(decision_tree, test_data, root):
    go = root
    while True:
        next_attr = decision_tree[go].get(test_data[go])
        if type(next_attr) == int:
            go = next_attr
        else:
            label = next_attr
            return label


def make_decision_tree(split_attribute_list, split_train_data, remove_index, attribute_, decision_tree , path, total_path):
    remove_attr = attribute_[remove_index] #선택한 attribute의 이름 ex)maint

    for sp_dt in range(len(split_attribute_list)):
        path_copy = copy.deepcopy(path)
        copy_train_data = cal_train_data(split_train_data[sp_dt], remove_index)
        copy_attribute = cal_attribute(attribute_, remove_index)
        copy_attribute_value = cal_attribute_value(copy_train_data, len(copy_attribute))
        label_count = find_label_count(copy_train_data)

        if cal_info(label_count) == 0:
            label = list(copy_attribute_value[-1].keys())
            decision_tree[attribute.index(remove_attr)][split_attribute_list[sp_dt]] = label[0]
            path = copy.deepcopy(path)
            path.append((remove_attr, split_attribute_list[sp_dt]))
            path.append((attribute[-1], label[0]))
            total_path.append(path)
            path = path_copy
        elif len(copy_attribute)-1 == 0:
            path = copy.deepcopy(path)
            path.append((remove_attr, split_attribute_list[sp_dt]))
            path.append((attribute[-1], max(copy_attribute_value[0], key=copy_attribute_value[0].get)))
            total_path.append(path)
            path = path_copy
        elif len(copy_train_data) == 0:
            print("train data is 0")
            break
        else:
            tmp_ = [label_ for label_ in copy_attribute_value[-1].values()]
            info_ = cal_info(tmp_)
            gain_ = cal_gain_ratio(info_, copy_attribute_value, copy_train_data)
            if len(gain_) == 0:
                break
            remove_index_ = gain_.index(max(gain_))
            split_attribute_list_ = [k for k in copy_attribute_value[remove_index_]]
            split_train_data_ = []
            for sp in split_attribute_list_:
                split_node_ = []
                for td in copy_train_data:
                    if sp in td[remove_index_]:
                        split_node_.append(td)
                split_train_data_.append(split_node_)
            decision_tree[attribute.index(remove_attr)][split_attribute_list[sp_dt]] = attribute.index(copy_attribute[remove_index_])

            path.append((remove_attr, split_attribute_list[sp_dt]))
            make_decision_tree(split_attribute_list_, split_train_data_, remove_index_, copy_attribute, decision_tree, path, total_path)
            path = path_copy

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
    for td in train_data:
        for j in range(len(td)):
            if td[j] in attr_value[j]:
                attr_value[j][td[j]] += 1
            else:
                attr_value[j][td[j]] = 1
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

