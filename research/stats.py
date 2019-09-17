from multiprocessing import Process
import re


def to_re_str(words):
    words = words.replace('.', '\.').replace('+', '\+')
    words = words.split(" ")
    re_str = ""
    for w in words:
        re_str += w + "/\w+ "
    return " " + re_str


def find_seg_count(word, iors):
    dic = dict()
    for i in range(1, 138):
        if iors == 'i':
            with open("I_study\\study" + str(i) + ".txt", encoding="utf-8-sig") as nd:
                text = "$ " + nd.read().replace("\n", " ") + " $"
                for t in re.findall(to_re_str(word), text):
                    t = t[1:-1]
                    if t not in dic:
                        dic[t] = 1
                    else:
                        dic[t] += 1
        else:
            with open("S_study\\study" + str(i) + ".txt", encoding="utf-8-sig") as nd:
                text = "$ " + nd.read().replace("\n", " ") + " $"
                for t in re.findall(to_re_str(word), text):
                    t = t[1:-1]
                    if t not in dic:
                        dic[t] = 1
                    else:
                        dic[t] += 1
    return dic


def run(r, dic, thread):
    with open("threads\\" + str(r[0]) + "_" + str(r[1]) + ".txt", 'w', encoding='utf-8-sig') as wr:
        big_dic = {}
        count = 0
        t_count = 0
        gap = r[1] - r[0]
        for key in dic:
            count += 1
            if count < r[0] or count > r[1]:
                continue
            t_count += 1
            if t_count % 5 == 0:
                print(thread + ": " + str(t_count) + " / " + str(gap))

            seg_set = {key}
            for k in dic[key]["I_segs"]:
                seg_set.add(k)
            for k in dic[key]["S_segs"]:
                seg_set.add(k)

            i_segs = dict()
            s_segs = dict()

            atime = 0
            for word in seg_set:
                i_pos_freq = find_seg_count(word, 'i')
                s_pos_freq = find_seg_count(word, 's')

                if len(i_pos_freq) != 0:
                    i_pos_freq_sum = sum(i_pos_freq.values())
                    i_segs[word] = {"frq": i_pos_freq_sum, "pos": i_pos_freq}
                    atime += i_pos_freq_sum

                if len(s_pos_freq) != 0:
                    s_pos_freq_sum = sum(s_pos_freq.values())
                    s_segs[word] = {"frq": s_pos_freq_sum, "pos": s_pos_freq}
                    atime += s_pos_freq_sum

            big_dic[key] = {"a_time": atime,
                            "i_segs": i_segs, "s_segs": s_segs}
            g = wr.write(key + '\t' + str(big_dic[key]) + '\n')


if __name__ == '__main__':
    dic = {}
    with open("mwords.txt", encoding="utf-8-sig") as mw:
        dic = eval(mw.read())

    thread_num = 5
    total_data_num = 20000
    gap = total_data_num // thread_num

    dic_list = list()
    for i in range(thread_num):
        dic_list.append(dic.copy())

    process_list = list()
    for i in range(thread_num):
        r = [i * gap, (i + 1) * gap - 1]
        t_name = "t" + str(i + 1)
        process_list.append(Process(target=run, args=(r, dic_list[i], t_name)))

    for i in range(thread_num):
        process_list[i].start()

    for i in range(thread_num):
        process_list[i].join()

    print("Finshed !")
