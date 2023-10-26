class Node:

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        prev = self.prev.value if self.prev is not None else None
        next = self.next.value if self.next is not None else None
        return f"Node: {self.value} Prev: {prev} Next: {next}"

def make_linked_list(list):
    previous = None
    list_map = []
    for x in list:
        node = Node(x)
        list_map.append(node)
        if previous is not None:
            previous.next = node
        node.prev = previous
        previous = node
    first, last = list_map[0], list_map[-1]
    first.prev = last
    last.next = first
    return list_map

def traverse_left(node, amount):
    while amount > 0:
        if node.prev is None:
            break
        node = node.prev
        amount -= 1
    return node

def traverse_right(node, amount):
    while amount > 0:
        if node.next is None:
            break
        node = node.next
        amount -= 1
    return node

def traverse_until(node, condition):
    while not condition(node):
        node = node.next
    return node

def remove_node(node):
    prev = node.prev
    next = node.next
    if prev is not None:
        prev.next = next
    if next is not None:
        next.prev = prev
    node.next = None
    node.prev = None
    return node

def insert_node_after(current, new):
    next = current.next
    if next is not None:
        next.prev = new
    current.next = new
    new.prev = current
    new.next = next

def insert_node_before(current, new):
    prev = current.prev
    if prev is not None:
        prev.next = new
    current.prev = new
    new.prev = prev
    new.next = current

def shift_value(list_map, index):
    node = list_map[index]
    shift_val = node.value
    if shift_val == 0:
        return
    if shift_val < 0:
        insert_node = traverse_left(node, abs(shift_val)+1)
    else:
        insert_node = traverse_right(node, shift_val)
    #print(f"Insert Node: {insert_node}")
    remove_node(node)
    insert_node_after(insert_node, node)

def serialize(node):
    current = node.next
    values = [node.value]
    while current != node:
        values.append(current.value)
        current = current.next
    return values

def process_nodes(array):
    list_map = make_linked_list(array)
    start = traverse_until(list_map[0], lambda x: x.value == 0)
    print(serialize(start))
    for i in range(len(arr)):
        shift_value(list_map, i)
    positions = [1000, 2000, 3000]
    values = list(map(lambda p: traverse_right(start, p).value, positions))
    print(serialize(start))
    print(values)
    return sum(values)

arr = []
with open("input.txt", "rb") as file:
    for line in file:
        arr.append(int(line.decode("utf-8")[:-1]))

print(process_nodes(arr))
