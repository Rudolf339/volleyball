class team:
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.point = 0
        self.point2 = 0
        self.wins = 0
        self.wins2 = 0
        self.losses = 0
    
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
        self.first = None
        self.second = None
        self.third = None

    def ranking(self):
        x = {}
        for i in self.teams:
            t[i.name] = t.points
        sort = sorted(x.items(), key=lambda y: y[1])
        
        self.first = find_team(sort[0], self.teams)
        self.second = find_team(sort[1], self.teams)
        self.third = find_team(sort[2], self.teams)


def find_team(name, l):
    for t in l:
        if t.name == name:
            return t
    return False
