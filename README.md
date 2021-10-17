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

```

## Model 2： BI-LSTM



```
python main.py
```


Based on the Github project https://github.com/linguishi/chinese_sentiment and codes can be found in Word2Vector.py, EvaluateInSampleAccuracy.py.

The labeling results (like top 5 negative/positive words) and in-sample performance is compared with the same CNN classifier trained on labels from the Chinese sentiment analysis project initiated by Qinghua University (the corpus can be found at https://github.com/InsaneLife/ChineseNLPCorpus)

(5) Conduct exactly the same exercise using reports and news title returning for the firm names from Wall Street Journal Chinese (as an example, the returning message for "Good Future Education" is https://www.wsj.com/search?query=TAL)

This part is now based on English language, classifier are trained and sentiment scores predicted using https://github.com/dragonAscent009/Stock-market-sentiment-analysis

(6) To sort of boost a causal analysis, I use the sentiment score retrieved from WSJ sample as an instrument for sentiment score constructed by guba (to the extent that market belief revealed from stock forum posts are formed by stock performance, here comes the endogeneity problem), controlling for other time-varying firm level variables correlated to both market sentiment and stock performance like Tobin's Q, firm size (proxied by log of total assets), leverage etc.

(7) I also conduct a time series analysis to evaluate the impulse response of stock price to sentiment score, and see how persistent the predictability of market sentiment on stock performance is.




 ## Reference

 [1] http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/

 [2] https://arxiv.org/abs/1408.5882

 [3] Kelly, Bryan T. and Manela, Asaf and Moreira, Alan, Text Selection (November 22, 2019). Available at SSRN: https://ssrn.com/abstract=3491942

 [4] Israel, Ronen and Kelly, Bryan T. and Moskowitz, Tobias J. and Moskowitz, Tobias J., Can Machines 'Learn' Finance? (January 10, 2020). Journal of Investment Management, Available at SSRN: https://ssrn.com/abstract=3624052 or [http://dx.doi.org/10.2139/ssrn.3624052](https://dx.doi.org/10.2139/ssrn.3624052)

 [5] Gu, Shihao and Kelly, Bryan T. and Xiu, Dacheng, Empirical Asset Pricing via Machine Learning (September 13, 2019). Chicago Booth Research Paper No. 18-04, 31st Australasian Finance and Banking Conference 2018, Yale ICF Working Paper No. 2018-09, Available at SSRN: https://ssrn.com/abstract=3159577 or [http://dx.doi.org/10.2139/ssrn.3159577](https://dx.doi.org/10.2139/ssrn.3159577)

 [6] Gentzkow, Matthew and Kelly, Bryan T. and Taddy, Matt, Text As Data (February 15, 2017). Available at SSRN: https://ssrn.com/abstract=2934001 or [http://dx.doi.org/10.2139/ssrn.2934001](https://dx.doi.org/10.2139/ssrn.2934001)
