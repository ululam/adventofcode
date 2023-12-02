def get_rgb_counts(game: str) -> (int, int, int):
    rgb = [0, 0, 0]
    names = ["red", "green", "blue"]
    for colours in game.split(","):
        count, name = colours.strip().split(" ")
        rgb[names.index(name)] = int(count)
    return rgb


def is_game_possible(game: str) -> bool:
    red, green, blue = get_rgb_counts(game)
    return red <= 12 and green <= 13 and blue <= 14


def get_game_number(s: str) -> int:
    return int(s.split(" ")[1])


def is_possible(s: str) -> (bool, int):
    game_number, list_of_games = s.split(":")
    game_number = get_game_number(game_number.strip())
    # Check that ALL games are possible in the ;-separated list of games
    return all([is_game_possible(a_game.strip()) for a_game in list_of_games.split(";")]), game_number


# ----------- 2 -------------
def find_min_cube(s: str) -> int:
    _, list_of_games = s.split(":")
    min_rgb = [0, 0, 0]
    for game in list_of_games.split(";"):
        for i, c in enumerate(get_rgb_counts(game.strip())):
            min_rgb[i] = max(min_rgb[i], c)
    return min_rgb[0] * min_rgb[1] * min_rgb[2]


def sum_possible_games(f):
    summa = 0
    for line in f:
        ok, game = is_possible(line)
        if ok:
            summa += game
    print(summa)


def sum_min_sets_cubes(f):
    summa = sum([find_min_cube(line) for line in f])
    print(summa)


with open("2.input") as f:
    # sum_possible_games(f)
    sum_min_sets_cubes(f)
