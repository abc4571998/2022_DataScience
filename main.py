from pprint import pprint as pp

def find_first_scan(fin):
    first_scan = {}
    sum = 0
    for line in fin:
        arr = line.strip('\n').split('\t')
        for item in arr:
            if item in first_scan:
                first_scan[item] = first_scan.get(item) + 1
            else:
                first_scan[item] = 1
            sum += 1
    pp(first_scan)
    return first_scan

def cal_support(scan, min_support):
    sum = 0
    for i in scan.values():
        sum += i

    for j in scan.keys():
        scan[j] = (scan[j]/sum)*100

    pp(scan)
    if scan[j] < min_support:
        del(scan[j])

    pp(scan)

def main():
    fin = open('input.txt', "r")
    fout = open('output.txt', "w")

    mim_support = 5

    first_scan = find_first_scan(fin)
    cal_support(first_scan,mim_support)
    fin.close()
    fout.close()

if __name__== "__main__":
    main()