import re

def load_config(filename):
    key_dict = dict()
    lock_dict = dict()
    count = 0
    with open("config\\"+filename, encoding="utf-8-sig") as config:
        for line in config:
            if line[-1] == '\n':
                line = line[:-1]

            # skip empty line or comments
            if len(line) == 0 or line[:2] == '//':
                continue

            k_idx = line.index('KEY') + 3
            slash_idx = line.index('/', k_idx)
            word = line[k_idx:slash_idx]

            left_part = line[:line.index("->")]
            if line[-2:] == "正确":
                if word in lock_dict:
                    lock_dict[word].append(left_part)
                else:
                    lock_dict[word] = [left_part]
                continue

            right_part = line[line.index("->")+2:]
            target_pos = "None"
            has_tilde = False
            need_merge = False
            if '~' in left_part:
                has_tilde = True
            if "MERGE" in right_part:
                need_merge = True
            if not need_merge:
                target_pos = right_part[right_part.index(">>")+2:]

            property_dic = {'left_part': left_part,
                            'right_part': right_part,
                            'has_tilde': has_tilde,
                            'target_pos': target_pos,
                           }

            if word in key_dict:
                if need_merge:
                    key_dict[word]['merge'].append(property_dic)
                else:
                    key_dict[word]['no_merge'].append(property_dic)
            else:
                if need_merge:
                    key_dict[word] = {'merge': [property_dic], 'no_merge': list(),}
                else:
                    key_dict[word] = {'merge': list(), 'no_merge': [property_dic],}

    return key_dict, lock_dict

def str_to_wordlist(s):
    l = s.split(" ")
    if l[-1] == '\n' or len(l[-1]) == 0:
        l = l[:-1]
    c = l.copy()
    for i in range(len(l)):
        l[i] = l[i][:l[i].index('/')]
    return c,l

def wordlist_to_str(l):
    temp_str = ""
    for haha in l:
        temp_str += haha + " "
    temp_str = temp_str[:-1] + '\n'
    return temp_str

def pattern_to_re_string(pattern, has_tilde=False):
    if "EOS" in pattern:
        pattern = pattern[:-4] + pattern[-3:]
    temp = pattern.replace("KEY","()").replace("BOS+","^").replace("EOS",r"\n").replace("+",r"\s").replace("2ANY",r"\w\w+").replace("ANY",r"\w+")
    if has_tilde:
        temp = temp.replace("~",".*")
    return temp

def letters_only(s):
    has_letter = False
    for i in s:
        if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z'):
            has_letter = True
        if not ((i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or (i >= '0' and i <= '9')):
            return False
    return has_letter

if __name__ == '__main__':
    filename = "demo.txt"
    key_dict, lock_dict = load_config("sampleconfig.txt")

    numeral = {"百万", "多半", "第一", "亿万", "好多", "万万", "万千", "大半"
           "半百", "好些", "百十", "小半", "十万", "好几", "大几", "多一半",
           "一多半"}

    punctuation = {"-","－","—","—","——","—－—","——","!","！","#","$","%","％",
               "&","(","（",")","）","*","＊",",","，","、",".","．","。",
               "/","／",":","：",";","；","?","？","@","[","［","\\","]","］"
               ,"^","_","{","|","}","~","～","‘","’","'","\"","“","”","〈",
               "〉","《","》","『","』","【","】","〔","〕","+","＋","<","＜"
               ,"=",">","＞","±","±","％","×","∶","▲","△","●","·","…","……","‰",}

    output_file = open("output\\" + filename, 'w', encoding="utf-8-sig")
    modification = open("output\\mod_" + filename, 'w', encoding="utf-8-sig")

    line_number = 0
    with open("..\\ictclas\\output_pku\\" + filename, encoding="utf-8-sig") as article:
        for line in article:
            line_number += 1
            if len(line) < 2:
                continue
            original_line = line
            if line[-1] == '\n':
                line = line[:-1]
            result_list = list()
            pattern_list = list()
            out_str = ""
            w_pos, wo_pos = str_to_wordlist(line)
            temp_line = line

            # repeat the below process two times to get a complete result
            for iter_times in range(2):
                # First, Deal With cases that need merge for each line
                # Repeat the process till no merge needed for this line
                has_merge = True
                while has_merge:
#                     print(line)
                    has_merge = False
                    need_break = False
                    for idx in range(len(wo_pos)):
                        if wo_pos[idx] in key_dict:
                            merge_check_list = key_dict[wo_pos[idx]]['merge']
                            for rule in merge_check_list:

#                                 dic_pos_list = rule['left_part'].split("+")
#                                 for dpl in dic_pos_list:
#                                     if 'KEY' in dpl:
#                                         dic_pos = dpl[dpl.index('/')+1:]
#                                 if dic_pos == w_pos[idx][w_pos[idx].index('/')+1:]:
#                                     continue
                                re_str = ""
                                if rule['has_tilde'] == False:
                                    re_str = pattern_to_re_string(rule['left_part'])
                                else:
                                    re_str = pattern_to_re_string(rule['left_part'],has_tilde=True)
                                re_obj = re.search(re_str, temp_line)
                                if re_obj is not None:
                                    k_s_idx = re_obj.regs[1][0]
#                                     print(temp_line)
#                                     print(k_s_idx)
                                    k_idx = 0
                                    for k_iter_idx in range(len(temp_line)):
                                        if k_iter_idx == k_s_idx:
                                            break
                                        if temp_line[k_iter_idx] == ' ':
                                            k_idx += 1

#                                     print(rule['left_part']+"->"+rule['right_part'])
#                                     print(w_pos)
#                                     print(k_idx)
                                    has_merge = True
                                    merge_bef = rule['right_part'][1:rule['right_part'].index('MERGE')-1]
                                    merge_aft = rule['right_part'][rule['right_part'].index('MERGE')+6:-1]
                                    merge_bef_list = merge_bef.split(" ")
                                    merge_aft_list = merge_aft.split(" ")
                                    merge_aft_list_nopos = merge_aft_list.copy()
                                    merge_bef_list_nopos = merge_bef_list.copy()
                                    for ite in range(len(merge_aft_list_nopos)):
                                        merge_aft_list_nopos[ite] = merge_aft_list_nopos[ite][:merge_aft_list_nopos[ite].index("/")]
                                    for ite in range(len(merge_bef_list_nopos)):
                                        merge_bef_list_nopos[ite] = merge_bef_list_nopos[ite][:merge_bef_list_nopos[ite].index("/")]
#                                     d_idx = 0
#                                     for i in range(len(wo_pos)-len(merge_bef_list_nopos)+1):
#                                         d_idx = i
#                                         has_find = True
#                                         for j in range(len(merge_bef_list_nopos)):
#                                             if wo_pos[i+j] != merge_bef_list_nopos[j]:
#                                                 has_find = False
#                                         if has_find:
#                                             break
                                    d_idx = k_idx

                                    result_before = ""
                                    for ite in range(len(merge_bef_list)):
                                        result_before += w_pos[d_idx] + " "
                                        del wo_pos[d_idx]
                                        del w_pos[d_idx]
                                    result_before = '[' + result_before[:-1] + ']'
                                    result_after = '[' + merge_aft + ']'
                                    result_list.append(result_before + "改为" + result_after)
                                    pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
                                    w_pos = w_pos[:d_idx] + merge_aft_list + w_pos[d_idx:]
                                    wo_pos = wo_pos[:d_idx] + merge_aft_list_nopos + wo_pos[d_idx:]
                                    temp_line = wordlist_to_str(w_pos)
#                                     print("temp_line   " + temp_line)
                                    need_break = True
                                    break
                            if need_break:
                                break

                ## KEY数字/t+年度/n->t正确
                re_str = "()[\d|一二三四五六七八九十百千万亿]/t\s年度/n"
                re_obj = re.search(re_str, temp_line)
                if re_obj is not None:
                    k_s_idx = re_obj.regs[1][0]
                    k_idx = 0
                    for k_iter_idx in range(len(temp_line)):
                        if k_iter_idx == k_s_idx:
                            break
                        if temp_line[k_iter_idx] == ' ':
                            k_idx += 1
                    wo_pos[k_idx] = "$$"

                ## Deal with "正确" Keyword
                for idx in range(len(wo_pos)):
                    if wo_pos[idx] in lock_dict:
                        for rule in lock_dict[wo_pos[idx]]:
                            re_str = pattern_to_re_string(rule)
                            re_obj = re.search(re_str, temp_line)
                            if re_obj is not None:
                                k_s_idx = re_obj.regs[1][0]
                                k_idx = 0
                                for k_iter_idx in range(len(temp_line)):
                                    if k_iter_idx == k_s_idx:
                                        break
                                    if temp_line[k_iter_idx] == ' ':
                                        k_idx += 1
                                wo_pos[k_idx] = "$$"

                ## Deal with "正确" with KEYANY
                for rule in lock_dict['ANY']:
                    re_str = pattern_to_re_string(rule)
                    re_obj = re.search(re_str, temp_line)
                    if re_obj is not None:
                        k_s_idx = re_obj.regs[1][0]
                        k_idx = 0
                        for k_iter_idx in range(len(temp_line)):
                            if k_iter_idx == k_s_idx:
                                break
                            if temp_line[k_iter_idx] == ' ':
                                k_idx += 1
                        wo_pos[k_idx] = "$$"

                # Deal with the process that Don't need merge
                # Only need direct assignment of pos to words
                for idx in range(len(wo_pos)):
                    if wo_pos[idx] == '$$':
                        continue
                    if wo_pos[idx] in key_dict:
                        check_list = key_dict[wo_pos[idx]]['no_merge']
                        for rule in check_list:
                            re_str = ""
                            if rule['has_tilde'] == False:
                                re_str = pattern_to_re_string(rule['left_part'])
                            else:
                                re_str = pattern_to_re_string(rule['left_part'],has_tilde=True)
                            re_obj = re.search(re_str, temp_line)
                            if re_obj is not None:
                                k_s_idx = re_obj.regs[1][0]
                                k_idx = 0
                                for k_iter_idx in range(len(temp_line)):
                                    if k_iter_idx == k_s_idx:
                                        break
                                    if temp_line[k_iter_idx] == ' ':
                                        k_idx += 1
                                if wo_pos[k_idx] == '$$':
                                    continue
                                if w_pos[k_idx][w_pos[k_idx].index('/')+1:] != rule['target_pos']:
                                    result_str = '[' + w_pos[k_idx] + ']改为['
                                    w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index('/')+1] + rule['target_pos']
                                    result_str += w_pos[k_idx] + ']'
                                    result_list.append(result_str)
                                    pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
                temp_line = wordlist_to_str(w_pos)

                # Deal with KEYANY
                check_keyany = key_dict['ANY']['no_merge']
                for rule in check_keyany:
                    re_str = ""
                    if rule['has_tilde'] == False:
                        re_str = pattern_to_re_string(rule['left_part'])
                    else:
                        re_str = pattern_to_re_string(rule['left_part'],has_tilde=True)
                    re_obj = re.search(re_str, temp_line)
                    if re_obj is not None:
                        k_s_idx = re_obj.regs[1][0]
                        k_idx = 0
                        for k_iter_idx in range(len(temp_line)):
                            if k_iter_idx == k_s_idx:
                                break
                            if temp_line[k_iter_idx] == ' ':
                                k_idx += 1
                        if wo_pos[k_idx] == '$$':
                            continue
                        if w_pos[k_idx][w_pos[k_idx].index('/')+1:] != rule['target_pos']:
                            result_str = '[' + w_pos[k_idx] + ']改为['
                            w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index('/')+1] + rule['target_pos']
                            result_str += w_pos[k_idx] + ']'
                            result_list.append(result_str)
                            pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
                temp_line = wordlist_to_str(w_pos)

                # Apply rule KEY数字/t+ANY/n->t>>m
                # Inclusing Chinese number 一二三四五六七八九十  百 千 万  >千万<  亿
                re_str = "()[\d|一二三四五六七八九十百千万亿]/t\s\w+/n"
                re_obj = re.search(re_str, temp_line)
                if re_obj is not None:
                    k_s_idx = re_obj.regs[1][0]
                    k_idx = 0
                    for k_iter_idx in range(len(temp_line)):
                        if k_iter_idx == k_s_idx:
                            break
                        if temp_line[k_iter_idx] == ' ':
                            k_idx += 1
                    if wo_pos[k_idx] == '$$':
                        continue
                    if w_pos[k_idx][w_pos[k_idx].index('/')+1:] != 'm':
                            result_str = '[' + w_pos[k_idx] + ']改为['
                            w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index('/')+1] + 'm'
                            result_str += w_pos[k_idx] + ']'
                            result_list.append(result_str)
                            pattern_list.append("KEY数字/t+ANY/n->t>>m")

            garbage = output_file.write(temp_line)
            if temp_line[:-1] != original_line[:-1]:

                ## write into modication file in proper format
                garbage = modification.write(str(line_number) + '\n')
                garbage = modification.write("<original_sent>" + original_line[:-1] + "\n</original_sent>" + '\n')
                garbage = modification.write("<modified_sent>" + temp_line[:-1] + "\n</modified_sent>" + '\n')
                garbage = modification.write("<pos_modification>" + '\n')
                for modi_i in range(len(result_list)):
                    garbage = modification.write('\t' + "<result>" + result_list[modi_i] + "</result>" + '\n')
                    garbage = modification.write('\t' + "<pattern>" + pattern_list[modi_i] + "</pattern>" + '\n')
                garbage = modification.write("</pos_modification>" + '\n' + '\n')

    output_file.close()
#     line_not_change.close()
    modification.close()
