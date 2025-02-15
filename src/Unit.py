class Unit:
    def __init__(self, type, id, *values, name=None):
        self.type = type
        self.id = id
        self.values = [value for value in values]
        self.name = name

    def __str__(self):
        return f"Unit(\"Type\": {self.type}, \"Id\": {self.id}, \"Name\": {self.name},\
 \"Values\": {[value for value in self.values]})"

    def __repr__(self):
        return self.__str__()
