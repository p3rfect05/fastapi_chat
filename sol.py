class Node:
    def __init__(self, val):
        self.val = val
        self.prev = self.next = None


class ListNode:
    def __init__(self, m):
        self.m = m
        self.right = Node(0)
        self.left = Node(0)
        self.left.next = self.right
        self.right.prev = self.left
        self.cache = {}




    def add(self, number):
        if number in self.cache:
            cur = self.cache[number]
            if cur != self.left.next:
                cur.prev.next, cur.next.prev = cur.next, cur.prev
                cur.next, cur.prev = self.left.next, self.left  # вставили слева
                self.left.next, self.left.next.prev = cur, cur  # вставили слева


            #self.cache[number] = cur
        else:
            if len(self.cache) == self.m:
                cur = Node(number) # создаём
                to_delete = self.right.prev.val # удаляемый номер
                #print(self.right.prev, self.cache)
                self.delete(self.right.prev.val) # объект
                self.cache.pop(to_delete) # удаляеем из кэша
                cur.next, cur.prev = self.left.next, self.left  # вставили слева
                self.left.next, self.left.next.prev = cur, cur  # вставили слева
                self.cache[number] = cur # новый номер записывается

            else:
                cur = Node(number)
                cur.next, cur.prev = self.left.next, self.left  # вставили слева
                self.left.next, self.left.next.prev = cur, cur  # вставили слева
                self.cache[number] = cur  # новый номер записывается



n = ListNode(3)
n.add('456')
n.add('789')
n.add('111')
n.add('456')
i = n.left
print(n.left.next.next.next, n.left.next.next.next.next, n.left.next.next.next.next.next)
# while i:
#     print(i.val)
#     i = i.next


