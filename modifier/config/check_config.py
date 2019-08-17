with open("rest_hard_p.txt", encoding="utf-8-sig") as rh:
    for line in rh:
        line = line[:-1]
        if len(line) == 0 or line[:2] == '//':
            continue
        if "M" in line or "ER" in line or "R" in line or "G" in line:
            if "MERGE" not in line:
                print(line)
        if line.count("KEY") != 1:
            print(line)
        else:
            if "+" in line[line.index("->"):]:
                print(line)
    print("Finish")
