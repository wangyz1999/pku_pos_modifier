## 应用模式：

1.  输入一篇文档，应用斯坦福分词器进行中文分词，并给予词性，生成分词词性文档。
    词性标注为滨州树库标准，应用词性转换，将词性变为北京大学词性标注集(pku)

2.  输入一篇文档，应用Ictclas分词器进行中文分词，并给予词性，生成分词词性文档。
    词性标注为Ictclas标准，应用词性转换，将词性变为北京大学词性标注集(pku)

3.  输入pku词性标注后的文档，使用词性修正器对词性进行修正，输出pku标准的分词词性文档


## Config文档介绍:

1. 输入格式

	模式包括模式左部（匹配规则）和模式右部（具体改动），每个模式的输入格式为

							"左部->右部"

1.2. 左部: 左部由若干子模式组成， 子模式 _i_ 的基本形式为：

1)	组合体，形式为：
    * ANY/词性，其中ANY表示任意单词
    * 词/ANY，其中ANY表示任意词性
    * 2ANY 表示对应的词或词性的字数一定是两个或以上

2)	特殊符号：
	* EOS 表示句子结尾 End of Sentence
	* BOS 表示句子开头 Beginning of Sentence
    * KEY 搜索中会先查找是否有 KEY 所在的词，然后搜索和此词对应的所有config  

子模式的组合方式："子模式1+子模式2+…+子模式n"，"+"可被 "\~" 替换，"\~" 表示分隔的两个词之间可以有多个词。
举例:

1.3. 右部: 右部有三种形式：
  1. [词性]正确 --- 表示该词性为正确, 这会将词性锁住，防止其他config修改
  2. [词性A]>>[词性B] --- 表示修改词性A为词性B
  3. [组合1]MERGE[组合2] --- 将组合1变为组合2

#### 一些细节
1. 在当前的代码, MERGE 模式中, 左边子模式的数量一定不能等于右边自模式的数量, 如果只是想修改词的词性而不重新分词，请采用 [词性A]>>[词性B] 的形式
2. MERGE 模式中, KEY一定指代的是方括号内的第一个字(词)

#### 举例

	修改前: 感/v 兴趣/n 的/u 朋友/n 不妨/d 多/a 了/u 解下/v

	修改理由: KEY多/v+了/u+解下/v->[多/v 了/u 解下/v]MERGE[多/d 了解/v 下/f]

	修改后: 感/v 兴趣/n 的/u 朋友/n 不妨/d 多/d 了解/v 下/f



##  此程序中的词性对照
##### 注: 以下表格只有 Ictclas -> pku 或 Stanford -> pku 之间转换的对应， 并不存在 Ictclas 和 Stanford 之间的关系
##### Stanford 的词性中, NR 代表了人名，地名，和机构名, 这里将其全部转换为了ns (待解决问题)

| Ictclas | pku    | Stanford |
| --------| ------ | -------- |
| n       | n      | NN       |
| nr      | nr     |          |
| nr1     | nr     |          |
| nr2     | nr     |          |
| nrj     | nr     |          |
| nrf     | nr     |          | 
| nrf     | nr     |          |
| ns      | ns     | NR       |
| nsf     | ns     | NR       |
| nt      | nt     |          |
| nz      | nz     |          |
| ng      | Ng     |          |
| n_new   | n      | NN       |
| njtgj   | n      | NN       |
| ntbj    | n      | NN       |
| ntsa    | n      | NN       |
| ntzj    | n      | NN       |
| 词性    | n      | NN       |
| nthub   | n      | NN       |
| ntyr    | n      | NN       |
| ntsd    | n      | NN       |
| ntyn    | n      | NN       |
| ntsh    | n      | NN       |
|n_newword| n      | NN       |
| ntzy    | n      | NN       |
| ntgm    | n      | NN       |
| ntss    | n      | NN       |
| ntxz    | n      | NN       |
| nttj    | n      | NN       |
| ntcq    | n      | NN       |
| ntes    | n      | NN       |
| ntuk    | n      | NN       |
| ntsx    | n      | NN       |
| ntme    | n      | NN       |
| ntgx    | n      | NN       |
| ntqc    | n      | NN       |
| ntit    | n      | NN       |
| ntsc    | n      | NN       |
| ntqz    | n      | NN       |
| nthun   | n      | NN       |
| ntah    | n      | NN       |
| ntcb    | n      | NN       |
| ntrqg   | n      | NN       |
| nthen   | n      | NN       |
| nthan   | n      | NN       |
| ntdc    | n      | NN       |
| ntgd    | n      | NN       |
| ntjs    | n      | NN       |
| ntjj    | n      | NN       |
| nswyy   | n      | NN       |
| nthk    | n      | NN       |
| 新增    | n      | NN       |
| ntdb    | n      | NN       |
| ntz     | n      | NN       |
| nv      | n      | NN       |
| ntan    | n      | NN       |
| nthl    | n      | NN       |
| ntgz    | n      | NN       |
| ntau    | n      | NN       |
| ntqg    | n      | NN       |
| ntkr    | n      | NN       |
| ntjx    | n      | NN       |
| ntjd    | n      | NN       |
| ntsz    | n      | NN       |
| ntkrn   | n      | NN       |
| nttc    | n      | NN       |
| ntjp    | n      | NN       |
| nms     | n      | NN       |
| ntjk    | n      | NN       |
| ntthk   | n      | NN       |
| ntfj    | n      | NN       |
| ntjl    | n      | NN       |
| ntheb   | n      | NN       |
| ntrs    | n      | NN       |
| nttw    | n      | NN       |
| ntcj    | n      | NN       |
| ntus    | n      | NN       |
| ntgs    | n      | NN       |
| ntot    | n      | NN       |
| ntcn    | n      | NN       |
| nttqg   | n      | NN       |
| ntln    | n      | NN       |
| ntts    | n      | NN       |
| ntfr    | n      | NN       |
| dg      | Dg     |          |
| yxz     | y      | SP       |
| yxb     | y      | SP       |
| t       | t      | NT       |
| tg      | tg     |          |
| s       | s      |          |
| f       | f      | LC       |
| v       | v      | VV       |
| vshi    | v      | VC       |
| vyou    | v      | VE       |
| vf      | v      | VV       |
| vx      | v      | VV       |
| vi      | v      | VV       |
| vd      | vd     |          |
| vn      | vn     |          |
| vg      | vg     |          |
| a       | a      | VA       |
| ad      | ad     |          |
| an      | an     |          |
| ag      | Ag     |          |
| al      | l      |          |
| nl      | l      |          |
| vl      | l      |          |
| dl      | l      |          |
| bl      | l      |          |
| b       | b      | JJ       |
| z       | z      |          |
| r       | r      | PN       |
| rr      | r      | PN       |
| rz      | r      | PN       |
| rzt     | r      | PN       |
| rzs     | r      | PN       |
| rzv     | r      | PN       |
| ry      | r      | PN       |
| ryt     | r      | PN       |
| rys     | r      | PN       |
| ryv     | r      | PN       |
| rg      | r      | PN       |
| Rg      | r      | PN       |
| R       | r      | PN       |
|         | r      | DT       |
| m       | m      | CD       |
| mq      | m      | CD       |
| Mg      | m      | CD       |
|         | m      | OD       |
| q       | q      | M        |
| qv      | q      | M        |
| qt      | q      | M        |
| d       | d      | AD       |
| p       | p      | P        |
| P       | p      | P        |
| pba     | p      | P        |
| pbei    | p      | P        |
| c       | c      | CS       |
| cc      | c      | CS       |
| u       | u      | DEC      |
|         | u      | DEG      |
|         | u      | DER      |
|         | u      | DEV      |
| uzhe    | u      |          |
| ule     | u      |          |
| uguo    | u      |          |
| ude1    | u      |          |
| ude2    | u      |          |
| ude3    | u      |          |
| usuo    | u      |          |
| udeng   | u      |          |
| uyy     | u      |          |
| udh     | u      |          |
| uls     | u      |          |
| uzhi    | u      |          |
| ulian   | u      |          |
| e       | e      | IJ       |
| y       | y      | SP       |
| o       | o      | ON       |
| h       | h      |          |
| k       | k      |          |
| x       | nx     | X        |
| xx      | nx     | X        |
| xu      | nx     | X        |
| News    | nx     | X        |
| xe      | nx     | X        |
| 术      | nx     | X        |
|         | nx     | FW       |
|         | nx     | URL      |
| w       | w      | PU       |
| wkz     | w      | PU       |
| wky     | w      | PU       |
| wyz     | w      | PU       |
| wyy     | w      | PU       |
| wj      | w      | PU       |
| ww      | w      | PU       |
| wt      | w      | PU       |
| wd      | w      | PU       |
| wf      | w      | PU       |
| wn      | w      | PU       |
| wm      | w      | PU       |
| ws      | w      | PU       |
| wp      | w      | PU       |
| wb      | w      | PU       |
| wh      | w      | PU       |
|         | P      | LB       |
|         | P      | SB       |
|         | P      | BA       |




