import os
import shutil
import time
import hashlib
from duplicate_finder import find_duplicates, find_duplicates_parallel

def create_test_files(base_dir, num_files=1000, num_duplicates=100):
    """
    테스트 디렉토리에 중복 파일을 생성합니다.
    
    Args:
        base_dir (str): 파일을 생성할 기본 디렉토리.
        num_files (int, optional): 생성할 고유 파일의 수. 기본값은 1000.
        num_duplicates (int, optional): 각 고유 파일당 생성할 중복 파일의 수. 기본값은 100.
    """
    os.makedirs(base_dir, exist_ok=True)
    unique_content = [f"This is unique content for file {i}" for i in range(num_files)]
    
    # 생성된 파일 저장 경로 리스트
    file_paths = []
    
    for i, content in enumerate(unique_content):
        file_name = f"file_{i}.txt"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)
        file_paths.append(file_path)
        
        # 중복 파일 생성
        for j in range(1, num_duplicates + 1):
            duplicate_file_name = f"file_{i}_dup_{j}.txt"
            duplicate_file_path = os.path.join(base_dir, duplicate_file_name)
            shutil.copy(file_path, duplicate_file_path)
            file_paths.append(duplicate_file_path)
    
    print(f"Created {len(file_paths)} files with {num_duplicates} duplicates each.")

def measure_execution_time(func, *args, **kwargs):
    """
    주어진 함수의 실행 시간을 측정합니다.
    
    Args:
        func (callable): 실행할 함수.
        *args: 함수에 전달할 위치 인자.
        **kwargs: 함수에 전달할 키워드 인자.
        
    Returns:
        float: 함수의 실행 시간(초 단위).
        any: 함수의 반환 값.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, result

def main():
    test_dir = "test_duplicates"
    
    # 기존 테스트 디렉토리가 있다면 삭제
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # 테스트 파일 생성
    create_test_files(test_dir, num_files=2000, num_duplicates=10)  # 총 22,000 파일 생성
    
    # find_duplicates() 실행 및 시간 측정
    print("\nRunning find_duplicates()...")
    time_serial, duplicates_serial = measure_execution_time(find_duplicates, test_dir)
    print(f"find_duplicates() took {time_serial:.2f} seconds.")
    
    # find_duplicates_parallel() 실행 및 시간 측정
    print("\nRunning find_duplicates_parallel()...")
    time_parallel, duplicates_parallel = measure_execution_time(find_duplicates_parallel, test_dir)
    print(f"find_duplicates_parallel() took {time_parallel:.2f} seconds.")
    
    # 결과 비교
    print("\nPerformance Comparison:")
    print(f"Serial Execution Time    : {time_serial:.2f} seconds")
    print(f"Parallel Execution Time  : {time_parallel:.2f} seconds")
    speedup = time_serial / time_parallel if time_parallel > 0 else float('inf')
    print(f"Speedup                  : {speedup:.2f}x faster using parallel processing")
    
    # 테스트 후 정리
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    main()