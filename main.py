import json
import time

def normalize_label(label):
    target = str(label).lower()
    if target in ['+', 'cross']: return 'Cross'
    elif target == 'x': return 'X'
    return label

def calculate_mac(pattern, filter_data):
    score = 0.0
    size = len(pattern)
    for r in range(size):
        for c in range(size):
            score += float(pattern[r][c]) * float(filter_data[r][c])
    return score

def get_manual_input(size=3):
    matrix = []
    while len(matrix) < size:
        # 🌟 예영님이 마음에 들어하셨던 친절한 입력 디자인으로 복구!
        line = input(f"{len(matrix) + 1}번째 줄 : ").split()
        if len(line) != size:
            print(f"-> 삐빅! 숫자를 정확히 {size}개 입력해야 합니다.")
            continue
        matrix.append([float(x) for x in line])
    return matrix

def judge(score_a, score_b, mode):
    epsilon = 1e-9
    diff = score_a - score_b
    
    if abs(diff) < epsilon:
        return "판정 불가 (|A-B| < 1e-9)" if mode == 1 else "UNDECIDED"
    
    if mode == 1:
        return "A" if diff > 0 else "B"
    else:
        return "Cross" if diff > 0 else "X"

def measure_performance(pattern, filter_data, iterations=10):
    start_time = time.perf_counter()
    for _ in range(iterations):
        calculate_mac(pattern, filter_data)
    end_time = time.perf_counter()
    return ((end_time - start_time) / iterations) * 1000

def run_mode_1():
    print("\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    print("필터 A (3줄 입력, 공백 구분)")
    filter_a = get_manual_input(3)
    
    print("\n필터 B (3줄 입력, 공백 구분)")
    filter_b = get_manual_input(3)
    
    print("\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    print("패턴 (3줄 입력, 공백 구분)")
    user_pattern = get_manual_input(3)
    
    s_a = calculate_mac(user_pattern, filter_a)
    s_b = calculate_mac(user_pattern, filter_b)
    
    final_decision = judge(s_a, s_b, mode=1)
    avg_time = measure_performance(user_pattern, filter_a)
    
    print("\n#---------------------------------------")
    # 🌟 판정 결과에 따라 출력되는 제목과 내용이 예시와 완벽히 일치하도록 분기 처리
    if "판정 불가" in final_decision:
        print("# [3] MAC 결과 (판정 불가)")
        print("#---------------------------------------")
        print(f"A 점수: {s_a}")
        print(f"B 점수: {s_b}")
        print(f"판정: {final_decision}")
    else:
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        print(f"A 점수: {s_a}")
        print(f"B 점수: {s_b}")
        print(f"연산 시간(평균/10회): {avg_time:.3f} ms")
        print(f"판정: {final_decision}")

def run_mode_2():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("에러: data.json 파일이 없습니다!")
        return

    filters = data.get('filters', {})
    patterns = data.get('patterns', {})

    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    for k in filters: print(f"✓ {k} 필터 로드 완료 (Cross, X)")

    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    pass_count = 0
    fail_count = 0
    performance_log = {}

    for p_id, p_info in patterns.items():
        try:
            size = int(p_id.split('_')[1])
            f_key = f"size_{size}"
            
            f_cross = filters[f_key]['cross']
            f_x = filters[f_key]['x']
            p_input = p_info['input']
            expected = normalize_label(p_info['expected'])

            sc_cross = calculate_mac(p_input, f_cross)
            sc_x = calculate_mac(p_input, f_x)
            
            final_judge = judge(sc_cross, sc_x, mode=2)
            
            if final_judge == expected:
                status = "PASS"
                pass_count += 1
            else:
                status = "FAIL"
                fail_count += 1
                
            print(f"--- {p_id} ---")
            print(f"Cross 점수: {sc_cross}")
            print(f"X 점수: {sc_x}")
            print(f"판정: {final_judge} | expected: {expected} | {status}")

            if size not in performance_log:
                performance_log[size] = measure_performance(p_input, f_cross)

        except Exception as e:
            print(f"--- {p_id} ---")
            print(f"FAIL (에러: {e})")
            fail_count += 1

    print("\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    print("-" * 40)
    for sz in sorted(performance_log.keys()):
        print(f"{sz}x{sz:<8} {performance_log[sz]:<15.3f} {sz*sz}")

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {pass_count + fail_count}개\n통과: {pass_count}개\n실패: {fail_count}개")

if __name__ == "__main__":
    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]\n1. 사용자 입력 (3x3)\n2. data.json 분석")
    choice = input("선택: ")
    if choice == '1': run_mode_1()
    elif choice == '2': run_mode_2()