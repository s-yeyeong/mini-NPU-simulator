import json

def create_cross_filter(size):
    """정가운데 십자가 모양(1) 배열 생성"""
    mid = size // 2
    return [[1 if r == mid or c == mid else 0 for c in range(size)] for r in range(size)]

def create_x_filter(size):
    """대각선 X 모양(1) 배열 생성"""
    return [[1 if r == c or r + c == size - 1 else 0 for c in range(size)] for r in range(size)]

def generate_json():
    data = {
        "filters": {},
        "patterns": {}
    }

    # 5x5, 13x13, 25x25 세 가지 크기에 대해 생성
    for size in [5, 13, 25]:
        filter_key = f"size_{size}"
        data["filters"][filter_key] = {
            "cross": create_cross_filter(size),
            "x": create_x_filter(size)
        }
        
        # 테스트 케이스 1: Cross 모양 입력 -> 정답은 '+' 
        data["patterns"][f"size_{size}_1"] = {
            "input": create_cross_filter(size),
            "expected": "+"
        }
        
        # 테스트 케이스 2: X 모양 입력 -> 정답은 'x'
        data["patterns"][f"size_{size}_2"] = {
            "input": create_x_filter(size),
            "expected": "x"
        }

    # 파일로 저장하기
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("✨ data.json 파일이 성공적으로 생성되었습니다!")

if __name__ == "__main__":
    generate_json()