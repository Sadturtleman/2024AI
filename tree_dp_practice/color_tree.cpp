#include <iostream>
#include <vector>
#include <cstring>
#include <algorithm>
#define FAST ios::sync_with_stdio(0); cin.tie(0); cout.tie(0)
using namespace std;

typedef long long ll;
const int MAX = 100000; // 문제에서 주어진 최대 노드 수
const ll MOD = 1e9 + 7;  // 나머지 연산에 사용할 값

// 참고 링크: https://acm-iupc.tistory.com/entry/트리와-dp

// n: 노드 수, k: 색이 지정된 노드의 수
ll n, k;
// dp[u][c]는 u번 노드에 색 c를 칠했을 때의 경우의 수
ll dp[MAX][4];
// 각 노드의 색 정보를 저장 (1~3: 색, 0: 색이 지정되지 않음)
ll clr[MAX];
// 트리의 인접 리스트
vector<int> adj[MAX];

ll f(int u, int pc, int p) {
	// 메모이제이션
	ll& ret = dp[u][pc];  // ret: dp 테이블의 참조
	if (ret != -1) return ret;  // 값이 이미 존재하면 반환

	// 현재 노드의 색이 지정되지 않은 경우
	if (clr[u] == 0) {
		ret = 0;  // 초기화
		//가능한 색상 (1~3) 모두 시도
		for (int c = 1; c <= 3; c++) {
			if (c == pc) continue;  // 이전 색과 동일하면 패스
			ll temp = 1;  // 현재 색 c에 대해 경우의 수 초기화
			// 인접한 모든 정점에 대해 재귀 호출
			for (int v : adj[u]) {
				if (v == p) continue;  // 부모 노드는 제외
				temp *= f(v, c, u);  // 자식 노드에 대해 경우의 수 곱하기
				temp %= MOD;  // 모듈러 연산
			}
			ret += temp;  // 가능한 모든 색상의 경우의 수 구하기
			ret %= MOD;  // 모듈러 연산
		}
	}
	// 현재 노드에 이미 색이 지정된 경우
	else { 
		// 이전 색과 모순되면 경우의 수는 0
		if (pc == clr[u]) 
			return ret = 0;

		// 모든 인접한 정점에 대해서 곱해준다.
		ret = 1;
		for (int v : adj[u]) {
			if (v == p) continue;  // 부모 노드는 제외
			ret *= f(v, clr[u], u);  // 자식 노드에 대해 경우의 수 곱하기
			ret %= MOD;  // 모듈러 연산
		}
	}
	return ret;  // u번 노드에 대한 경우의 수 반환
}

int main() {
	FAST;
	cin >> n >> k;  // (입력) n: 노드 수, k: 색이 지정된 노드의 수
	for (int i = 0, u, v; i < n - 1; i++) {
		cin >> u >> v;  // (입력) 정점 u, v 
		// u와 v 간의 양방향 간선 생성
		adj[u].push_back(v);
		adj[v].push_back(u);
	}
	for (int i = 0, u, c; i < k; i++) {
		cin >> u >> c;  // (입력) 색이 지정된 노드와 색 입력
		clr[u] = c;  // clr 배열에 색 저장
	}

	// dp 테이블을 -1로 초기화 (아직 계산되지 않은 상태)
	memset(dp, -1, sizeof(dp)); 
	
	// 루트 노드(1번)에서 시작하여 색칠 가능한 모든 경우의 수 계산
	//pc == 0으로 초기화해서 부모 노드의 색상이 없는 경우를 처리
	cout << f(1, 0, 0) << '\n';
}