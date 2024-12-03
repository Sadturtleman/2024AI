import pandas as pd
import gzip

csv_file = 'hash_table.csv'  # 입력 csv 파일
msgpack_file = 'hash_table.msgpack.gz'  # 출력 gzip 압축 파일

df = pd.read_csv(csv_file)

with gzip.open(msgpack_file, 'wb') as f:
    df.to_pickle(f)

print('done')