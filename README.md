# Value-Weighted-Portfolio-using-Size-and-BM-ratio
Compared performance of simple portfolio strategies based on value-weighted size and b/m ratio factors

# Data
Used data downloaded from [Wharton Research Data Services]('ds-web.wharton.upenn.edu') 2003 ~2018

# Portfolio Strategies
* Different stocks were selected and value-weighted every month</br>
* How stocks were selected for each startegy:</br>
      - 10% Smallest market capital (str1)</br>
      - 35% Top B/M ratio (str2)</br>
      - 50% Largest market capital and 35% Top B/M ratio (str3)</br>
      - 50% Smallest market capital and 35% Top B/M ratio (str4)</br>

# Performane Comparison Criteria and Insights
![](/Performance2.png)
## Sharpe Ratio
* __Sharpe Ratio of Each Strategy before 2009__</br>
![](/Sharpe_before2009.png)</br>
* __Sharpe Ratio of Each Strategy after 2009__</br>
![](/Sharpe_after2009.png)</br>
* __Insights__</br>
     From the results, the most obvious finding is “str2”, “str3” and “str4” all having very low sharpe ratios before 2009, and relatively high values after 2009, while “str1” has a much more stable result within both periods.</br>
This indicates that size premiums may be more robust when compared with value premiums.

## Fama-French
* The insignificance of alpha for all of the portfolios indicates that these four portfolios could not beat the Fama French Model benchmark.
* Coefficients of SMB and HML represents which factor does each strategy weight on
