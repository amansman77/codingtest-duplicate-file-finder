import unittest
import os
from duplicate_finder import calculate_hash, find_duplicates

class TestDuplicateFinder(unittest.TestCase):
    
    def setUp(self):
        # 테스트용 디렉토리 및 파일 생성
        os.makedirs('test_dir/subdir', exist_ok=True)
        with open('test_dir/file1.txt', 'w') as f:
            f.write('Hello World')
        with open('test_dir/file2.txt', 'w') as f:
            f.write('Hello World')
        with open('test_dir/subdir/file3.txt', 'w') as f:
            f.write('Another file')
    
    def tearDown(self):
        # 테스트 파일 삭제
        import shutil
        shutil.rmtree('test_dir')
    
    def test_calculate_hash(self):
        hash1 = calculate_hash('test_dir/file1.txt')
        hash2 = calculate_hash('test_dir/file2.txt')
        hash3 = calculate_hash('test_dir/subdir/file3.txt')
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
    
    def test_find_duplicates(self):
        duplicates = find_duplicates('test_dir')
        self.assertTrue('test_dir/file1.txt' in [file for sublist in duplicates.values() for file in sublist])
        self.assertTrue('test_dir/file2.txt' in [file for sublist in duplicates.values() for file in sublist])
        self.assertFalse('test_dir/subdir/file3.txt' in [file for sublist in duplicates.values() for file in sublist])

if __name__ == '__main__':
    unittest.main()