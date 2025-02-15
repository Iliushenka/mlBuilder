class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def assign(self, *types):
        for type in types:
            if self.type == type:
                return True
        return False

    def __str__(self):
        return f"Token({self.type}: {self.value})"

    def __repr__(self):
        return self.__str__()