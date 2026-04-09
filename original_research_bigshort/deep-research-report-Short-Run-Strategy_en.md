# Executive Summary

Developing a *very short-term algorithmic trading system* based on supervised ML and social sentiment signals requires **several key pillars**: reliable data sources (market and social networks), sentiment indicators ("animal spirits"), network influencer analysis, ML models calibrated with bounded risk, and strict human monitoring with a **kill switch**. The literature suggests that hybrid approaches — combining technical and sentiment analysis — are the most promising【23†L43-L47】【21†L333-L341】. For example, models that integrate text and prices are strong candidates for a generalized strategy【23†L43-L47】. Twitter (now X) is a widely used data source for measuring "market temperature" in real time【14†L588-L597】【16†L58-L64】. Sentiment indicators can be extracted via NLP from tweets, and by crossing them with social network analysis we can detect **herd behavior** patterns and finfluencer influences. All of this feeds a supervised ML model that emits trading signals. It is essential to implement risk limits (positional, stop-loss) and an automatic kill switch that shuts down the algorithm in the event of anomalies【21†L333-L341】. The following sections detail these strategic design components.

## 1. Data Sources and Real-Time Extraction

**Capital markets**: The foundation consists of classic trading data (stock quotes, futures, currency pairs, indices) at intraday frequency (1m, tick). This data comes from official exchange or broker feeds (e.g., IBKR, Saxo), including prices, volumes, and depth.  

**Social networks (X/Twitter)**: To capture *market sentiment*, X offers APIs (streaming and REST) that allow real-time tweet collection. Libraries such as **Tweepy** in Python facilitate connection and message *streaming* by keywords or specific accounts【14†L588-L597】. According to IBKR, "Twitter… is widely used as a market sentiment indicator"【14†L588-L597】. Other sources (financial news, forums) can also complement this, but the focus here is X. Real-time collection (API stream) supplies an NLP engine.  

**Enriched data**: In addition to text, it is useful to include metadata: time, location, hashtags, and interaction networks (retweets, mentions). This allows inference of which *communities* are discussing specific assets. Data preparation involves cleaning (removing spam/noise), normalization (stemming, lemmatization), and tokenization.

## 2. Sentiment Indicators and "Animal Spirits"

**Market sentiment**: Quantitative indicators of investor mood are created. For example, a sentiment score (positive vs. negative) per asset, extracted from relevant tweets. According to a recent study, "sentiment analysis has enormous potential as a forecasting tool, providing information on market patterns and investor mood"【16†L23-L32】. Keynes defined *"animal spirits"* as the emotions (confidence, fear, euphoria) that drive the market【12†L252-L261】【12†L302-L310】. In this context, we identify atypical tweet volumes, sudden spikes in positive mentions, or emerging hashtags indicating euphoria or panic. For example, a rapid increase in optimistic comments can anticipate a bullish move even without solid economic news【12†L252-L261】.

**NLP and supervised ML**: Tweets are processed with NLP techniques (transformer-based models, BERT/RoBERTa adapted to finance, or lexicon+ML classification) to assign polarity and relevance. Finance-trained sentiment tools can be used (e.g., a "fear/greed" lexicon). With ML contributions, recent improvements have achieved greater precision in extracting the market's pulse【16†L23-L32】. A possible workflow: collect tweets with asset-related keywords → linguistic preprocessing → ML model that classifies sentiment and topics (e.g., *buy*, *sell*, *up*, *down*)【16†L23-L32】【23†L93-L100】.

**Composite metrics**: For each asset/sector, a *net sentiment* indicator can be defined — for example, the ratio of positive to negative tweets, or a mean score weighted by the sender's influence. Another indicator would be the percentage change in mentions (indicating euphoria). These signals are crossed with technical data (volatility, trend) to form final signals. Studies show that including sentiment data in ML models improves the accuracy of predicting market direction (not exact price)【4†L308-L310】.

## 3. Social Network Analysis and Influencer Identification

Herd emotions emerge in networks. Using **Social Network Analysis (SNA)** we can detect communities and influential figures. The work of Ku et al. (2023) proposes modeling Twitter as a directed network where influential users and connected groups are identified using metrics such as PageRank【10†L162-L170】【10†L271-L278】. In practice, we build a *graph* where nodes are users and edges represent interactions (retweets, mentions). SNA tools (NetworkX, Gephi) allow central influence to be calculated: "influencers are users with many followers and a high degree of engagement; they spread messages powerfully across the network"【10†L271-L278】.

**Communities and herd behavior**: By grouping users by topic (hashtags) and measuring the synchrony of their messages, we can detect gregarious behavior. For example, if a small group of *finfluencers* begins to promote an asset, the overall sentiment curve may spike. One strategy is to monitor "centers of mass" in the network: if a key influencer changes their tone, it can trigger trading avalanches (herd behavior). Studies show that in speculative markets (meme stocks, crypto) social networks dominate price dynamics【8†L81-L85】: "meme stock investors do not operate on fundamentals, but are sensitive to herd/sentiment movements"【8†L81-L85】.

In summary, we cross content analysis with SNA: a tweet carries more weight if it comes from a financial influencer in our network. Final indicators would include changes in activity of the most influential nodes (e.g., change in average sentiment of high-PageRank users) and network density metrics (looking for communication bursts).

## 4. Supervised Trading Model and Algorithmic Calibration

With sentiment signals and market variables, we train a supervised ML model that decides very short-term entries/exits. For example, classifiers (logistic regression, trees, neural networks) can be used that, given feature vectors (technical momentum + social mood), predict *intraday price direction*. The literature indicates that accuracy is limited (e.g., ~50–70%) and that hybrid approaches are better【23†L43-L47】【4†L308-L310】.  

**Features**: Typical variables include technical indicators (momentum, moving averages, volume, implied volatility), plus the social metrics mentioned above (net sentiment, changes in mentions, influencer activity). Every tick (minute, 5m, 1h) the algorithm collects this vector.  

**Training**: Supervised ML requires labeled data. For example, the next intraday return (positive/negative) can be used as a training label. The model is trained periodically using recent data (backtests over historical data) so that it "learns" the relationship between market sentiment and price movement. Ideally it is retrained daily/weekly to adapt to regime changes. [23] emphasizes that "the best models that combine sentiment and technicals" are ideal candidates【23†L43-L47】.

**Calibration and validation**: The model should be calibrated (hyperparameter tuning) with cross-validation methods using walk-forward validation. Given the look-ahead bias in high-frequency settings, time-block validation is preferred. Key metrics: directional accuracy, strategy Sharpe ratio, maximum drawdown. Research indicates that sentiment data increases *Sharpe* or directional accuracy【4†L308-L310】, but that overall performance remains moderate.

**Signal strategies**:  
- *Entries* when the model indicates a high probability of movement (e.g., >60% that price will rise/fall).  
- *Stop-Loss* and *Take-Profit* based on expected return ranges (to cap losses), configurable per scenario.  
- *Capital allocation*: given the high risk, it is recommended to diversify across several small ideas (e.g., do not invest everything in a single asset, but in a portfolio).  
- The algorithm can hedge long positions with shorts in the same sector (pair trades) if it detects opposing signals.

## 5. Human Supervision and Circuit-Breaker Mechanisms ("Kill Switch")

**Real-time control**: The proposed design requires a human supervisor to monitor continuously. Even though the system operates automatically, the human acts as the final circuit breaker. There must be a monitoring interface showing key metrics (intraday P&L, net exposure, anomaly indicators). For example, if drawdown exceeds a threshold, an alert is triggered.

**Kill switch**: Following best practices (FIA 2024)【21†L333-L341】, a *kill switch* is implemented that instantly halts all algorithmic trading. According to the guide, "a kill switch…immediately disables all trading activity…preventing new orders and canceling pending ones"【21†L333-L341】. This mechanism should be used as a last resort in the face of critical errors (e.g., model out of bounds, abnormally volatile market, unexpected losses).

**Cutoff rules**: Possible triggers include:
- **Loss limit**: exposure of capital (e.g., –5% intraday) activates automatic cutoff.  
- **Data disconnection**: failure in data ingestion (market or Twitter) suspends trading.  
- **Dissonant signals**: if technical signals and sentiment diverge strongly, it may indicate corrupted data.  
- **Latency anomalies**: execution delays force a stop.  

Additionally, manual supervision allows the model to be retrained or adjusted on the fly if *drift* is detected (a change in the signal-market relationship). While the human watches, "the strategy should only operate under supervision, so that in the event of a losing trend the algorithm can be stopped immediately" (problem requirement).

## 6. Backtesting, Stress Tests, and Operational Metrics

Before going to production, simulation is performed with historical data and simulators:
- **Backtest with tweets**: a historical tweet archive (e.g., archived data) synchronized with prices is required. The strategy is recreated minute by minute, validating returns.  
- **Shock simulations**: crisis scenarios, "flash crashes," or market breakdowns (e.g., COVID, geopolitical events) to see how the model responds.  
- **Metrics**: daily Sharpe and Sortino coefficients, % of profitable days, maximum drawdown over the simulated period, signal accuracy. Also influencer network metrics: with what lead time does sentiment change before the market?  

**Operational indicators**: Because of the very short-term nature, latencies are monitored (time between signal and order), slippage, and order fill rate. In a diversified portfolio, variance across assets is tracked. For example, success can be measured with the accumulated P&L vs. time chart, and correlation with sentiment indicators.  

## 7. Risk and Ethical Considerations

This system is *high-risk* due to its ultra-short horizon and reliance on unorthodox social signals. It must be noted that even with supervision, investments can lose significantly. Regulations must be followed (e.g., not using private information, respecting X's API terms of service) and data privacy must be managed. Furthermore, given the "best effort" approach, it must be warned that results depend critically on correct calibration and continuous vigilance. As Investopedia notes regarding *"animal spirits"*, emotions can generate **bubbles or panics** that escape fundamental analysis【12†L252-L261】【12†L302-L310】. The system proposes to take advantage of these dynamics, but with strict loss limits and active supervision.

In summary, the strategic pillars are: (1) real-time trading and social media data feed; (2) NLP processing to produce mood indicators; (3) network analysis to identify herd behavior and key influencers; (4) a supervisedly trained ML model that combines those signals with classical techniques; and (5) an operational architecture with human monitoring and immediate stop mechanisms【21†L333-L341】【23†L43-L47】. With this skeleton, a very short-term *algorithmic strategy* can be implemented — diversified and high-risk — oriented toward obtaining daily gains while the supervisor is active.

**Sources:** Academic literature and algorithmic trading guides recommend combining technical analysis with social sentiment【23†L43-L47】【16†L23-L32】. The use of Twitter/X as a sentiment source is common in quantitative trading systems【14†L588-L597】【16†L58-L64】. Risk practices insist on having a supervised kill switch to stop runaway algorithms【21†L333-L341】, and recent studies confirm that social network herding can move prices (meme stocks) independently of fundamentals【8†L81-L85】. These findings support the approach proposed here.
