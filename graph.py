import pandas
import tqdm

csvname = 'tree_merged_1to20_table.csv'
CUTTOTAL = 1
CUTWINRATE = 0.7
CUTLEVEL = 2

game = pandas.read_csv(csvname)

game['Level'] = pandas.to_numeric(game['Level'], errors = 'coerce')
game['Total Games'] = pandas.to_numeric(game['Total Games'], errors = 'coerce')
game['Wins'] = pandas.to_numeric(game['Wins'], errors = 'coerce')


game = game[
    (game['Total Games'] > CUTTOTAL) & 
    (game['Wins'] / game['Total Games'] > CUTWINRATE) &
    (game['Level'] > CUTLEVEL)
]

print('cut game')

game = game.sort_values(by = ['Wins', 'Total Games'], ascending = False)

print('sort game')

print(game)

