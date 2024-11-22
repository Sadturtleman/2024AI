#깊이별 승률 변화 시각화 - 게임 진행에 따른 전략적 중요도 분석 가능
import pandas as pd
import matplotlib.pyplot as plt


file_path = "tree_merged_1to20_table.csv"


df = pd.read_csv(file_path)


df["Win Rate"] = df["Wins"] / df["Total Games"]


depth_win_rate = df.groupby("Level")["Win Rate"].mean()

plt.figure(figsize=(10, 6))
plt.plot(depth_win_rate.index, depth_win_rate.values, marker="o", color="b", label="Average Win Rate")
plt.axhline(y=depth_win_rate.mean(), color="r", linestyle="--", label="Overall Average Win Rate")
plt.title("Win Rate by Depth")
plt.xlabel("Depth (Level)")
plt.ylabel("Average Win Rate")
plt.xticks(depth_win_rate.index)
plt.grid(alpha=0.5)
plt.legend()
plt.show()
