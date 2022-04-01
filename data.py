import csv, vb, os

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
    for t in group_csv[g]:
        data['teams'][t] = {'group':abc[g], 'points':0, 'wins':0}

matches = []
data['GM'] = ''
gm = 0
for m in match_csv:
    st = m[0]
    r = m[1]
    l = m[2]
    t = m[3]
    if (r.startswith('#') or l.startswith('#')) and data['GM'] == '':
        data['GM'] = gm
    else:
        gm += 1
    matches.append({'st':st, 't':t, 'r':r, 'l':l, 'w':'', 'loser':''})

data['matches'] = matches

def order(data):
    for g in data['groups']:
        go = True
        t = {}
        # add group members to t
        for tn in data['teams']:
            if data['teams'][tn]['group'] == g:
                t[tn] = data['teams'][tn]
        s = sorted(t, key=lambda x: (t[x]['wins'],
                                     t[x]['points']),
                   reverse=True)
        for n in data['groups'][g]:
            if data['groups'][g][n] != '':
                go = False
        if go:
            data['groups'][g][1] = s[0]
            data['groups'][g][2] = s[1]
            data['groups'][g][3] = s[2]

    for m in range(data['current_round'], len(data['matches'])):
        if data['matches'][m]['r'].startswith('#'):
            if data['matches'][m]['r'][1] == 'G':
                data['matches'][m]['r'] = data['groups'][data['matches'][m]['r'][2]][int(data['matches'][m]['r'][3])]
            
            elif data['matches'][m]['r'][3] == 'W' and data['matches'][int(data['matches'][m]['r'][1]) * 10 + int(data['matches'][m]['r'][2]) - 1]['w'] != '':
                data['matches'][m]['r'] = data['matches'][int(data['matches'][m]['r'][1]) * 10 + int(data['matches'][m]['r'][2]) - 1]['w']
            elif data['matches'][m]['r'][3] == 'L' and data['matches'][int(data['matches'][m]['r'][1]) * 10 + int(data['matches'][m]['r'][2]) - 1]['loser'] != '':
                data['matches'][m]['r'] = data['matches'][int(data['matches'][m]['r'][1]) * 10 + int(data['matches'][m]['r'][2]) - 1]['loser']

        if data['matches'][m]['l'].startswith('#'):
            if data['matches'][m]['l'][1] == 'G':
                data['matches'][m]['l'] = data['groups'][data['matches'][m]['l'][2]][int(data['matches'][m]['l'][3])]

            elif data['matches'][m]['l'][3] == 'W' and data['matches'][int(data['matches'][m]['l'][1]) * 10 + int(data['matches'][m]['l'][2]) - 1]['w'] != '':
                data['matches'][m]['l'] = data['matches'][int(data['matches'][m]['l'][1]) * 10 + int(data['matches'][m]['l'][2]) - 1]['w']
            elif data['matches'][m]['l'][3] == 'L' and data['matches'][int(data['matches'][m]['l'][1]) * 10 + int(data['matches'][m]['l'][2]) - 1]['loser'] != '':
                data['matches'][m]['l'] = data['matches'][int(data['matches'][m]['l'][1]) * 10 + int(data['matches'][m]['l'][2]) - 1]['loser']

    return data

def export(db):
    _ = ' | '
    md = '#### Éjszakai Röpi 2022\n'
    md += '| csapatnév            | csoport | nyert | pont |\n'
    md += '|----------------------------------|---|---|----|\n'
    for t in db['teams'].keys():
        if t != '#K_D' and t != 'foo':
            md += '| ' + t  + ' ' * (32 - len(t)) + _ + db['teams'][t]['group'] + _ + str(db['teams'][t]['wins']) + _ + str(db['teams'][t]['points']) + ' |\n'

    md += '\n'
    md += '## Meccsek\n'
    md += 'Félkövér a győztes\n'
    md += '| kezdés | csapatnév                      | csapatnév                      | kategória |\n'
    md += '|--------|--------------------------------|--------------------------------|---------------|\n'
    for m in db['matches']:
        if not m['l'].startswith('#'):
            if m['l'] != 'K_D':
                if m['l'] == m['w']:
                    l = '__' + m['l'] + '__'
                else:
                    l = m['l']
            else:
                l = 'Közönségszavazatos'
        else:
            if m['l'][1] == 'G':
                l = m['l'][2] + ' csoport ' +  m['l'][3]
            else:
                n = int(m['l'][1]) * 10 + int(m['l'][2])
                l = db['matches'][n]['st'] + '-es meccs '
                if m['l'][3] == 'W':
                    l += 'győztese'
                else:
                    l += 'vesztese'
        if not m['r'].startswith('#'):
            if m['r'] != 'K_D':
                if m['r'] == m['w']:
                    r = '__' + m['r'] + '__'
                else:
                    r = m['r']
            else:
                r = 'Közönségszavazatos'
        else:
            if m['r'][1] == 'G':
                r = m['r'][2] + ' csoport ' + m['r'][3]
            else:
                r = db['matches'][int(m['r'][1]) * 10 + int(m['r'][2])]['st'] + '-es meccs '
                if m['r'][3] == 'W':
                    r += 'győztese'
                else:
                    r += 'vesztese'
        l += ' ' * (32 - len(l))
        r += ' ' * (32 -len(r))
        md += '| ' + m['st'] + _ + l + _ + r + _ + m['t'] + ' |\n'

    with open('table.md', 'w') as f:
        f.write(md)
    os.system('bash ./updategist.sh')
    
