class Node:
    move_type = ""
    distance = 0
    next = None
    def __init__(self, move_type=None, distance=None):
        self.move_type = move_type
        self.distance = distance

class MoveTracker:
    head = Node()
    next_node_distance = 1

    def add(move_type, distance):
        current = MoveTracker.head
        node = Node(move_type, distance)

        while current.next is not None:
            current = current.next

        current.next = node
    
    def print():
        while MoveTracker.head is not None:
            print("mt: ", MoveTracker.head.move_type, " d: ", MoveTracker.head.distance)
            MoveTracker.head = MoveTracker.head.next

    def get_next():
        current = MoveTracker.head
        for x in range(MoveTracker.next_node_distance):
            current = current.next
        MoveTracker.next_node_distance += 1
        return current
            

l = [9, 10, 8, 11, 12, 13, 14]
def remove_index(x, l):
    return l[:x] + [None] + l[x + 1:]

print(remove_index(1, l))