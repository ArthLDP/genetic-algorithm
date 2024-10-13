from random import randrange

TEAM_SIZE = 5
POPULATION_SIZE = 100
MAX_GAMES = 20

class Player:
    def __init__(self, name, aptitude, games):
        self.name = name
        self.aptitude = aptitude
        self.games = games

    def __str__(self):
        return f"Name = {self.name}, Aptitude = {self.aptitude}, Games = {self.games}"

player1 = Player("Fábio", 7, 2)
player2 = Player("Carlos", 9, 5)
player3 = Player("Matheus", 6, 2)
player4 = Player("Luan", 9, 6)
player5 = Player("Podeisso", 4, 2)
player6 = Player("Arnaldo", 3, 4)
player7 = Player("Tulio", 4, 1)
player8 = Player("Neymar", 7, 6)
player9 = Player("Theus", 5, 1)
player10 = Player("Fenomeno", 8, 7)

all_players = [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10]

def get_binary_from_team(team):
    binary_team = []

    for i in range(len(all_players)):
        binary_team.append(0)

    for i in team:
        player_index = all_players.index(i)
        binary_team[player_index] = 1

    return binary_team

def get_team_from_binary(binary_team):
    team = []

    for index, i in enumerate(binary_team):
        if i == 1:
            team.append(all_players[index])

    return team

def generate_random_binary_team():
    team = []

    for i in range(len(all_players)):
        team.append(0)

    # Generate Random and Different indexes from 0 to all_players size - 1, to overwrite 1
    for i in range(TEAM_SIZE):
        index = randrange(len(all_players))

        while team[index] == 1:
            index = randrange(len(all_players))

        team[index] = 1

    return team

def generate_binary_population(size):
    population = []

    for i in range(size):
        population.append(generate_random_binary_team())

    return population

def get_sum_of_games_from_binary_team(binary_team):
    team = get_team_from_binary(binary_team)
    games = 0

    for i in team:
        games += i.games

    return games


def get_sum_of_aptitude_from_binary_team(binary_team):
    team = get_team_from_binary(binary_team)
    aptitude = 0
    games = 0

    for i in team:
        games += i.games
        aptitude += i.aptitude

    # Punish aptitude of team that have more than 20 games
    if games > MAX_GAMES:
        aptitude -= 100

    return aptitude

def get_best_team_from_binary_population(binary_population):
    best_binary_team = []

    for team in binary_population:
        if len(best_binary_team) == 0:
            best_binary_team.append(team)

        tmp_binary_team = team

        sum_of_games = get_sum_of_games_from_binary_team(tmp_binary_team)
        sum_of_aptitude = get_sum_of_aptitude_from_binary_team(tmp_binary_team)

        if sum_of_aptitude > get_sum_of_aptitude_from_binary_team(best_binary_team):
            best_binary_team = tmp_binary_team

    return best_binary_team


def mutate_invalid_binary_son(son):
    players = 0

    for i in son:
        if i == 1:
            players += i

    if players > TEAM_SIZE:
        diff = players - TEAM_SIZE

        while diff > 0:
            index = randrange(len(son))
            if son[index] == 1:
                son[index] = 0
                diff -= diff

    if players < TEAM_SIZE:
        diff = TEAM_SIZE - players

        while diff > 0:
            index = randrange(len(son))
            if son[index] == 0:
                son[index] = 1
                diff -= diff


def generate_binary_son_from_parents(first_parent, second_parent):
    son = []

    middle_index = round(len(first_parent) / 2)

    for i in range(middle_index):
        son.append(first_parent[i])

    for i in range(middle_index, len(first_parent)):
        son.append(second_parent[i])

    mutate_invalid_binary_son(son)

    return son

first_population = generate_binary_population(POPULATION_SIZE)
second_population = generate_binary_population(POPULATION_SIZE)

first_parent_binary = get_best_team_from_binary_population(first_population)
second_parent_binary = get_best_team_from_binary_population(second_population)
son_binary = generate_binary_son_from_parents(first_parent_binary, second_parent_binary)

first_parent_team = get_team_from_binary(first_parent_binary)
second_parent_team = get_team_from_binary(second_parent_binary)
son_team = get_team_from_binary(son_binary)

print("//////// BINARY ////////\n")
print("First parent binary: ", first_parent_binary)
print("Second parent binary: ", second_parent_binary)
print("Son binary: ", son_binary)

print("\n//////// TEAM ////////\n")

print("First parent team: " + "APTITUDE = ", get_sum_of_aptitude_from_binary_team(first_parent_binary),
      "| GAMES = ", get_sum_of_games_from_binary_team(first_parent_binary))

for first_parent_player in first_parent_team:
    print(first_parent_player)

print("\nSecond parent team: " + "APTITUDE = ", get_sum_of_aptitude_from_binary_team(second_parent_binary),
      "| GAMES = ", get_sum_of_games_from_binary_team(second_parent_binary))

for second_parent_player in second_parent_team:
    print(second_parent_player)

print("\nSon team: " + "APTITUDE = ", get_sum_of_aptitude_from_binary_team(son_binary),
      "| GAMES = ", get_sum_of_games_from_binary_team(son_binary))

for son_player in son_team:
    print(son_player)
