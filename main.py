import json
import time  # ⏱️ 시간 측정을 위해 새로 추가된 도구!

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
    print(f"\n{size}x{size} 크기의 숫자를 한 줄씩 입력하세요 (공백 구분):")
    matrix = []
    while len(matrix) < size:
        line = input(f"{len(matrix) + 1}행: ").split()
        if len(line) != size:
            print(f"-> 삐빅! 숫자를 정확히 {size}개 입력해야 합니다.")
            continue
        matrix.append([float(x) for x in line])
    return matrix

def judge(score_cross, score_x):
    epsilon = 1e-9
    diff = score_cross - score_x
    if abs(diff) < epsilon:
        return "UNDECIDED"
    return "Cross" if diff > 0 else "X"

def measure_performance(pattern, filter_data, iterations=10):
    """MAC 연산 시간을 측정합니다 (10회 반복 후 평균 시간 반환, ms 단위)"""
    start_time = time.perf_counter()  # 초시계 시작!
    for _ in range(iterations):
        calculate_mac(pattern, filter_data)
    end_time = time.perf_counter()    # 초시계 정지!
    
    # ms(밀리초) 단위로 변환해서 평균 구하기
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    return avg_time_ms

def run_mode_1():
    print("\n[필터 Cross 입력]")
    filter_cross = get_manual_input(3)
    print("\n[필터 X 입력]")
    filter_x = get_manual_input(3)
    print("\n[검사할 패턴 입력]")
    user_pattern = get_manual_input(3)
    
    s_cross = calculate_mac(user_pattern, filter_cross)
    s_x = calculate_mac(user_pattern, filter_x)
    final_decision = judge(s_cross, s_x)
    avg_time = measure_performance(user_pattern, filter_cross) # 성능 측정
    
    print("\n=== [MAC 결과] ===")
    print(f"Cross 점수: {s_cross}")
    print(f"X 점수: {s_x}")
    print(f"판정: {final_decision}")
    print(f"연산 시간(평균/10회): {avg_time:.6f} ms")

def run_mode_2():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("에러: data.json 파일이 없습니다!")
        return

    filters = data.get('filters', {})
    patterns = data.get('patterns', {})

    print("\n# [1] 필터 로드")
    for k in filters: print(f"✓ {k} 필터 준비 완료")

    print("\n# [2] 패턴 채점 (라벨 정규화 적용)")
    pass_count = 0
    fail_count = 0
    
    # 🌟 크기별 연산 시간을 저장할 딕셔너리 준비
    performance_log = {}

    for p_id, p_info in patterns.items():
        try:
            size = int(p_id.split('_')[1])
            f_key = f"size_{size}"
            
            f_cross = filters[f_key]['cross']
            f_x = filters[f_key]['x']
            p_input = p_info['input']
            expected = normalize_label(p_info['expected'])

            # MAC 계산 및 판정
            sc_cross = calculate_mac(p_input, f_cross)
            sc_x = calculate_mac(p_input, f_x)
            final_judge = judge(sc_cross, sc_x)
            
            if final_judge == expected:
                status = "PASS"
                pass_count += 1
            else:
                status = "FAIL"
                fail_count += 1
                
            print(f"- {p_id} | 내 판정: {final_judge} | 정답: {expected} | {status}")

            # 🌟 해당 사이즈의 성능 측정을 아직 안 했다면 1번만 측정해서 저장
            if size not in performance_log:
                performance_log[size] = measure_performance(p_input, f_cross)

        except Exception as e:
            print(f"- {p_id} | 에러 발생: {e} -> FAIL")
            fail_count += 1

    # 🌟 성능 표 출력하기
    print("\n# [3] 성능 분석 (평균/10회)")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    print("-" * 40)
    for sz in sorted(performance_log.keys()):
        print(f"{sz}x{sz:<8} {performance_log[sz]:<15.6f} {sz*sz}")

    print("\n# [4] 결과 요약")
    print(f"총 {pass_count + fail_count}개 테스트 중 | 통과: {pass_count}개 | 실패: {fail_count}개")


if __name__ == "__main__":
    print("=== Mini NPU 시뮬레이터 ===")
    print("1. 사용자 직접 입력 모드 (3x3)")
    print("2. JSON 파일 자동 분석 모드")
    choice = input("원하는 모드의 번호를 입력하세요: ")
    
    if choice == '1': run_mode_1()
    elif choice == '2': run_mode_2()
    else: print("1 또는 2를 입력해주세요.")