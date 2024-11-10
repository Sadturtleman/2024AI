import pickle
import os
from tqdm import tqdm

dir_path = "/Users/yereum/Documents/인공지능/2024AI/pickle_files"
merged_dict = {}

for i in tqdm(range(1, 238), desc="Merging pickle files"):
    file_path = os.path.join(dir_path, f"tuning{i}.pickle")
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
        merged_dict.update(data)

output_file_path = os.path.join(dir_path, "merged_dict.pickle")
with open(output_file_path, 'wb') as output_file:
    pickle.dump(merged_dict, output_file)

print("Done")