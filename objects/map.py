import csv
import random
from constants import SPRINKLER_RANGES, SCARECROW_RANGES
from objects.tile import Tile

'''⬜⬛🟥🟦🟧🟨🟩🟪🟫❎'''


class Map:
    def __init__(self, fileloc:str):
        char_map = list(csv.reader(open(fileloc)))
        
        self.max_x = len(char_map)
        self.max_y = len(char_map[0])
        self.map = [['' for _ in range(self.max_y)] for _ in range(self.max_x)]
        self.fitness = -99999
        self.sprinklers = []
        self.scarecrows = []

        for i in range(self.max_x):
            for j in range(self.max_y):
                match char_map[i][j]:
                    case 'w':
                        self.map[i][j] = Tile('w')
                    case 's':
                        self.map[i][j] = Tile('s')
                    case 'g':
                        self.map[i][j] = Tile('g')
                    case 'b':
                        self.map[i][j] = Tile('b')
                    case _:
                        print(f"Invalid base character {char_map[i][j]}.")


    def print(self):
        ''' Prints the farm map. '''
        fitness = self.get_fitness()
        print()
        for i in range(self.max_x):
            for j in range(self.max_y):
                tile = self.map[i][j]
                match tile.base:
                    case 'w': # unusable water
                        print('🟦', end='')
                    case 's': # soil
                        if tile.watered and tile.protected:
                            print('🟫', end='')
                        elif tile.watered:
                            print('🟧', end='')
                        elif tile.protected:
                            print('⬜', end='')
                        elif tile.has_sprinkler:
                            print('🟪', end='')
                        elif tile.has_scarecrow:
                            print('⬛', end='')
                        else:
                            print('🟨', end='')
                    case 'g':
                        if tile.has_sprinkler:
                            print('🟪', end='')
                        elif tile.has_scarecrow:
                            print('⬛', end='')
                        else:
                            print('🟩', end='')
                    case 'b':
                        print('❎', end='')
                    case _:
                        print(f'Invalid map position value. {self.map[i][j]}')
                        return
            print()
        print(f"Fitness: {fitness}")

    def place_object(self, object_type:str, position:tuple[int,int]):
        ''' Calls either place_sprinkler or place_scarecrow. '''
        x, y = position
        if not self.is_valid_placement(position):
            print(f"Can't place at ({x}, {y})!")
            return
        
        if object_type in SPRINKLER_RANGES.keys():
            self.__place_sprinkler(object_type, x, y)
        elif object_type in SCARECROW_RANGES.keys():
            self.__place_scarecrow(object_type, x, y)

    def __place_sprinkler(self, sprinkler_type:str, x:int, y:int):
        ''' Places a sprinkler on the map. '''
        self.map[x][y].has_sprinkler = True
        self.map[x][y].watered = False
        self.map[x][y].protected = False
        self.map[x][y].sprinkler_type = sprinkler_type
        self.sprinklers.append((x, y))

        # # for every spot the sprinkler covers (nx, ny)
        # for dx, dy in radius_points:
        #     nx, ny = x + dx, y + dy
        #     if self.is_on_map((nx, ny)):
        #         # if the spot is tillable make it watered
        #         tile = self.map[nx][ny]
        #         if tile.tillable and not tile.has_scarecrow and not tile.has_sprinkler:
        #             self.map[nx][ny].watered = True


    def __place_scarecrow(self, scarecrow_type:str, x:int, y:int):
        ''' Places a scarecrow on the map. '''
        self.map[x][y].has_scarecrow = True
        self.map[x][y].watered = False
        self.map[x][y].protected = False
        self.map[x][y].scarecrow_type = scarecrow_type
        self.scarecrows.append((x, y))

        # # for every spot the scarecrow covers (nx, ny)
        # for dx, dy in radius_points:
        #     nx, ny = x + dx, y + dy
        #     if self.is_on_map((nx, ny)):
        #         # if the spot is tillable make it protected
        #         tile = self.map[nx][ny]
        #         if tile.tillable and not tile.has_scarecrow and not tile.has_sprinkler:
        #             self.map[nx][ny].protected = True

            
    def is_on_map(self, spot:tuple[int, int]) -> bool:
        x, y = spot
        return 0 <= x < self.max_x and 0 <= y < self.max_y

    def is_valid_placement(self, spot:tuple[int, int]) -> bool:
        ''' Returns whether an object can be placed in this spot. '''
        if not self.is_on_map(spot):
            return False
        
        x, y = spot
        tile = self.map[x][y]
        
        if tile.buildable and not tile.has_sprinkler and not tile.has_scarecrow:
            return True
        else:
            return False
    
    def rand_spot(self) -> tuple[int, int]:
        x = random.randint(0, self.max_x)
        y = random.randint(0, self.max_y)

        while not self.is_valid_placement((x, y)):
            x = random.randint(0, self.max_x)
            y = random.randint(0, self.max_y)

        return (x, y)
    
    def get_fitness(self) -> int:
        ''' Returns the fitness value of the map. '''

        for x in range(self.max_x):
            for y in range(self.max_x):
                tile = self.map[x][y]

                if hasattr(tile, 'sprinkler_type'):                    
                    radius_points = SPRINKLER_RANGES[tile.sprinkler_type]
                    # for every spot the sprinkler covers (nx, ny)
                    for dx, dy in radius_points:
                        nx, ny = x + dx, y + dy
                        if self.is_on_map((nx, ny)):
                            # if the spot is tillable make it watered
                            tile = self.map[nx][ny]
                            if tile.tillable and not tile.has_scarecrow and not tile.has_sprinkler:
                                self.map[nx][ny].watered = True

                elif hasattr(tile, 'scarecrow_type'):
                    radius_points = SCARECROW_RANGES[tile.scarecrow_type]
                    # for every spot the scarecrow covers (nx, ny)
                    for dx, dy in radius_points:
                        nx, ny = x + dx, y + dy
                        if self.is_on_map((nx, ny)):
                            # if the spot is tillable make it protected
                            tile = self.map[nx][ny]
                            if tile.tillable and not tile.has_scarecrow and not tile.has_sprinkler:
                                self.map[nx][ny].protected = True


        tillable_tiles = 0
        crop_tiles = 0

        for i in range(self.max_x):
            for j in range(self.max_x):
                tile = self.map[i][j]

                if tile.tillable:
                    tillable_tiles += 1
                    if tile.watered and tile.protected:
                        crop_tiles += 1

        fitness = crop_tiles - tillable_tiles
        self.fitness = fitness
        return fitness


