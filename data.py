import csv
import vb

results = []
with open("./meccsek.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        results.append(row)

# for i in range(len(results)):
#     results[i][0] = int(results[i][0].split(':').join(''))

teams = [vb.team('ChikNwins', 'A'),
         vb.team('Csak úgy', 'A'),
         vb.team('Wasserspitzmäuser', 'A'),
         vb.team('Ked Regeli Djuras', 'A'),
         vb.team('MAMBA', 'A'),
         vb.team('Hupszidézi', 'B'),
         vb.team('That\'s what she set', 'B'),
         vb.team('Avangurs', 'B'),
         vb.team('Krrr', 'B'),
         vb.team('Hóbortos hubihuszárnyunyuskák', 'B'),
         vb.team('FRÖCCSKÖLŐK', 'C'),
         vb.team('Give it up', 'C'),
         vb.team('Pontverseny', 'C'),
         vb.team('Volley Buli', 'C'),
         vb.team('Nicolas Cage szektája', 'D'),
         vb.team('Ászéjszaka', 'D'),
         vb.team('Bioszból elég, ha kettes', 'D'),
         vb.team('Csumpi csapat', 'D'),
         vb.team('Last last minute', 'D'),
         vb.team('ettemmaxddddd', 'E'),
         vb.team('Végmoréna sánc', 'E'),
         vb.team('A Team ++', 'E'),
         vb.team('Vicceskóla', 'E')
         ]

data = {
    'teams':{
        'ChikNwins':{
            'group':'A',
            'points':0,
            'wins':0,
            },
        'Csak úgy':{
            'group':'A',
            'points':0,
            'wins':0,
            },
        'Wasserspitzmäuser':{
            'group':'A',
            'points':0,
            'wins':0,
            },
        'Ked Regeli Djuras':{
            'group':'A',
            'points':0,
            'wins':0,
            },
        'MAMBA':{
            'group':'A',
            'points':0,
            'wins':0,
            },
        'Hupszidézi':{
            'group':'B',
            'points':0,
            'wins':0,
            },
        'That\'s what she set':{
            'group':'B',
            'points':0,
            'wins':0,
            },
        'Avangurs':{
            'group':'B',
            'points':0,
            'wins':0,
            },
        'Krrr':{
            'group':'B',
            'points':0,
            'wins':0,
            },
        'Hóbortos hubihuszárnyunyuskák':{
            'group':'B',
            'points':0,
            'wins':0,
            },
        'FRÖCCSKÖLŐK':{
            'group':'C',
            'points':0,
            'wins':0,
            },
        'Give it up':{
            'group':'C',
            'points':0,
            'wins':0,
            },
        'Pontverseny':{
            'group':'C',
            'points':0,
            'wins':0,
            },
        'Volley Buli':{
            'group':'C',
            'points':0,
            'wins':0,
            },
        'Nicolas Cage szektája':{
            'group':'D',
            'points':0,
            'wins':0,
            },
        'Ászéjszaka':{
            'group':'D',
            'points':0,
            'wins':0,
            },
        'Bioszból elég, ha kettes':{
            'group':'D',
            'points':0,
            'wins':0,
            },
        'Csumpi csapat':{
            'group':'D',
            'points':0,
            'wins':0,
            },
        'Last last minute':{
            'group':'D',
            'points':0,
            'wins':0,
            },
        'ettemmaxddddd':{
            'group':'E',
            'points':0,
            'wins':0,
            },
        'Végmoréna sánc':{
            'group':'E',
            'points':0,
            'wins':0,
            },
        'A Team ++':{
            'group':'E',
            'points':0,
            'wins':0,
            },
        'Vicceskóla':{
            'group':'E',
            'points':0,
            'wins':0,
            }
        },
    'groups':{}
    }


matches = []

for m in results:
    t = m[0]
    r = m[1]
    l = m[2]
    winner = ''
    matches.append({'t':t, 'r':r, 'l':l, 'w':''})

data['matches'] = matches

group_names = ['A', 'B', 'C', 'D', 'E']
for g in group_names:
    data['groups'][g] = {1:'', 2:'', 3:''}

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
