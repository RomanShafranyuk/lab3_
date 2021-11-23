import json


def merge_two_list(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i]["weight"] < b[j]["weight"]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    if i < len(a):
        result += a[i:]
    if j < len(b):
        result += b[j:]
    return result


def merge_sort(s):
    if len(s) == 1:
        return s
    middle = len(s) // 2
    left = merge_sort(s[:middle])
    right = merge_sort(s[middle:])
    return merge_two_list(left, right)


data = json.load(open("result.txt", encoding="windows-1251"))
sorted_data = merge_sort(data)
# print(sorted_data)

json.dump(sorted_data, open("../result_sort.txt", "w", encoding="windows-1251"), ensure_ascii=False, sort_keys=False, indent=4)
check = json.load(open("../result_sort.txt", encoding="windows-1251"))
print(check)

