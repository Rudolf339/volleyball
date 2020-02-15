import csv
import vb

results = []
with open("./meccsek.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        results.append(row)

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
         vb.team('Pintverseny', 'C'),
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

