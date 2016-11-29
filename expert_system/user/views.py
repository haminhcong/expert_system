xxx = '4|-0.6^5|3'
arr = []
i =0
while i<len(xxx):
    if xxx[i] =='-':
        num = '-'
        j = i+1
        while j<len(xxx):
            if xxx[j] != '|' and xxx[j] != '^':
                num += xxx[j]
                j +=1
            else:
                break
        arr.append(float(num))
        i = j
    elif xxx[i].isdigit():
        arr.append(int(xxx[i]))
        i +=1
    else:
        arr.append(xxx[i])
        i +=1

result = 0
for x in range(0,len(arr)):
    # print x
    if arr[x] == '|':
        result = max(arr[x-1],arr[x+1])
        print result
    elif arr[x] == '^':
        result = min(arr[x-1],arr[x+1])
        print result

print arr