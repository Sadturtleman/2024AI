import pickle

output_hash = "hash_table.pkl"

def read_partial_hash_table(file_path, start=0, end=100):
    with open(file_path, 'rb') as f:
        hash_table = pickle.load(f)
    
    partial_hash_table = dict(list(hash_table.items())[start:end])
    return partial_hash_table

partial_hash_table = read_partial_hash_table(output_hash, 0, 100)

for key, value in partial_hash_table.items():
    print(f"Key: {key}, Value: {value}")

print(partial_hash_table["0 0 1"])
