import http.server
import inspect

print("=== http.server 모듈 전체 탐색 ===\n")

# 1. 모듈 내부의 모든 것을 출력
print("1. http.server 모듈 내부 항목들:")
all_items = dir(http.server)
for item in all_items[:20]:  # 처음 20개만 출력
    print(f"   - {item}")
print(f"   ... 총 {len(all_items)}개의 항목\n")