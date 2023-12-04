def get_rgb_counts(game: str) -> (int, int, int):
    rgb = [0, 0, 0]
    for colours in game.split(","):
        count, name = colours.strip().split(" ")
        rgb[["red", "green", "blue"].index(name)] = int(count)
    return rgb

def is_game_possible(game: str) -> bool:
    red, green, blue = get_rgb_counts(game)
    return red <= 12 and green <= 13 and blue <= 14

def is_possible(s: str) -> (bool, int):
    game_number, list_of_games = s.split(":")
    game_number = int(game_number.strip().split(" ")[1])
    return all([is_game_possible(a_game.strip()) for a_game in list_of_games.split(";")]), game_number

def find_min_cube(s: str) -> int:
    _, list_of_games = s.split(":")
    min_rgb = [0, 0, 0]
    for game in list_of_games.split(";"):
        for i, c in enumerate(get_rgb_counts(game.strip())):
            min_rgb[i] = max(min_rgb[i], c)
    return min_rgb[0] * min_rgb[1] * min_rgb[2]

with open("2.input") as f:
    # print(sum([game if ok else 0 for ok, game in [is_possible(line) for line in f]]))
    print(sum([find_min_cube(line) for line in f]))
