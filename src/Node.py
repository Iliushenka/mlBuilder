from TokensNode import TokensNode


class Node:
    def __init__(self, type, value1=None, value2=None, other=None, id=TokensNode.ACTION, values=None):
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.other = other
        self.my_name = None
        self.id = id
        self.values = values

    def __str__(self):
        return f"Node({self.type}: {self.value1}, {self.value2}, {self.other})"

    def __repr__(self):
        return self.__str__()
