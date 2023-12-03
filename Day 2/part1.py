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

def is_handful_possible(bag: CubeSet, handful: CubeSet) -> bool:
    possible:bool = (handful.r <= bag.r)
    possible = possible and (handful.g <= bag.g)
    possible = possible and (handful.b <= bag.b)
    return possible

def is_game_possible(bag: CubeSet, game: Game) -> bool:
    for handful in game.handfuls:
        if not is_handful_possible(bag, handful):
            return False
    return True

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

def filter_games_possible_with_bag(game_set: list[Game], bag: CubeSet) -> list[Game]:
    possible_game_set: list[Game] = []
    for game in game_set:
        if is_game_possible(bag,game):
            possible_game_set.append(game)
    return possible_game_set

def sum_game_set_ids(game_set: list[Game]) -> int:
    id_sum = 0
    for game in game_set:
        id_sum = id_sum + game.id_number
    return id_sum

bag = CubeSet(12,13,14)
game_set = parse_game_set(test_input.full_input)
possible_games = filter_games_possible_with_bag(game_set,bag)
id_sum = sum_game_set_ids(possible_games)

print(str(id_sum))