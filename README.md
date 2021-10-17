# Chinese Sentiment Analysis - Finance

This project concentrates on Chinese sentiment analysis, particularly for financial field, in which a unique feature is that the practitioners and academics speak the same jargon.

The project includes

(1) Web scraping stock forum comments from http://guba.eastmoney.com/, where most of the comments are circulated among noise investors, while the sentimental (more likely to be irrational) contents can be rich;

(2) Retrieve "risk event" breakpoints from wind database and construct event-based labeled sample. 

The fundamental problems I have to solve is the lack of annotated training samples. Even though I conduct some labor intensive work involving labeling the sentiment tags (positive, negative or neutral?), the labels can be rather subjective and suffer from a loss of generality. 

So the basic idea is to identify "bad news" / "good news" using objective capital market events, which means a belief agreement among investors that the corresponding firm is bad / good. 

In particular, I identified degrading/default event/negative profit revealed from financial reports/eminently unfavorable policy announcement to be "bad news", and upgrading/profit boom/eminently favorable policy announcement to be "good news", and comments three days after "good news" are labeled as POSITIVE, and those after "bad news" are labeled as NEGATIVE. 

The basic rationale is that "good news" and "bad news" are observed by sophisticated capital market (a common knowledge which should be priced) and the justification is market wide so it's more objective and convincing. Of course, we can enrich this identification strategy by including richer capital market variations, like including the financial crisis and some macro events, there can be a lot of flexibility, adapted to research interest.

The wind functions (APIs required) are in allComments.xlsx, and the identification of events in IdentifyEvents.do.

(3) Use jieba cut project from https://github.com/fxsjy/jieba to pre-process and lemmatize the comments.

The files in RawData folders contain the comment data scraped from guba, they contain the title of the post (basically a sentence showing the blogger's feeling), the number of views and comments of the post, and time of posting.

I then use jieba cut, which is a Github project focusing on lemmatizing Chinese words in particular. Technical details and indispensable modifications to facilitate usage can be found in the Github project, and related functions are defined in jiebacut.py.

(4) Construct my Chinese financial market corpus, train a **CNN** classifier and evaluate in-sample accuracy. (Following Gentzkow, Kelly, and Taddy (2018), I also tried an **LSTM** model, the results are basically the same.)

## Model 1：CNN

#### Structure：

1. Chinese Embedding
2. Convolutional  layer with multiple filter widths and feature maps
3. Max-over-time pooling, generates the maximum one for each filter
4. Fully connected layer with dropout and softmax output

 ![截图](http://www.wildml.com/wp-content/uploads/2015/11/Screen-Shot-2015-11-06-at-8.03.47-AM-1024x413.png)
source: https://arxiv.org/abs/1408.5882 , note that in this paper, the authors adopted a double channel with both pre-trained embeddings and untrained embeddings. But here I use a pre-trained embeddings only.



#### CNN模型的训练结果

在`model`目录底下运行

```
python score_report.py cnn/results/score/eval.preds.txt
```

输出：

```
              precision    recall  f1-score   support

         POS       0.91      0.87      0.89       400
         NEG       0.88      0.91      0.89       400

   micro avg       0.89      0.89      0.89       800
   macro avg       0.89      0.89      0.89       800
weighted avg       0.89      0.89      0.89       800

```

## 模型二： BI-LSTM

1. 中文词Embedding
2. bi-lstm
3. 全连接

![截图](https://raw.githubusercontent.com/linguishi/chinese_sentiment/master/pic/1_GRQ91HNASB7MAJPTTlVvfw.jpeg)


BI-LSTM模型的训练，在`lstm`目录底下运行 

```
python main.py
```

#### BI-LSTM模型训练时间

在**GTX 1060 6G**的加持下大概耗时5分钟

#### BI-LSTM模型的训练结果

在`model`目录底下运行

```
python score_report.py lstm/results/score/eval.preds.txt
```

输出：

```
              precision    recall  f1-score   support

         POS       0.90      0.87      0.88       400
         NEG       0.87      0.91      0.89       400

   micro avg       0.89      0.89      0.89       800
   macro avg       0.89      0.89      0.89       800
weighted avg       0.89      0.89      0.89       800

```

### 模型的导出和serving（BI-LSTM为例）

#### 模型导出

在`lstm`目录底下运行 

```
python export.py
```

导出`estimator`推断图，可以用作prediction。本项目已上传了`saved_model`，可以不通过训练直接测试。

在`model/lstm`目录底下运行 `python serve.py`可以利用导出的模型进行实体识别。详情见代码。

测试结果

![截图](https://raw.githubusercontent.com/linguishi/chinese_sentiment/master/pic/clip.png)

虽然模型由真实评论数据训练而成，这些数据长短不一（有的分词后长度超过1000），但由上图可得，模型对短评论表现尚可。

Based on the Github project https://github.com/linguishi/chinese_sentiment and codes can be found in Word2Vector.py, EvaluateInSampleAccuracy.py.

The labeling results (like top 5 negative/positive words) and in-sample performance is compared with the same CNN classifier trained on labels from the Chinese sentiment analysis project initiated by Qinghua University (the corpus can be found at https://github.com/InsaneLife/ChineseNLPCorpus)

(5) Conduct exactly the same exercise using reports and news title returning for the firm names from Wall Street Journal Chinese (as an example, the returning message for "Good Future Education" is https://www.wsj.com/search?query=TAL)

This part is now based on English language, classifier are trained and sentiment scores predicted using https://github.com/dragonAscent009/Stock-market-sentiment-analysis

(6) To sort of boost a causal analysis, I use the sentiment score retrieved from WSJ sample as an instrument for sentiment score constructed by guba (to the extent that market belief revealed from stock forum posts are formed by stock performance, here comes the endogeneity problem), controlling for other time-varying firm level variables correlated to both market sentiment and stock performance like Tobin's Q, firm size (proxied by log of total assets), leverage etc.

(7) I also conduct a time series analysis to evaluate the impulse response of stock price to sentiment score, and see how persistent the predictability of market sentiment on stock performance is.



### code environment
在 python3.6 & Tensorflow1.13 下工作正常

其他环境也许也可以，但是没有测试过。

还需要安装 `scikit-learn` package 来计算指标，包括准确率回召率和F1因子等等。

### 语料的准备
语料的选择为 *谭松波老师的评论语料*，正负例各2000。属于较小的数据集，本项目包含了原始语料，位于`data/hotel_comment/raw_data/corpus.zip`中

解压 `corpus.zip` 后运行，并在`raw_data`运行
```sh
python fix_corpus.py
```
将原本`gb2312`编码文件转换成`utf-8`编码的文件。

### 词向量的准备
本实验使用开源词向量[*chinese-word-vectors*](https://github.com/Embedding/Chinese-Word-Vectors)

选择知乎语料训练而成的Word Vector, 本项目选择词向量的下载地址为 https://pan.baidu.com/s/1OQ6fQLCgqT43WTwh5fh_lg ,需要百度云下载，解压，直接放在工程目录下

### 训练数据的格式
参考 `data/hotel_comment/*.txt` 文件

- step1

本项目把数据分成训练集和测试集，比例为`4:1`, 集4000个样本被分开，3200个样本的训练集，800的验证集。

对于训练集和验证集，制作训练数据时遵循如下格式：
在`{}.words.txt`文件中，每一行为一个样本的输入，其中每段评论一行，并用`jieba`分词，词与词之间用空格分开。
```text
除了 地段 可以 ， 其他 是 一塌糊涂 ， 惨不忍睹 。 和 招待所 差不多 。
帮 同事 订 的 酒店 , 他 老兄 刚 从 东莞 回来 , 详细 地问 了 一下 他 对 粤海 酒店 的 印象 , 说 是 硬件 和 软件 : 极好 ! 所以 表扬 一下
```
在`{}.labels.txt`文件中，每一行为一个样本的标记
```text
NEG
POS
```
本项目中，可在`data/hotel_comment`目录下运行`build_data.py`得到相应的格式

- step2

因为本项目用了`index_table_from_file`来获取字符对应的id，需要两个文件表示词汇集和标志集，对应于`vocab.labels.txt`和`vocab.words.txt`,其中每一行代表一个词或者是一行代表一个标志。

本项目中，可在`data/hotel_comment`目录下运行`build_vocab.py`得到相应的文件

- step3

由于下载的词向量非常巨大，需要提取训练语料中出现的字符对应的向量，对应本项目中的`data/hotel_comment/w2v.npz`文件

本项目中，可在`data/hotel_comment`目录下运行`build_embeddings.py`得到相应的文件



 ## Reference

 [1] http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/

 [2] https://arxiv.org/abs/1408.5882

 [3] Kelly, Bryan T. and Manela, Asaf and Moreira, Alan, Text Selection (November 22, 2019). Available at SSRN: https://ssrn.com/abstract=3491942

 [4] Israel, Ronen and Kelly, Bryan T. and Moskowitz, Tobias J. and Moskowitz, Tobias J., Can Machines 'Learn' Finance? (January 10, 2020). Journal of Investment Management, Available at SSRN: https://ssrn.com/abstract=3624052 or [http://dx.doi.org/10.2139/ssrn.3624052](https://dx.doi.org/10.2139/ssrn.3624052)

 [5] Gu, Shihao and Kelly, Bryan T. and Xiu, Dacheng, Empirical Asset Pricing via Machine Learning (September 13, 2019). Chicago Booth Research Paper No. 18-04, 31st Australasian Finance and Banking Conference 2018, Yale ICF Working Paper No. 2018-09, Available at SSRN: https://ssrn.com/abstract=3159577 or [http://dx.doi.org/10.2139/ssrn.3159577](https://dx.doi.org/10.2139/ssrn.3159577)

 [6] Gentzkow, Matthew and Kelly, Bryan T. and Taddy, Matt, Text As Data (February 15, 2017). Available at SSRN: https://ssrn.com/abstract=2934001 or [http://dx.doi.org/10.2139/ssrn.2934001](https://dx.doi.org/10.2139/ssrn.2934001)