使用说明

1. 进入斯坦福分词器官网下载页面, 下载两样东西: 分词器 和 中文模组
    https://stanfordnlp.github.io/CoreNLP/download.html

2. 启动斯坦福分词服务器:
      java -Xmx12g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties -port 9000 -timeout 15000 -quiet true
