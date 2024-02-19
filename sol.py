n = int(input())

pts = []
visited = {}
res = n
b_a = {}
for i in range(n):
    a, b = map(int, input().split(' '))
    # if (0, a) in visited or (1, b) in visited:
    #     if (0, a) in visited and visited[(0, a)] == 1:
    #         res -= 2
    #     elif (0, a) in visited:
    #         res -= 1
    #
    #     if (1, b) in visited and visited[(1, b)] == 1:
    #         res -= 2
    #     elif (1, b) in visited:
    #         res -= 1
    #
    # visited[(0, a)] = 1 + visited.get((0, a), 0)
    # visited[(1, b)] = 1 + visited.get((1, b), 0)
    if (1, b) in b_a:
        b_a[(1, b)].append((0, a))
    else:
        b_a[(1, b)] = [(0, a)]
    pts.append([(0, a), (1, b)])


pts.sort()
#print(pts)
#b = [pts[0][1]]
#b_i = 0
b_stack = [pts[0][1]]
max_b = pts[0][1]
i = 1
#print(pts)
count1 = {pts[0][0] : 1}
while i < len(pts):
    #print(b_stack, res)

    cur_b = pts[i][1]
    count1[pts[i][0]] = 1 + count1.get(pts[i][0], 0)
    #print(b_stack, cur_b, max_b)
    if b_stack and cur_b <= b_stack[-1]:
        res -= 1
        while b_stack and cur_b <= b_stack[-1]:
            #max_b = max(max_b, cur_b)
            res -= 1
            b_stack.pop()
    elif not b_stack and cur_b <= max_b:
        res -= 1
    else:
        #print(cur_b)
        b_stack.append(cur_b)
    #print(b_stack, cur_b, max_b)
    max_b = max(max_b, cur_b)
    i += 1
    #print(b_stack, res)


count2 = {}
for b in b_stack:
    for i in b_a[b]:
        count2[i] = 1 + count2.get(i, 0)
for c in count1:
    if c in count2 and count1[c] > 1:
        res -= count2[c]
#print(count1, count2)
#print(b_stack)
print(res)
