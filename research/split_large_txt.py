import os

study = open("study.txt", encoding='gbk',errors='ignore')

count = 0

while True:
    count += 1
    file_name = "study" + str(count) + ".txt"
    with open("splits\\" + file_name, 'w', encoding="utf-8") as temp:
        while os.stat("splits\\" + file_name).st_size / 1024 < 2000:
            temp.write(study.readline())



info = os.stat("study.txt")
print(type(info))
print(info)
