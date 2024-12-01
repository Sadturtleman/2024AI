# place_dict

place_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "10": "4", "11": "5", "12": "6", "13": "7",
    "20": "8", "21": "9", "22": "A", "23": "B",
    "30": "C", "31": "D", "32": "E", "33": "F"
}

def place_hex_to_tuple(hex_char, mapping):
    for key, value in mapping.items():
        if value == hex_char:
            return tuple(map(int, key))

result = place_hex_to_tuple("E", place_dict)
print(result)

# piece_dict

piece_dict = {
    "00": "0", "01": "1", "02": "2", "03": "3",
    "04": "4", "05": "5", "06": "6", "07": "7",
    "08": "8", "09": "9", "10": "A", "11": "B",
    "12": "C", "13": "D", "14": "E", "15": "F"
}

def piece_hex_to_binary(hex_char, mapping):
    key = next(key for key, value in mapping.items() if value == hex_char)
    return tuple(int(bit) for bit in format(int(key), '04b'))

result = piece_hex_to_binary("3", piece_dict)
print(result)