import pandas as pd

pickle_file = 'hash_table_less45_more55_short_asymmetric_lv8.pkl'  # pickle 파일 이름
csv_file = 'hash_table_less45_more55_short_asymmetric_lv8.csv'   # 출력할 csv 파일 이름

try:
    df = pd.read_pickle(pickle_file)
    df = pd.DataFrame(list(df.items()), columns=['Key', 'Value'])

    df.to_csv(csv_file, index=False)
    print(f"{csv_file}로 변환 완료!")
except Exception as e:
    print(f"오류 발생: {e}")