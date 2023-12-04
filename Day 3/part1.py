import puzzle_input
import copy

class SchematicCoordinates:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y

class PartNumber:
    def __init__(self, number: int, coords: list[SchematicCoordinates]):
        self.number = number
        self.coords = coords
        self.connections:list[chr] = []

class Schematic:
    dimensions = 140
    def  __init__(self):
        self.grid:list[list[chr]] = []
        for i in range(Schematic.dimensions):
            row:list[list[chr]] = []
            for j in range(Schematic.dimensions):
                row.append(0)
            self.grid.append(row)

def is_character_valid(char: chr) -> bool:
    valid_chrs = {
        '@' : True,
        '#' : True,
        '$' : True,
        '%' : True,
        '&' : True,
        '*' : True,
        '-' : True,
        '=' : True,
        '/' : True,
        '+' : True
    } 

    return char in valid_chrs

def is_part_number_valid(part_number: PartNumber, schematic: Schematic) -> bool:
    is_valid: bool = False

    for coord in part_number.coords:
        range_min_x,range_min_y = max(0,coord.x - 1),max(0,coord.y - 1)

        #+2 to make the loops inclusive
        range_max_x,range_max_y = min(Schematic.dimensions,coord.x + 2),min(Schematic.dimensions,coord.y + 2)

        for x in range(range_min_x,range_max_x):
            for y in range(range_min_y,range_max_y):
                character = schematic.grid[x][y]
                is_valid = is_valid or is_character_valid(character)
                if is_valid:
                    part_number.connections.append(character)
                    break
            if is_valid:
                break
        if is_valid:
            break
    

    #if not is_valid:
        #print(str(part_number.number)+": "+str(is_valid))

    return is_valid

def parse_schematic(schematic_str: str)->Schematic:
    schematic = Schematic()
    x,y = 0,0
    for line in schematic_str.split('\n'):
        x = 0
        for character in line:
            schematic.grid[x][y]  = character
            x = x + 1
        y = y + 1
    return schematic

def get_part_numbers_from_schematic(schematic: Schematic) -> list[PartNumber]:
    schematic_copy = copy.deepcopy(schematic)
    parts:list[PartNumber] = []
    for y in range(Schematic.dimensions):
        for x in range(Schematic.dimensions):
            if schematic_copy.grid[x][y].isnumeric():
                num = int(schematic_copy.grid[x][y])
                schematic_copy.grid[x][y] = '.'
                coord = [SchematicCoordinates(x,y)]
                if x < (Schematic.dimensions - 1):
                    if schematic_copy.grid[x+1][y].isnumeric():
                        num = num * 10 + int(schematic_copy.grid[x+1][y])
                        schematic_copy.grid[x+1][y] = '.'
                        coord.append(SchematicCoordinates(x+1,y))
                        if x < (Schematic.dimensions - 2):
                            if schematic_copy.grid[x+2][y].isnumeric():
                                num = num * 10 + int(schematic_copy.grid[x+2][y])
                                schematic_copy.grid[x+2][y] = '.'
                                coord.append(SchematicCoordinates(x+2,y))
                parts.append(PartNumber(num,coord))
    return parts

def filter_valid_parts(parts:list[PartNumber],schematic: Schematic)->list[PartNumber]:
    valid_parts:list[PartNumber] = []
    for part in parts:
        if is_part_number_valid(part,schematic):
            valid_parts.append(part)
    return valid_parts

def sum_part_numbers(parts:list[PartNumber]) -> int:
    sum_numbers = 0
    for part in parts:
        sum_numbers = sum_numbers + part.number
    return sum_numbers

schematic = parse_schematic(puzzle_input.full_input)
parts  = get_part_numbers_from_schematic(schematic)
valid_parts = filter_valid_parts(parts,schematic)
sum_numbers = sum_part_numbers(valid_parts)

print(sum_numbers)