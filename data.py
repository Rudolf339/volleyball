import csv
import vb

match_csv = []
with open('./meccsek.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        match_csv.append(row)
        
group_csv = []
with open('./csoportok.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    raw_csv = []
    for row in reader:
        raw_csv.append(row)
    ml = 0
    for r in raw_csv:
        ml = max(len(r), ml)

    # fill out empty spaces
    for row in range(len(raw_csv)):
        for cl in range(ml):
            try:
                a = raw_csv[row][cl]
            except IndexError:
                raw_csv[row].append('')

    print()
    # flip cloumns and rows
    for c in range(ml):
        group_csv.append([])
        for r in range(len(raw_csv)):
            if raw_csv[r][c] != '':
                group_csv[c].append(raw_csv[r][c])


data = {
    'teams':{},
    'groups':{},
    'matches':{},
    'current_round':0
    }

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # theoretical support of 8 pools
for g in range(len(group_csv)):
    data['groups'][abc[g]] = {1:'', 2:'', 3:''}
    for t in match_csv[g]:
        data['teams'][t] = {'group':abc[g], 'points':0, 'wins':0}

matches = []
for m in match_csv:
    t = m[0]
    r = m[1]
    l = m[2]
    winner = ''
    matches.append({'t':t, 'r':r, 'l':l, 'w':''})

data['matches'] = matches

def order(data):
    for g in data['groups']:
        t = {}
        # add group members to t
        for tn in data['teams']:
            if data['teams'][tn]['group'] == g:
                t[tn] = data['teams'][tn]
        s = sorted(t, key=lambda x: (t[x]['wins'],
                                     t[x]['points']),
                   reverse=True)
        data['groups'][g][1] = s[0]
        data['groups'][g][2] = s[1]
        data['groups'][g][3] = s[2]
        
    return data
