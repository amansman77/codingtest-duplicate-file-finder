# Coding Challenge #75 - Duplicate File Finder

`John Crickett` 이 만든 코딩 챌린지 [75번째 문제](https://www.linkedin.com/pulse/coding-challenge-75-duplicate-file-finder-john-crickett-pcqme/)입니다.

## 문제

This challenge is to build your own version of a file deduplication tool. These tools are useful for finding duplicate files that can be deleted to free up storage space.

For many of us this probably isn’t a problem we face often, but it’s enough of a problem that several tools exist, including fdupes written in C. It’s fairly readable code, so even if you don’t fancy writing your own tool, you could learn more about the techniques used by reading the code for fdupes.

There are several uses for deduplication and the techniques used for identifying duplicate files. The first is obviously to find duplicate files and remove them freeing up storage space. Another common use is to exclude duplicate files from backups.

When we extend this to enterprise level backups they also often use these techniques to find duplicates within files to further reduce the storage (and network bandwidth) requirements.

### Aside: Performance Quiz - The Answer
Last week I asked readers of Coding Challenges this question: if we re-wrote Docker in Python, what impact would it have on the performance of the containers you run?

The correct answer is that it would have no impact on the performance of the containers that you run. Docker is simply doing some configuration with Linux namespaces and cgroups and then running another process (your container) within those namespaces. The runtime is therefore completely unaffected by the language used to develop Docker.

To really understand Docker, check out the build your own Docker challenge. By building your own Docker, you’ll gain a deeper understanding of Docker and become a better software engineer.

###Question: Should I Build A Course On How To Build Your Own Docker?
If you think so, and would be interested, please sign up to the waitlist. If there is enough interest I’ll build a course that explains how to create your own solution to the Docker Coding Challenge in Python, Go and Rust.

Anyone on the waitlist will be offered a 50% discount.

### If You Enjoy Coding Challenges Here Are Three Ways You Can Help Support It
1. Refer a friend or colleague to the newsletter. 🙏
2. Sign up for a paid subscription - think of it as buying me a coffee ☕️ twice a month, with the bonus that you also get 20% off any of my courses.
3. Buy one of my courses that walk you through a Coding Challenge.

### The Challenge - Building A Duplicate File Finder
In this coding challenge we’ll be building a command line tool that can scan a directory to identify and remove duplicate files.

### Step Zero
Like all the best programming languages we’re zero indexed!

For this step, I’ll leave you to setup your IDE / editor of choice and programming language of choice. After that here’s what I’d like you to do to be ready to test your solution:

```bash
for i in {1..20}; do dd if=/dev/urandom bs=100 count=1 of=file$i; done
cp file1 file21 
```

You can tweak this to create more files (change the 1..20 to use a bigger range), or different sized files (change the value of bs). The cp command then ensures we have a duplicate, feel free to create more duplicates for testing.

Please make your testing more complete by creating subdirectories and ensuring there are duplicate files in different levels of the directory hierarchy you create.

### Step 1
In this step your goal is to accept and directory in the command line and then scan that directory and list all the files in it recursively. That should look something like this:

```bash
% ccdupe .
file1
file2
subdir/file11
subdir/anothersubdir/file21 
```

### Continued...
You can find the remaining steps for this challenge on the Coding Challenges Substack here.

## 프로젝트 구조

```
duplicate_finder.py
setup.py
test_duplicate_finder.py
performance_test.py
```

## 프로젝트 실행 방법

```bash
python setup.py install
ccdupe .
```

## 테스트 방법

### 단위 테스트

```bash
python test_duplicate_finder.py
```

### 성능 테스트

```bash
python performance_test.py
```

성능 테스트 결과는 다음과 같습니다.

```bash
Created 22000 files with 10 duplicates each.

Serial Execution Time    : 0.35 seconds
Parallel Execution Time  : 0.15 seconds
Speedup                  : 2.30x faster using parallel processing
```

