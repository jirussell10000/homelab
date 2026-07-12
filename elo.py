import random

K_FACTOR = 32
players = []


class Player:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo


for i in range(10):
    players.append(Player("Player" + str(i), random.randint(1200, 2400)))


def main():
    player_a = random.choice(players)
    player_b = random.choice(players)

    if player_a.name == player_b.name:
        main()
    else:
        print("Player A name: " + player_a.name)
        print("Player A elo: " + str(player_a.elo))
        print("Player B name: " + player_b.name)        
        print("Player B elo: " + str(player_b.elo))

        elo_diff = abs(player_a.elo - player_b.elo)
        print("Elo difference: " + str(elo_diff))
        
        prob_a = player_a_win_prob(player_a, player_b)
        print("Probability A wins: " + str(prob_a))

        prob_b = 1 - prob_a
        print("Probability B wins: " + str(prob_b))

        player_a_new_elo = delta_R(prob_a)
        print("If A wins new elo: " + str(player_a.elo + player_a_new_elo))
        print("If A loses new elo: " + str(player_a.elo - player_a_new_elo))

        player_b_new_elo = delta_R(prob_b)
        print("If B wins new elo: " + str(player_b.elo + player_b_new_elo))
        print("If B loses new elo: " + str(player_b.elo - player_b_new_elo))


def player_a_win_prob(player_a, player_b):
    d_term = 10 ** ((player_b.elo - player_a.elo) / 400)
    prob_a = 1 / (1 + d_term)
    
    return prob_a


def delta_R(prob_a):
    return K_FACTOR * (1 - prob_a)
    

if __name__ == "__main__":
    main()