import pandas
import pickle
import tqdm

def piece_dex_to_hex(dex_num):
    if (int(dex_num) < 10):
        return str(int(dex_num))
    else:
        return chr(int(dex_num) + 55)
    
def place_dex_to_hex(two_digit_num):
    if int(two_digit_num) < 10:
        return f"0{int(two_digit_num)}"  
    else:
        return chr(int(two_digit_num) + 55) 
    

csvfile = 'tuning1.csv'
picklefile = 'tuning10.pickle'

csvdata = pandas.read_csv(csvfile)

with open(picklefile, 'rb') as file:
    pickledata = pickle.load(file)

for log, value in tqdm.tqdm(pickledata.items()):

    text = ""
    for level in range(0, len(log), 4):
        part = log[level:level + 4]

        piece_hex = piece_dex_to_hex(part[:2])
        place_hex = place_dex_to_hex(part[2:])

        text = text + piece_hex + place_hex + " "

        find_row = csvdata.loc[csvdata['Play Log'] == text]
        
        if find_row.empty:
            df = pandas.DataFrame({
                'Level' : [level + 1],
                'Wins' : [int(value == 1)],
                'Total Games' : [1],
                'Play Log' : [text]
                })
            
            csvdata = pandas.concat([csvdata, df], ignore_index = True)

        else:
            csvdata.loc[find_row.index, 'Wins'] += 1
            csvdata.loc[find_row.index, 'Total Games'] += 1

        
csvdata.to_csv('test.csv')

