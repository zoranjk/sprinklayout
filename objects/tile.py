class Tile:
    
    def __init__(self, base:str):
        self.base = base

        match base:
            case 'w': # water
                self.buildable = False
                self.tillable = False
            case 's': # soil
                self.buildable = True
                self.tillable = True
                self.watered = False
                self.protected = False
                self.has_sprinkler = False
                self.has_scarecrow = False
            case 'g': # grass
                self.buildable = True
                self.tillable = False
                self.has_sprinkler = False
                self.has_scarecrow = False
            case 'b': # buildings
                self.buildable = False
                self.tillable = False