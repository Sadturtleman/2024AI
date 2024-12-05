import gzip
import os
import pandas as pd
import ast  # 문자열을 안전하게 딕셔너리로 변환

def load_global_hash_table(file_path):
    if os.path.exists(file_path):
        try:
            with gzip.open(file_path, 'rb') as f:
                global_hash_table = pd.read_pickle(f)
                print(f"해시 테이블 로드 완료: {len(global_hash_table)}개의 부모 노드")
        except Exception as e:
            raise Exception(f"해시 테이블 파일을 읽는 중 오류 발생: {e}")
    else:
        raise FileNotFoundError(f"해시 테이블 파일을 찾을 수 없습니다: {file_path}")
    
    return global_hash_table

file_path = "hash_table.msgpack.gz"

try:
    # 데이터 로드
    hash_table = load_global_hash_table(file_path)
    print(hash_table.dtypes)
    
    # 딕셔너리로 변환
    hash_table_dict = dict(zip(hash_table['Key'], hash_table['Value']))
    
    key_to_check = "0"
    value = hash_table_dict.get(key_to_check)
    if isinstance(value, str):
        value = ast.literal_eval(value)  # 문자열을 딕셔너리로 변환
        hash_table_dict[key_to_check] = value  # 변환된 값 업데이트
   
    # Key '0'의 best_child 출력
    best_child = hash_table_dict.get("0", {}).get("best_child")
    print(f"Key '0'의 best_child 값: {best_child}")
except Exception as e:
    print(e)
