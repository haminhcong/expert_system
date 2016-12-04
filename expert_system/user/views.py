xxx = '4|-0.6^5|3'
arr = []
i = 0
while i < len(xxx):
    if xxx[i] == '-':
        num = '-'
        j = i + 1
        while j < len(xxx):
            if xxx[j] != '|' and xxx[j] != '^':
                num += xxx[j]
                j += 1
            else:
                break
        arr.append(float(num))
        i = j
    elif xxx[i].isdigit():
        arr.append(int(xxx[i]))
        i += 1
    else:
        arr.append(xxx[i])
        i += 1
print arr

result = 0
while len(arr) > 1:
    try:
        index = arr.index('|')
        print index
        if index > 0:
            temp = max(arr[index - 1], arr[index + 1])
            # print type(temp)
            arr = arr[:index - 1] + [temp] + arr[index + 2:]
        index = arr.index('^')
        print index
        if index > 0:
            temp = min(arr[index - 1], arr[index + 1])
            arr = arr[:index - 1] + [temp] + arr[index + 2:]
    except Exception:
        arr = arr
print arr
