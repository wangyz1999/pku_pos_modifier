使用说明
===

1. 安装分词器: 进入 ictclas github 页面, 下载 ictclas 分词器
	https://github.com/NLPIR-team/NLPIR

2. 启动ictclas分词器, 并自行使用其对文档进行分词, 将分词结果放在 output_ict 文件夹内
* 使用说明请参考官方说明文档

3. 输入输出文件夹说明: 可以分别进入这三个文件夹查看其中的 demo.txt 来更清楚了解

	* input 用于存放原文档, 可以将此文件夹在 ictclas 中设置为默认输入文件夹, 若不需要可以无视此文件夹
	* output_ict 文件夹将存放 ictclas 分词结果文档, 可以将此文件夹在 ictclas 中设置为默认输出文件夹, 或自行将输出文档复制到此文件夹中
	* output_pku 文件夹将输出转换为pku词性的文档, pku 意为 Peking University (北京大学词性标注集)

4.  分词步骤:
    1. 启动 ictclas 分词系统, 并自行使用其对文档进行分词
    2. 将分词结果放在 output_ict 文件夹内
    3. 运行 "ictclas_pos.py" 程序将 ictclas 词性标注集 转换为 pku 词性标注集
