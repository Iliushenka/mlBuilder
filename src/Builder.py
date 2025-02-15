import json


from Unit import Unit
from Node import Node
from Lang import Lang
from Token import Token
from TokensNode import TokensNode
from TokensLexer import TokensLexer


class Builder:
    def __init__(self, init_node: Node, filename: str, lang: Lang):
        self.initNode = init_node
        self.filename = filename
        self.lang = lang

        self.indexName = 0

    def flatting(self):
        place = list()
        stack = [self.initNode]
        while len(stack) > 0:
            node = stack[-1]
            if node is None:
                stack.pop()
                continue
            if node.type not in self.lang.type[self.lang.basis[TokensNode.EVENT]].values():
                if isinstance(node.value1, Node):
                    stack.append(node.value1)
                    name = Token(TokensLexer.VARIABLE, self.nextName())
                    node.value1.my_name = name
                    node.value1 = name
                    continue
                if isinstance(node.value2, Node):
                    stack.append(node.value2)
                    name = Token(TokensLexer.VARIABLE, self.nextName())
                    node.value2.my_name = name
                    node.value2 = name
                    continue
                if node.my_name is None:
                    node.my_name = Token(TokensLexer.VARIABLE, self.nextName())
            else:
                stack.pop()
                stack.append(node.other)
                stack.append(Node(TokensNode.CLOSE_LINE))
                if node.value1 is not None:
                    stack.append(node.value1)
                node.other = None
                node.value1 = None
                stack.append("NONE")
            values = list()
            if node.value1 is not None:
                values.append(node.value1)
            if node.value2 is not None:
                values.append(node.value2)
            if node.values is not None:
                for value in node.values:
                    values.append(value)
            place.append(Unit(node.type, node.id, *values, name=node.my_name))
            stack.pop()
            if isinstance(node.other, Node):
                stack.append(node.other)
        return place

    def takeName(self, relative_index):
        index = self.indexName + relative_index
        name = f"{self.filename}{index}"
        return name

    def nextName(self):
        self.indexName += 1
        return self.takeName(0)

    def optimization(self):
        place = self.flatting()
        # for pos in place:
        #     print(pos)
        table = dict()
        reduced = list()
        lastAction = None
        for index, unit in enumerate(place):
            if unit.type == TokensNode.BOF:
                continue
            if unit.type == TokensNode.CLOSE_LINE:
                reduced.append(unit)
                continue
            if unit.id == TokensNode.VALUE and unit.type == TokensLexer.PARENT:
                if unit.values[0] in table.keys():
                    table[unit.name] = table[unit.values[0]]
                lastAction = unit.type
                continue
            if unit.id == TokensNode.VALUE:
                # print(unit.values)
                table[unit.name] = unit.values[0]
            if unit.id == TokensNode.ACTION:
                for key, valueName in enumerate(unit.values):
                    if valueName in table.keys():
                        # print(table[valueName])
                        # print(unit.values[key])
                        unit.values[key] = table[valueName]
                        # print(unit)
                if unit.type != "SET_VARIABLE":
                    if lastAction != unit.type:
                        reduced.append(unit)
                    elif (lastAction == unit.type and unit.type in
                          self.lang.type[self.lang.basis[TokensNode.SET_VARIABLE]].values()):
                        reduced[-1].values = unit.values + reduced[-1].values
                        reduced[-1].name = unit.name
                    else:
                        reduced.append(unit)
                else:
                    nameVar = unit.values[0]
                    unit.name = nameVar
                    unit.values = unit.values[1:]
                    if len(unit.values) == 1 and unit.values[0].type == TokensLexer.VARIABLE:
                        reduced[-1].name = unit.name
                    else:
                        reduced.append(unit)
                lastAction = unit.type
                # print(unit.name)
                table[unit.name] = unit.name
        return reduced

    def generation(self):
        reduced = self.optimization()
        lines = list()
        line = list()
        for index, unit in enumerate(reduced):
            if unit.type == TokensNode.CLOSE_LINE:
                lines.append(line)
                line = list()
                continue
            if unit.name is not None and unit.name in self.lang.type[self.lang.basis[TokensNode.SET_VARIABLE]].values():
                unit.values = [unit.name] + unit.values
            block = self.lang.block[unit.type]
            path = self.lang.path[unit.type]
            line += [[
                ["block", block],
                ["path", path]
            ]]
            if len(unit.values) > 0:
                values = ["values"]
                for value in unit.values:
                    values.append({
                        "type": value.type,
                        "value": value.value,
                        "save": False
                    })
                line[-1].append(values)
        else:
            if len(line) > 0:
                lines.append(line)
        filename = self.filename + ".json"
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(lines, file, indent=2,ensure_ascii=False)
        return reduced
    