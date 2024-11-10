import pickle

# Load pickle file
with open("tuning.pickle", "rb") as fr:
    data = pickle.load(fr)

# print(data)

# Print each iteration
t = 1
for key, value in data.items():
    key_parts = [key[i:i+4] for i in range(0, len(key), 4)] 
    print(f"------Turn {t}------", "\nPlay Log: ", key_parts, "\nWinner: ", value)
    t += 1

# 시뮬레이션 데이터를 분석해서 승리하는 조합을 찾으면 어떨지?
# ex) Clustering, Association Rule Learning, Regression, Association Rule Learning, Markov chain rule
