import csv

def save_to_file(jobs) :
  file = open("jobs.csv", mode = "w") 
  # 1. 먼저 파일을 열고
  # 2. 그 파일을 file이란 변수에 저장
  writer = csv.writer(file) 
  # 3. csv 파일을 작성
  writer.writerow(["title, company, location, link"])
  for job in jobs:
    writer.writerow(list(job.values())) #csv파일에 입력
  return