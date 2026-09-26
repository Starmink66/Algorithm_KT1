class TrieNode:
    def __init__(self):
        self.children = {}
        self.flag = False
        self.frequency = 0

class Trie:
    TOP_K = 5
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode()
            current_node = current_node.children[letter]
        current_node.flag = True
        current_node.frequency += 1

    def search(self, prefix):
        current_node = self.root
        for letter in prefix:
            if letter not in current_node.children:
                return None
            current_node = current_node.children[letter]
        return current_node

    def autocomplete(self, prefix):
        start = self.search(prefix)
        if start is None:
            return []
        heap = MinHeap()
        self._big_top(start, prefix, heap, self.TOP_K)
        return [(word, freq) for freq, word in heap.sorted_desc()]

    def _big_top(self, node, prefix, heap, k):
        if node.flag:
            item = (node.frequency, prefix)
            if len(heap) < k:
                heap.insert(item)
            elif item > heap._get_min():
                heap.extract_min(item)
        for ch, child in node.children.items():
            self._big_top(child, prefix + ch, heap, k)

class MinHeap:
    def __init__(self):
        self.arr = []
    def __len__(self):
        return len(self.arr)
    def _left(self, item): return 2 * item +1
    def _right(self, item): return 2 * item + 2
    def _parent(self, item): return ((item - 1)//2)
    def _get_min(self): return self.arr[0]
    def insert(self, num):
        self.arr.append(num)
        self._fall_up(len(self.arr) - 1)

    def extract_min(self, item):
        if not self.arr:
            self.arr.append(item)
            return
        self.arr[0] = item
        self._fall_down(0)

    def sorted_desc(self):
        return sorted(self.arr, reverse=True)

    def _fall_up(self, item):
        while item > 0:
            par = self._parent(item)
            if self.arr[par] <= self.arr[item]:
                break
            self.arr[par], self.arr[item] = self.arr[item], self.arr[par]
            item = par

    def _fall_down(self, item):
        n = len(self.arr)
        while True:
            lt, rt = self._left(item), self._right(item)
            smallest = item
            if lt < n and self.arr[lt] < self.arr[smallest]:
                smallest = lt
            if rt < n and self.arr[rt] < self.arr[smallest]:
                smallest = rt
            if smallest == item:
                break
            self.arr[item], self.arr[smallest] = self.arr[smallest], self.arr[item]
            item = smallest


class Priority_Queue:
    def __init__(self):
        self.arr = []
        self.order = 0

    def __len__(self):
        return len(self.arr)
    def _left(self, item): return 2 * item +1
    def _right(self, item): return 2 * item + 2
    def _parent(self, item): return ((item - 1)//2)
    def _swap(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def _fall_up(self, item):
        while item > 0:
            par = self._parent(item)
            if self.arr[par] <= self.arr[item]:
                break
            self._swap(par, item)
            item = par #зачем нам тут дважды менять? если мы уже использовали swap?

    def _fall_down(self, item):
        n = len(self.arr)
        while True:
            lt, rt = self._left(item), self._right(item)
            smallest = item
            if lt < n and self.arr[lt] < self.arr[smallest]:
                smallest = lt
            if rt < n and self.arr[rt] < self.arr[smallest]:
                smallest = rt
            if smallest == item:
                break
            self.arr[item], self.arr[smallest] = self.arr[smallest], self.arr[item]
            item = smallest

    def enqueue(self, request, priority=0):
        item = (-priority, self.order, request)
        self.order += 1
        self.arr.append(item)
        self._fall_up(len(self.arr)- 1)
    def dequeue(self):
        if not self.arr:
            return None
        top = self.arr[0]
        last = self.arr.pop()
        if self.arr:
            self.arr[0] = last
            self._fall_down(0)
        return top[2]

t = Trie()
for w in ['радость', 'груша', 'чай', 'корабль', 'кофе', 'облако', 'мечта', 'деревня', 'часы', 'улица', 'яхта', 'лук', 'самолет', 'морковь', 'велосипед', 'парк', 'рыба', 'троллейбус', 'туфли', 'снег' , 'человек', 'стол', 'солнце', 'башня', 'друг', 'город','лестница', 'часы','рыба','храм']:
    t.insert(w)

print(t.autocomplete('р'))
print(t.autocomplete('ч'))
print(t.autocomplete('к'))
print(t.autocomplete('о'))
print(t.autocomplete('м'))

pq = Priority_Queue()
pq.enqueue(['рыба', 'радость'], 1)
pq.enqueue(['часы', 'человек', 'чай'], 0)

print('VIP')
print(pq.dequeue())
print('Обычная очередь')
print(pq.dequeue())

