# Mode Analytics Questionnaire and Answers

## Part 1

### Look to answer the questions below and include the following:
- a brief answer to the questions; please clearly state your assumptions and the logic of your solution
- your SQL code; you may include an external link (Google Doc or Mode Report) to reference your source code

### You may use some or all of the following tables to answer the following questions from the Mode tutorial database:
- tutorial.crunchbase_acquisitions
- tutorial.crunchbase_companies
- tutorial.crunchbase_investments

### Questions
1. **How many companies are included in the crunchbase investment dataset?**
2. **What percentage of those companies are located in the United States?**
3. **What state has the highest total investments?**
4. **What investor contributes the most to biotech companies in the United States?**
5. **What is the average Series A investment amount for biotech companies in California?**
6. **What is the median Series A investment amount for biotech companies in California?**
7. **What percentage of companies which received a Series A are operating?**
8. **What percentage of companies which received a Series A were acquired?**

## Part 2

### In addition, complete the following question. Think of presenting your findings in a report format, and as if a client were to read over it. 
9. What conclusions can you draw about the best location to obtain Series A funding for a software company? Support your answer with data and/or visualizations.

## Part 1 Answers
1. I assumed that you are interested in looking at the number of unique companies that are included in the crunchbase investment dataset. I used a count distinct company_name query to determine that there were **22421 distinct companies within the crunchbase_investments dataset.** Using a count(distinct) query takes into account if there are any duplicate records inside the dataset.
2. I assumed that we are looking at distinct companies inside the crunchbase_investments dataset once again. **57.45 % of companies inside the crubchbase_investments dataset are located inside the United States.** I used a CTE query with a case when statement to calculate the number of companies which are located inside the USA.I used the total count of companies from question 1 as my denominator, and I used the count of companies inside the USA as my numerator.
3. I assumed that we are only looking at companies inside the USA since the term ‘state’ was used in the question. **California has the highest total amount of investments received from investors at $396,572,671,008 USD.** For this question, I used a group by statement to list all of the States with investments, and the sum of all of those investments. The order by descending statement was used so that the first row of the table is the state with the highest total investments.
4. **Domain Associates is the investor which invests the most money into biotech companies at $2,102,700,016 USD.** I again used a group by clause to get a list of all investors which have invested in Biotech companies (where clause stating company category = ‘biotech’), and the sum of all those investments. The order by descending statement was used so that the first row of the table is the investor with the highest total investments to biotech companies. 
5. I am Assuming we are looking at the average individual Series A investment a company receives, and not the total Series A investment amount a company could receive from multiple investments. **The average individual Series A investment for biotech companies in California is $17,946,039.22 USD.** Again, a group by statement was used to show the state, and the average investment amount. The where clause was used to filter for Series A funding for Biotech companies in California.
6. I am assuming that we are looking at the median individual Series A investment a company receives, and not the total Series A investment amount a company receives from multiple investments. **The Median Series A investment amount for biotech companies in california is 13 million dollars USD.** Since SQL doesn’t have a Median method, i had to use subqueries to solve this issue. I assigned a column containing row numbers after ordering the table from the smallest investment to the largest investment. The second subquery obtains the middle row(s) in the table regardless if there are an even or odd number of rows. The last part of the query then averages the investment amount from the middle row(s) to obtain the median. 
7. **63.12 % of companies are still operating after recieving Series A funding. 7501 Companies received Series A funding, and 4735 of these companies are still operating.** This question i used a CTE query to get our result. The first part of the question was getting a count of distinct companies with Series A funding from the crunchbase_investments dataset. The second part of the question involved grabbing the count of distinct companies which received Series A funding and are still operating. This required an inner join between the crunchbase_investments dataset and the crunchbase_companies dataset in order to get this information. Lastly, we would use the information from the first part as our denominator, and the information from the second part as our numerator, and did division between the two counts to get our percentage.
8. For this question I opted to use the crunchbase_investments dataset and the crunchbase_acquisitions dataset, as the crunchbase_acquisitions dataset had a more complete history of company acquisitions. I am assuming we do not care when the company got acquired, as long as the company got series a funding and got acquired. **10.27 % of companies were acquired after recieving Series A funding. 7501 Companies received Series A funding, and 770 of these companies were acquired.** The first part of the question was getting a count of distinct companies with Series A funding from the crunchbase_investments dataset. The second part of the question involved grabbing the count of distinct companies which received Series A funding and were acquired. This required an inner join between the crunchbase_investments dataset and the crunchbase_acquisitions dataset. Lastly, we would use the information from the first part as our denominator, and the information from the second part as our numerator, and did division between the two counts to get our percentage. 

### The answer and report for Part 2 will be stored on a PDF document within the same repository
