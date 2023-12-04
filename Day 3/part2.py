import puzzle_input
import copy

class SchematicCoordinates:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y

class Part:
    def __init__(self, number: int, coords: list[SchematicCoordinates]):
        self.number = number
        self.coords = coords
        self.connections:list[chr] = []

class Gear:
    def __init__(self, pos: SchematicCoordinates, connected_parts: list[Part]):
        self.pos = pos
        self.connected_parts = connected_parts
        self.ratio = 0
        if len(self.connected_parts) == 2:
            self.ratio = self.connected_parts[0].number * self.connected_parts[1].number

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

def is_part_number_valid(part_number: Part, schematic: Schematic) -> bool:
    is_valid: bool = False

    for coord in part_number.coords:
        range_min_x,range_min_y = max(0,coord.x - 1),max(0,coord.y - 1)

        #+2 to make the loops inclusive
        range_max_x,range_max_y = min(Schematic.dimensions,coord.x + 2),min(Schematic.dimensions,coord.y + 2)

        for x in range(range_min_x,range_max_x):
            for y in range(range_min_y,range_max_y):
                character = schematic.grid[x][y]
                if is_character_valid(character):
                    part_number.connections.append(character)
                    is_valid = True

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

def get_part_numbers_from_schematic(schematic: Schematic) -> list[Part]:
    schematic_copy = copy.deepcopy(schematic)
    parts:list[Part] = []
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
                parts.append(Part(num,coord))
    return parts

def filter_valid_parts(parts:list[Part],schematic: Schematic)->list[Part]:
    valid_parts:list[Part] = []
    for part in parts:
        if is_part_number_valid(part,schematic):
            valid_parts.append(part)
    return valid_parts

#only do this after a pass from filter_valid_parts
def filter_potentially_geared_parts(parts:list[Part])->list[Part]:
    valid_parts:list[Part] = []
    for part in parts:
        for connection in part.connections:
            if connection == "*":
                valid_parts.append(part)
                break
    return valid_parts

def sum_part_numbers(parts:list[Part]) -> int:
    sum_numbers = 0
    for part in parts:
        sum_numbers = sum_numbers + part.number
    return sum_numbers

def get_gears_from_schematic(schematic: Schematic, gear_candidate_parts: list[Part]) -> list[Gear]:
    local_gears:list[Gear] = []
    for y in range(Schematic.dimensions):
        for x in range(Schematic.dimensions):
            if schematic.grid[x][y] == '*':
                coord = SchematicCoordinates(x,y)
                connected_parts: list[Part] = []

                range_min_x,range_min_y = max(0,coord.x - 1),max(0,coord.y - 1)
                #+2 to make the loops inclusive
                range_max_x,range_max_y = min(Schematic.dimensions,coord.x + 2),min(Schematic.dimensions,coord.y + 2)

                for candidate in gear_candidate_parts:
                    isConnected = False
                    for candidate_coord in candidate.coords:      
                        for check_x in range(range_min_x,range_max_x):
                            for check_y in range(range_min_y,range_max_y):
                                if candidate_coord.x == check_x and candidate_coord.y == check_y:
                                    isConnected = True
                                    break
                            if isConnected:
                                break
                        if isConnected:
                                break
                    if isConnected:
                        connected_parts.append(candidate)
                if len(connected_parts) == 2:
                    local_gears.append(Gear(coord,connected_parts))
    return local_gears

def get_sum_gear_ratios(gears: list[Gear]) -> int:
    ratio_sum = 0
    for gear in gears:
        ratio_sum = ratio_sum + gear.ratio
    return ratio_sum

schematic = parse_schematic(puzzle_input.full_input)
parts  = get_part_numbers_from_schematic(schematic)
valid_parts = filter_valid_parts(parts,schematic)
sum_numbers = sum_part_numbers(valid_parts)
gear_candidate_parts = filter_potentially_geared_parts(valid_parts)
gears = get_gears_from_schematic(schematic,gear_candidate_parts)
ratio_sum = get_sum_gear_ratios(gears)

print(ratio_sum)