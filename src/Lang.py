import json


class Lang:
    def __init__(self, path):
        self.file = json.load(open(path, "r", encoding="UTF-8"))

        self.basis = dict()

        self.initBasis()

        self.type = dict()
        self.path = dict()
        self.block = dict()

        self.objects = dict()

        self.initObjects()

        self.setup("EVENT", "minecraft:diamond_block")
        self.setup("PLAYER_ACTION", "minecraft:cobblestone")
        self.setup("SET_VARIABLE", "minecraft:iron_block")
        self.setup("GAME_ACTION", "minecraft:nether_bricks")
        self.setup("ARRAY_ACTION", "minecraft:bookshelf")
        self.setup("IF_GAME", "minecraft:red_nether_bricks")
        self.setup("IF_VARIABLE", "minecraft:obsidian")
        self.setup("IF_ENTITY", "minecraft:bricks")
        self.setup("IF_PLAYER", "minecraft:oak_planks")
        self.setup("SELECT_OBJECT", "minecraft:purpur_block")

    def initBasis(self):
        for value in self.file["BASIS"]:
            self.basis[value["name"]] = value["customName"]

    def initObjects(self):
        for value in self.file["OBJECTS"]:
            self.objects[value["customName"]] = value["name"]

    def setup(self, type, block):
        custom_name = self.basis[type]

        self.type[custom_name] = dict()
        self.path[custom_name] = dict()
        for value in self.file[type]:
            self.type[custom_name][value["customName"]] = value["name"]
            self.path[value["name"]] = value["path"]
            self.block[value["name"]] = block

    def getType(self, value1, value2):
        if value1 in self.type.keys():
            if value2 in self.type[value1].keys():
                return self.type[value1][value2]
        return False

    def getPath(self, value):
        return self.path[value]
