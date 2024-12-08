import pandas as pd

# pickle_file = 'hash_table_less30_more70.pkl'  # pickle 파일 이름
# csv_file = 'hash_table_less30_more70.csv'   # 출력할 csv 파일 이름

pickle_file = 'hash_table_less30_more70_short.pkl'  # pickle 파일 이름
csv_file = 'hash_table_less30_more70_short.csv'   # 출력할 csv 파일 이름

try:
    df = pd.read_pickle(pickle_file)
    df = pd.DataFrame(list(df.items()), columns=['Key', 'Value'])

    df.to_csv(csv_file, index=False)
    print(f"{csv_file}로 변환 완료!")
except Exception as e:
    print(f"오류 발생: {e}")