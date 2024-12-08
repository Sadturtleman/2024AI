import pickle
import zstandard as zstd
import pandas as pd

# csv_file = 'hash_table_less30_more70.csv'
# msgpack_file = 'hash_table_less30_more70.pickle.zst'

csv_file = 'hash_table_less30_more70_short.csv'
msgpack_file = 'hash_table_less30_more70_short.pickle.zst'

# CSV 읽기
df = pd.read_csv(csv_file)

# Pickle 직렬화 후 Zstandard 압축
with open(msgpack_file, 'wb') as f:
    compressor = zstd.ZstdCompressor(level=22)
    pickle_data = pickle.dumps(df)  # Pickle 직렬화
    compressed_data = compressor.compress(pickle_data)  # Zstandard 압축
    f.write(compressed_data)

print('done')
