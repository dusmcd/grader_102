class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def enqueue(self, val):
        node = Node(val)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.count += 1

    def dequeue(self):
        if self.head is None:
            return None

        val = self.head.val
        self.head = self.head.next
        self.count -= 1
        return val

    def peek(self):
        return self.head.val if self.head is not None else None

