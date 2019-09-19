import re
import sys


class PosModifier:
    def __init__(self, filename, lock_file, config_files):
        self.line_number = 0
        self.lock_dict = dict()
        self.key_dicts = list()
        self.output_file = open("output\\" + filename, 'w', encoding="utf-8-sig")
        self.modification = open("output\\mod_" + filename, 'w', encoding="utf-8-sig")

        self.result_list = list()
        self.pattern_list = list()
        self.original_line = ""

        self.numeral = {"百万", "多半", "第一", "亿万", "好多", "万万", "万千", "大半"
                        "半百", "好些", "百十", "小半", "十万", "好几", "大几", "多一半",
                        "一多半"}

        self.punctuation = {"-", "－", "—", "—", "——", "—－—", "——", "!", "！", "#", "$", "%", "％",
                            "&", "(", "（", ")", "）", "*", "＊", ",", "，", "、", ".", "．", "。",
                            "/", "／", ":", "：", ";", "；", "?", "？", "@", "[", "［", "\\", "]", "］",
                            "^", "_", "{", "|", "}", "~", "～", "‘", "’", "'", "\"", "“", "”", "〈",
                            "〉", "《", "》", "『", "』", "【", "】", "〔", "〕", "+", "＋", "<", "＜",
                            "=", ">", "＞", "±", "±", "％", "×", "∶", "▲", "△", "●", "·", "…", "……", "‰", }

        self.load_lock_config(lock_file)
        self.load_config(config_files)

    def __del__(self):
        self.output_file.close()
        self.modification.close()

    def write_to_file(self, line):
        g = self.output_file.write(line + '\n')
        if line != self.original_line:
            # write into modification file in proper format
            g = self.modification.write("<line>" + str(self.line_number) + "</line>" + '\n')
            g = self.modification.write("<original_sent>" + self.original_line + "\n</original_sent>" + '\n')
            g = self.modification.write("<modified_sent>" + line + "\n</modified_sent>" + '\n')
            g = self.modification.write("<pos_modification>" + '\n')
            for modi_i in range(len(self.result_list)):
                g = self.modification.write('\t' + "<result>" + self.result_list[modi_i] + "</result>" + '\n')
                g = self.modification.write('\t' + "<pattern>" + self.pattern_list[modi_i] + "</pattern>" + '\n')
            g = self.modification.write("</pos_modification>" + '\n' + '\n')
        self.result_list.clear()
        self.pattern_list.clear()

    def load_lock_config(self, filename):
        lock_dict = dict()
        count = 0
        with open("config\\" + filename, encoding="utf-8-sig") as config:
            for line in config:
                if line.isspace() or len(line) == 0 or line[:2] == '//':
                    continue
                while line[-1].isspace():
                    line = line[:-1]

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
        self.lock_dict = lock_dict

    def load_config(self, filename_list):
        for filename in filename_list:
            key_dict = dict()
            count = 0
            with open("config\\" + filename, encoding="utf-8-sig") as config:
                for line in config:
                    if line.isspace() or len(line) == 0 or line[:2] == '//':
                        continue
                    while line[-1].isspace():
                        line = line[:-1]

                    try:
                        k_idx = line.index('KEY') + 3
                        slash_idx = line.index('/', k_idx)
                        word = line[k_idx:slash_idx]
                        left_part = line[:line.index("->")]
                        right_part = line[line.index("->") + 2:]
                        target_pos = "None"
                        has_tilde = False
                        need_merge = False
                        if '~' in left_part:
                            has_tilde = True
                        if "MERGE" in right_part:
                            need_merge = True
                        if not need_merge:
                            target_pos = right_part[right_part.index(">>") + 2:]

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
                                key_dict[word] = {'merge': [property_dic], 'no_merge': list(), }
                            else:
                                key_dict[word] = {'merge': list(), 'no_merge': [property_dic], }
                    except:
                        print("ERROR CONFIG: " + line + " in " + filename)
            self.key_dicts.append(key_dict)

    def str_to_wordlist(self, s):
        l = s.split(" ")
        c = l.copy()
        for i in range(len(l)):
            l[i] = l[i][:l[i].index('/')]
        return c, l

    def wordlist_to_str(self, l):
        temp_str = ""
        for haha in l:
            temp_str += haha + " "
        temp_str = temp_str[:-1]
        return temp_str

    def pattern_to_re_string(self, pattern, has_tilde=False):
        if "EOS" in pattern:
            pattern = pattern[:-4] + pattern[-3:]
        if "BOS" in pattern:
            pattern = pattern[:3] + pattern[4:]
        temp = pattern.replace("KEY", "()").replace("+", r"\s").replace("2ANY", r"\w\w+").replace("ANY", r"\w+")
        if has_tilde:
            temp = temp.replace("~", ".*")
        if "BOS" in pattern and "EOS" not in pattern:
            temp = temp.replace("BOS", "BOS ")
            return temp + " "
        elif "EOS" in pattern and "BOS" not in pattern:
            temp = temp.replace("EOS", " EOS")
            return " " + temp
        elif "EOS" in pattern and "BOS" in pattern:
            temp = temp.replace("EOS", " EOS").replace("BOS", "BOS ")
            return temp
        else:
            return " " + temp + " "

    def letters_only(self, s):
        has_letter = False
        for i in s:
            if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z'):
                has_letter = True
            if not ((i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or (i >= '0' and i <= '9')):
                return False
        return has_letter

    def various_modification(self, line):
        w_pos, wo_pos = self.str_to_wordlist(line)
        for idx in range(len(wo_pos)):
            if wo_pos[idx] in self.numeral:
                w_pos[idx] = w_pos[idx][:w_pos[idx].index('/') + 1] + 'm'
            if wo_pos[idx] in self.punctuation:
                w_pos[idx] = w_pos[idx][:w_pos[idx].index('/') + 1] + 'w'
            if self.letters_only(wo_pos[idx]):
                w_pos[idx] = w_pos[idx][:w_pos[idx].index('/') + 1] + 'nx'
        out_line = self.wordlist_to_str(w_pos)
        return out_line

    def apply_config(self, line, key_dict, use_lock):
        original_line = line

        w_pos, wo_pos = self.str_to_wordlist(line)
        temp_line = line

        # repeat the below process two times to get a complete result
        for iter_times in range(2):
            # First, Deal With cases that need merge for each line
            # Repeat the process till no merge needed for this line
            has_merge = True
            while has_merge:
                # print(line)
                has_merge = False
                need_break = False
                for idx in range(len(wo_pos)):
                    if wo_pos[idx] in key_dict:
                        # print(wo_pos[idx])
                        merge_check_list = key_dict[wo_pos[idx]]['merge']
                        for rule in merge_check_list:
                            re_str = ""
                            if rule['has_tilde'] == False:
                                re_str = self.pattern_to_re_string(rule['left_part'])
                            else:
                                re_str = self.pattern_to_re_string(
                                    rule['left_part'], has_tilde=True)
                            re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                            if re_obj is not None:
                                # print(rule)
                                k_s_idx = re_obj.regs[1][0] - 1
                                k_idx = 0
                                for k_iter_idx in range(len(temp_line)):
                                    if k_iter_idx == k_s_idx:
                                        break
                                    if temp_line[k_iter_idx] == ' ':
                                        k_idx += 1
                                has_merge = True
                                merge_bef = rule['right_part'][1:rule['right_part'].index('MERGE') - 1]
                                merge_aft = rule['right_part'][rule['right_part'].index('MERGE') + 6:-1]
                                merge_bef_list = merge_bef.split(" ")
                                merge_aft_list = merge_aft.split(" ")
                                # print(merge_bef_list)
                                # print(merge_aft_list)
                                merge_aft_list_nopos = merge_aft_list.copy()
                                merge_bef_list_nopos = merge_bef_list.copy()
                                for ite in range(len(merge_aft_list_nopos)):
                                    merge_aft_list_nopos[ite] = merge_aft_list_nopos[ite][:merge_aft_list_nopos[ite].index("/")]
                                for ite in range(len(merge_bef_list_nopos)):
                                    merge_bef_list_nopos[ite] = merge_bef_list_nopos[ite][:merge_bef_list_nopos[ite].index("/")]

                                d_idx = k_idx

                                result_before = ""
                                for ite in range(len(merge_bef_list)):
                                    result_before += w_pos[d_idx] + " "
                                    del wo_pos[d_idx]
                                    del w_pos[d_idx]
                                result_before = '[' + \
                                    result_before[:-1] + ']'
                                result_after = '[' + merge_aft + ']'
                                self.result_list.append(result_before + "改为" + result_after)
                                self.pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
                                w_pos = w_pos[:d_idx] + \
                                    merge_aft_list + w_pos[d_idx:]
                                wo_pos = wo_pos[:d_idx] + \
                                    merge_aft_list_nopos + wo_pos[d_idx:]
                                temp_line = self.wordlist_to_str(w_pos)
                                need_break = True
                                break
                        if need_break:
                            break

            # KEY数字/t+年度/n->t正确
            if use_lock:
                re_str = "()[\d|一二三四五六七八九十百千万亿]/t\s年度/n"
                re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                if re_obj is not None:
                    k_s_idx = re_obj.regs[1][0] - 1
                    k_idx = 0
                    for k_iter_idx in range(len(temp_line)):
                        if k_iter_idx == k_s_idx:
                            break
                        if temp_line[k_iter_idx] == ' ':
                            k_idx += 1
                    wo_pos[k_idx] = "$$"

            # Deal with "正确" Keyword
            if use_lock:
                for idx in range(len(wo_pos)):
                    if wo_pos[idx] in self.lock_dict:
                        for rule in self.lock_dict[wo_pos[idx]]:
                            re_str = self.pattern_to_re_string(rule)
                            re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                            if re_obj is not None:
                                k_s_idx = re_obj.regs[1][0] - 1
                                k_idx = 0
                                for k_iter_idx in range(len(temp_line)):
                                    if k_iter_idx == k_s_idx:
                                        break
                                    if temp_line[k_iter_idx] == ' ':
                                        k_idx += 1
                                wo_pos[k_idx] = "$$"

            # Deal with "正确" with KEYANY
            if use_lock:
                if 'ANY' in self.lock_dict:
                    for rule in self.lock_dict['ANY']:
                        re_str = self.pattern_to_re_string(rule)
                        re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                        if re_obj is not None:
                            k_s_idx = re_obj.regs[1][0] - 1
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
                            re_str = self.pattern_to_re_string(
                                rule['left_part'])
                        else:
                            re_str = self.pattern_to_re_string(
                                rule['left_part'], has_tilde=True)
                        re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                        if re_obj is not None:
                            k_s_idx = re_obj.regs[1][0] - 1
                            k_idx = 0
                            for k_iter_idx in range(len(temp_line)):
                                if k_iter_idx == k_s_idx:
                                    break
                                if temp_line[k_iter_idx] == ' ':
                                    k_idx += 1
                            if wo_pos[k_idx] == '$$':
                                continue
                            if w_pos[k_idx][w_pos[k_idx].index('/') + 1:] != rule['target_pos']:
                                result_str = '[' + w_pos[k_idx] + ']改为['
                                w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index(
                                    '/') + 1] + rule['target_pos']
                                result_str += w_pos[k_idx] + ']'
                                self.result_list.append(result_str)
                                self.pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
            temp_line = self.wordlist_to_str(w_pos)

            # Deal with KEYANY
            if 'ANY' in key_dict:
                check_keyany = key_dict['ANY']['no_merge']
                for rule in check_keyany:
                    re_str = ""
                    if rule['has_tilde'] == False:
                        re_str = self.pattern_to_re_string(rule['left_part'])
                    else:
                        re_str = self.pattern_to_re_string(
                            rule['left_part'], has_tilde=True)
                    re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
                    if re_obj is not None:
                        k_s_idx = re_obj.regs[1][0] - 1
                        k_idx = 0
                        for k_iter_idx in range(len(temp_line)):
                            if k_iter_idx == k_s_idx:
                                break
                            if temp_line[k_iter_idx] == ' ':
                                k_idx += 1
                        if wo_pos[k_idx] == '$$':
                            continue
                        if w_pos[k_idx][w_pos[k_idx].index('/') + 1:] != rule['target_pos']:
                            result_str = '[' + w_pos[k_idx] + ']改为['
                            w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index('/') + 1] + rule['target_pos']
                            result_str += w_pos[k_idx] + ']'
                            self.result_list.append(result_str)
                            self.pattern_list.append(rule['left_part'] + "->" + rule['right_part'])
                temp_line = self.wordlist_to_str(w_pos)

            # Apply rule KEY数字/t+ANY/n->t>>m
            # Inclusing Chinese number 一二三四五六七八九十  百 千 万  >千万<  亿
            re_str = "()[\d|一二三四五六七八九十百千万亿]/t\s\w+/n"
            re_obj = re.search(re_str, "BOS " + temp_line + " EOS")
            if re_obj is not None:
                k_s_idx = re_obj.regs[1][0] - 1
                k_idx = 0
                for k_iter_idx in range(len(temp_line)):
                    if k_iter_idx == k_s_idx:
                        break
                    if temp_line[k_iter_idx] == ' ':
                        k_idx += 1
                if wo_pos[k_idx] == '$$':
                    continue
                if w_pos[k_idx][w_pos[k_idx].index('/') + 1:] != 'm':
                    result_str = '[' + w_pos[k_idx] + ']改为['
                    w_pos[k_idx] = w_pos[k_idx][:w_pos[k_idx].index('/') + 1] + 'm'
                    result_str += w_pos[k_idx] + ']'
                    self.result_list.append(result_str)
                    self.pattern_list.append("KEY数字/t+ANY/n->t>>m")
        if temp_line[:3] == "@@ " and temp_line[-3:] == " @@":
            return temp_line[3:-3]
        else:
            return temp_line


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "demo.txt"

    lock_file = "lock_config.txt"
    config_files = ["absolute_priority.txt", "rest_hard_p.txt", "config_confident.txt", "config_conflict.txt",
                    "config_undecidable.txt", "config_lastname.txt", "hardword.txt", "rest_hard.txt", "sampleconfig.txt"]

    p = PosModifier(filename, lock_file, config_files)

    with open("..\\stanford\\output_pku\\" + filename, encoding="utf-8-sig") as article:
        article_lines = article.readlines()
        article_length = len(article_lines)
        for line in article_lines:
            p.line_number += 1
            # if p.line_number != 5310:
            #     continue
            if p.line_number % 100 == 0:
                print(str(p.line_number) + " / " + str(article_length))
            if line.isspace():
                continue
            while line[-1].isspace():
                line = line[:-1]

            p.original_line = line
            # print(line)
            line = p.various_modification(line)
            # print(line)
            line = p.apply_config(line, key_dict=p.key_dicts[0], use_lock=False)

            for i in range(1, len(p.key_dicts)):
                line = p.apply_config(line, key_dict=p.key_dicts[i], use_lock=True)
                # print(line)

            p.write_to_file(line)
