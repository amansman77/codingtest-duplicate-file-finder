import hashlib
import os
import argparse
from multiprocessing import Pool, cpu_count
import logging

def setup_logging(log_file="duplicate_finder.log"):
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def calculate_hash(file_path, hash_algo='sha256', chunk_size=8192):
    """
    파일의 해시 값을 계산합니다.

    Args:
        file_path (str): 해시를 계산할 파일의 경로.
        hash_algo (str, optional): 사용할 해시 알고리즘. 기본값은 'sha256'.
        chunk_size (int, optional): 파일을 읽을 청크 크기. 기본값은 8192 바이트.

    Returns:
        str: 계산된 해시 값 또는 오류 시 None.
    """
    hasher = hashlib.new(hash_algo)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, PermissionError) as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_duplicates(directory):
    """
    지정된 디렉토리 내에서 중복 파일을 찾습니다.

    Args:
        directory (str): 중복 파일을 찾을 디렉토리 경로.

    Returns:
        dict: 해시 값을 키로 하고, 동일 해시를 진 파일 경로 리스트를 값으로 하는 딕셔너리.
    """
    hash_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = calculate_hash(full_path)
            if file_hash:
                if file_hash in hash_dict:
                    hash_dict[file_hash].append(full_path)
                else:
                    hash_dict[file_hash] = [full_path]
    duplicates = {hash_val: paths for hash_val, paths in hash_dict.items() if len(paths) > 1}
    logging.info(f"Found {len(duplicates)} groups of duplicate files.")
    return duplicates

def remove_duplicates(duplicates, keep_one=True):
    """
    중복 파일을 삭제합니다.

    Args:
        duplicates (dict): 중복 파일 그룹을 포함하는 딕셔너리.
        keep_one (bool, optional): 각 그룹에서 하나의 파일을 유지할지 여부. 기본값은 True.
    """
    for hash_val, files in duplicates.items():
        if keep_one:
            # 첫 번째 파일을 제외하고 삭제
            files_to_delete = files[1:]
        else:
            files_to_delete = files
        print(f"\nDeleting files with hash {hash_val}:")
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

def calculate_hash_wrapper(args):
    return calculate_hash(*args)

def find_duplicates_parallel(directory):
    hash_dict = {}
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    
    with Pool(cpu_count()) as pool:
        hashes = pool.map(calculate_hash, file_paths)
    
    for file_path, file_hash in zip(file_paths, hashes):
        if file_hash:
            if file_hash in hash_dict:
                hash_dict[file_hash].append(file_path)
            else:
                hash_dict[file_hash] = [file_path]
    
    duplicates = {hash_val: paths for hash_val, paths in hash_dict.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Duplicate File Finder")
    parser.add_argument("directory", help="Directory to scan for duplicates")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete duplicate files")
    parser.add_argument("-e", "--exclude", nargs='*', help="List of directories to exclude")
    parser.add_argument("-f", "--extensions", nargs='*', help="List of file extensions to include")
    args = parser.parse_args()
    
    duplicates = find_duplicates(args.directory, exclude=args.exclude, extensions=args.extensions)
    
    # 중복 파일을 화면에 출력
    for hash_val, files in duplicates.items():
        print(f"Hash: {hash_val}")
        for file in files:
            print(f"  {file}")
    
    if args.delete:
        remove_duplicates(duplicates, keep_one=True)
    
if __name__ == "__main__":
    setup_logging()
    main()