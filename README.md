应用模式：

1.	输入一篇文档，应用斯坦福分词器进行中文分词，并给予词性，生成分词词性文档。
词性标注为滨州树库标准，应用词性转换，将词性变为北京大学词性标注集(pku)

2.	输入一篇文档，应用Ictclas分词器进行中文分词，并给予词性，生成分词词性文档。
词性标注为Ictclas标准，应用词性转换，将词性变为北京大学词性标注集(pku)

3.	输入pku词性标注后的文档，使用词性修正器对词性进行修正，输出pku标准的分词词性文档
