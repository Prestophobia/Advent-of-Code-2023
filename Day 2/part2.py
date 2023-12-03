from enum import Enum
import test_input

class Color(Enum):
    INVALID = 0
    RED = 1
    GREEN = 2
    BLUE = 3

class CubeSet:
    def __init__(self,r:int,g:int,b:int):
        self.r = r
        self.g = g
        self.b = b

class Game:
    def __init__(self,id_number:int,handfuls:list[CubeSet]):
        self.id_number = id_number
        self.handfuls = handfuls

def parse_color(line: str)-> Color:
    color_strs = {
        "red" : Color.RED,
        "green" : Color.GREEN,
        "blue" : Color.BLUE
    } 
    color: Color = Color.INVALID
    line = line.casefold()
    line = line.strip()
    for substr in line.split():
        if substr in color_strs:
            color = color_strs[substr]
            break
    return color

def get_minimal_bag_for_game(game: Game) -> CubeSet:
    r: int = 0
    g: int = 0
    b: int = 0

    for handful in game.handfuls:
        r = max(r,handful.r)
        g = max(g,handful.g)
        b = max(b,handful.b)

    return CubeSet(r,g,b)

def get_game_power(game: Game) -> int:
    bag: CubeSet = get_minimal_bag_for_game(game)
    return bag.r * bag.g * bag.b

def parse_handful(line: str) -> CubeSet:
    r: int = 0
    g: int = 0
    b: int = 0
    for entry in line.split(','):
        color:Color = parse_color(entry)
        if color != Color.INVALID:
            for word in entry.split():
                if word.isnumeric():
                    match color:
                        case Color.RED:
                            r = int(word)
                        case Color.GREEN:
                            g = int(word)
                        case Color.BLUE:
                            b = int(word)
                    break
    return CubeSet(r,g,b)

def parse_game(line: str) -> Game:
    id_number: int = 0
    handfuls: list[CubeSet] = []
    id_handfuls_pair = line.split(':')
    if  len(id_handfuls_pair) > 1:
        for substr in id_handfuls_pair[0].split():
            if substr.isnumeric():
                id_number = int(substr)
                break
        handful_strs = id_handfuls_pair[1].split(';')
        for handful_str in handful_strs:
            handfuls.append(parse_handful(handful_str))
    return Game(id_number,handfuls)

def parse_game_set(games: str) -> list[Game]:
    game_set: list[Game] = []
    for line in games.split('\n'):
        game_set.append(parse_game(line))
    return game_set

def sum_game_power(game_set: list[Game]) -> int:
    power_sum = 0
    for game in game_set:
        power_sum = power_sum + get_game_power(game)
    return power_sum

game_set = parse_game_set(test_input.full_input)
power_sum = sum_game_power(game_set)

print(str(power_sum))