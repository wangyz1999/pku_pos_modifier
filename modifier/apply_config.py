
def load_config(filename):
    key_dict = dict()
    lock_dict = dict()
    count = 0
    with open("config\\"+filename, encoding="utf-8-sig") as config:
        for line in config:
            if line[:-1] == '\n':
                line = line[:-1]

            try:
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
            except:
                print(line)

    return key_dict, lock_dict
