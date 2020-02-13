class team:
    def __init__(self, name, goup, members):
        self.name = name
        self.group = group
        self.point = 0
        self.wins = 0
        self.losses = 0
        self.members = members
    
    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

class match:
    def __init__(self, l, r, group, t):
        self.l = l
        self.r = r
        self.group = group
        self.winner = ""
        self.scheduled_time = t

class group:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

def find_team(name, l):
    for t in l:
        if t.name == name:
            return t
    return False

matches = []
