使用说明
===

1. 安装分词器: 进入斯坦福分词器官网下载页面, 下载两样东西: 分词器 和 中文模组
	https://stanfordnlp.github.io/CoreNLP/download.html

2. 启动斯坦福分词服务器: 启动指令可以在官网查看
	https://stanfordnlp.github.io/CoreNLP/corenlp-server.html

```bash
java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties -port 9000 -timeout 15000
```
	
	* 可以用 -Xmx4g 分配所需要的内存
	* 注意添加 -serverProperties StanfordCoreNLP-chinese.properties 表明处理中文
	* 添加 -quiet true 可以在分词时不将结果输出到控制台中

	* 可以将指令写入脚本,如 "start_nlp_server.bat" 方便以后启动
 
3. 输入输出文件夹说明: 可以分别进入这三个文件夹查看其中的 demo.txt 来更清楚了解
	
	* input 文件夹放入需要进行文字处理的 txt 文档 (注意中文处理的txt文档编码格式必须为 utf-8)
	* output_cpt 文件夹将输出斯坦福分词器的结果文档, cpt 意为 Chinese Penn Treebank (宾州中文树库)
	* output_pku 文件夹将输出转换为pku词性的文档, pku 意为 Peking University (北京大学词性标注集)
    
4.  
    1. 将斯坦福分词服务器启动（方法查看步骤2）
    2. 将需要进行分词的文档放入 input 文件夹
    3. 运行 "stanford_pos.py" 程序获得 cpt 和 pku 两种词性文档
   
