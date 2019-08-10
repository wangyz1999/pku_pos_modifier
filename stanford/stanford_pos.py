import sys
from nltk.parse import corenlp

def cpt_to_pku(cpt):
    dic = {
        'VA': 'a',
        'VC': 'v',
        'VE': 'v',
        'VV': 'v',
        'NR': 'ns',
        'NT': 't',
        'NN': 'n',
        'LC': 'f',
        'PN': 'r',
        'DT': 'r',
        'CD': 'm',
        'OD': 'm',
        'M': 'q',
        'AD': 'd',
        'P': 'p',
        'CC': 'c',
        'CS': 'c',
        'DEC': 'u',
        'DEG': 'u',
        'DER': 'u',
        'DEV': 'u',
        'SP': 'y',
        'AS': 'u',
        'ETC': 'u',
        'MSP': 'u',
        'IJ': 'e',
        'ON': 'o',
        'PU': 'w',
        'JJ': 'b',
        'FW': 'nx',
        'LB': 'P',
        'SB': 'P',
        'BA': 'P',
        'URL': 'nx',
        'X':'nx',
    }
    pku = list()
    for idx in range(len(cpt)):
        if idx != len(cpt)-1 and cpt[idx][1] == 'VA' and cpt[idx+1][1] in ['VC','VE','VV']:
            p = 'ad'
        else:
            p = dic[cpt[idx][1]]
        pku += [(cpt[idx][0],p)]
    return pku



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("please provide one txt filename")
    else:
        filename = sys.argv[1]
        parser = corenlp.CoreNLPParser(url='http://localhost:9000',tagtype='pos')
        cpt_file = open("output_cpt\\" + filename, 'w', encoding="utf-8-sig")
        pku_file = open("output_pku\\" + filename, 'w', encoding="utf-8-sig")
        with open("input\\" + filename, encoding="utf-8-sig") as file:
            for line in file:
                cpt_pos = parser.tag(line.split())
                pku_pos = cpt_to_pku(cpt_pos)
                cpt_file.write(' '.join(i[0] + '/' + i[1] for i in cpt_pos) + '\n')
                pku_file.write(' '.join(i[0] + '/' + i[1] for i in pku_pos) + '\n')

        cpt_file.close()
        pku_file.close()
