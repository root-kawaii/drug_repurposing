class Triple:
    head = None
    tail = None
    relation = None

    def __init__(self, head, relation, tail):
        self.head = head
        self.tail = tail
        self.relation = relation

    def __str__(self):
        return str(self.head) + "\t" + str(self.relation) + "\t" + str(self.tail)

