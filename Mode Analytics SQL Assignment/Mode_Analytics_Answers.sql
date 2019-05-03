---- Databases used in analysis on Mode Analytics
-- tutorial.crunchbase_acquisitions
-- tutorial.crunchbase_companies
-- tutorial.crunchbase_investments


----  Question 1
-- First I did was to check to see if there were any duplicate names or companies within the database
-- From this query, we can see that there are 2 companies names 'Onemln' (A check to be sure)
-- 22421 distinct companies within the crunchbase_investments database
-- Explain about taking a deeper look at distinct country codes and region codes

select count(distinct company_name) from tutorial.crunchbase_investments

---- Question 1 Extra: Checking if any duplicates exist in dataset
select company_name, count(*)
from tutorial.crunchbase_investments
group by company_name
having COUNT(*) > 1

---- Question 2
-- Here, we had 22421 distinct companies in total, and after a where clause on the company name field, we see that there are 12880 companies from the USA
-- I am assuming we are worried about data integrity, therefore the decimal(8,3) was used in this query
-- To speed up this query, we could cast the values as float instead
with a as(
select distinct company_name, company_category_code, company_country_code
from tutorial.crunchbase_investments)

select sum(case when a.company_country_code = 'USA' then 1 else 0 end) as CNT_USA, 
count(distinct a.company_name) as CNT_TOT,
CAST((sum(case when a.company_country_code = 'USA' then 1 else 0 end)::decimal(8,3) / count(distinct a.company_name)::decimal(8,3))*100 AS DECIMAL(8,3)) AS PCT_USA
FROM a


---- Question 3
-- I am assuming we are only interested in the USA since the terminology 'State' is used in the question
-- I am also assumning we arelooking at the state with the highest investments 'RECIEVED' by a company
-- California has the highest total amount of investments recieved from investors at $396,572,671,008 USD

select company_state_code, sum(raised_amount_usd) as RAISED_AMOUNT_USD
from tutorial.crunchbase_investments
where company_country_code = 'USA'
group by company_state_code
order by RAISED_AMOUNT_USD desc;


---- Question 4
-- Domain Associates is the investor which invests the most money into biotech companies at $2,102,700,016 USD
select investor_name, investor_category_code, sum(raised_amount_usd) as RAISED_AMOUNT_USD from tutorial.crunchbase_investments
where company_category_code = 'biotech' 
and RAISED_AMOUNT_USD is not null
group by investor_name, investor_category_code
order by RAISED_AMOUNT_USD desc
;


---- Question 5
-- When discussing state, I am assuming the company state is the state that is being used
-- Assuming we are looking at individual series a investments, and not the total series a investment amount a company could recieve from multiple investments
-- I am also assuming we are only looking at the USA
-- the average individual series a investment  $17,946,039.22
select company_state_code, CAST(AVG(raised_amount_usd)AS DECIMAL(16,2)) as AVG_RAISED_AMOUNT
from tutorial.crunchbase_investments
where company_state_code = 'CA' and company_category_code = 'biotech' and funding_round_type = 'series-a'
group by company_state_code

---- Question 5 Extra: we can also look at all states where companies recieved investments
select company_state_code, CAST(AVG(raised_amount_usd)AS DECIMAL(16,2)) as AVG_RAISED_AMOUNT
from tutorial.crunchbase_investments
where company_category_code = 'biotech' and funding_round_type = 'series-a' AND RAISED_AMOUNT_USD IS NOT NULL
group by company_state_code
ORDER BY AVG_RAISED_AMOUNT DESC;


---- Question 6
-- Median series a investment amount for biotech companies in california is 13 million dollars
-- Assuming we are looking at individual series a investments, and not the total series a investment amount a company could recieve from multiple investments
select avg(raised_amount_usd) as median_investment_amount
from (
select raised_amount_usd from (
select company_name, raised_amount_usd, 
row_number() over (ORDER BY raised_amount_usd) as rownumber,
count(*) over() as rowcount
from tutorial.crunchbase_investments
where raised_amount_usd is not null and company_state_code = 'CA' and company_category_code = 'biotech' and funding_round_type = 'series-a') a
where rownumber in ((rowcount +1)/2, (rowcount+2)/2)) b;


---- Question 7 (Assuming we are looking for percentage of only )
-- Percentage of companies who recieved series a funding which are still operating
-- First part is determining how many companies recieved series - a funding
-- 63.12 % of companies are still operating after recieving Series A funding, 7501 Companies recieved Series A funding, 
with c as (
select distinct company_name as COMP from tutorial.crunchbase_investments
where funding_round_type = 'series-a'),
d as (
select distinct a.company_name as Operating from tutorial.crunchbase_investments a
join tutorial.crunchbase_companies b
on a.company_name = b.name
where a.funding_round_type = 'series-a' and b.status = 'operating')

SELECT COUNT(C.COMP) as TOTAL_COMPANIES, 
COUNT(D.OPERATING) AS OPERATING, CAST((COUNT(D.OPERATING)::DECIMAL / COUNT(c.comp)::DECIMAL)*100.00 AS DECIMAL(8,2)) AS PERCENT_OPERATING
FROM c
left join d
on c.COMP = d.operating

---- Question 8 (Same as above, looking for percentage of companies acquired after recieving Series A funding)
-- After doing a count of distinct company names in both the acquisitions table and the companies table, I am assuming the acquisitions table is more complete with its acquistion history
-- Therefore will compare between Investments and Acquisitons Table
-- Assuming we do not care when the company got acquired, as long as the company got series a funding and got acquired'
-- 10.27 % of companies were acquired after recieving Series A funding
with c as (
select distinct company_name as COMP from tutorial.crunchbase_investments
where funding_round_type = 'series-a'),
d as (
select distinct a.COMPANY_NAME as Acquired from tutorial.crunchbase_investments a
join tutorial.crunchbase_acquisitions b
ON a.company_name = b.company_name
where funding_round_type = 'series-a')

select count(C.COMP) AS TOTAL_COMPANIES,
COUNT(D.ACQUIRED) AS TOTAL_ACQUIRED,
CAST((COUNT(D.ACQUIRED)::DECIMAL / COUNT(c.comp)::DECIMAL)*100.00 AS DECIMAL(8,2)) AS PERCENT_ACQUIRED
FROM C
LEFT JOIN D
ON C.COMP = D.ACQUIRED

-- If we were concerned about the crunchbase_companies and crunchbase_acquisitions tables having different companies which were acquired
-- we could union the tables together based on company name to get a complete comprehensive list, and then conduct our left join using the same query structure as above

---- Question 8 Extra
-- Also, If we were worried about the date of acquisition, we could use a where clause in d where b.dateacquired > a.funded_at to address our prior assumption

with c as (
select distinct company_name as COMP from tutorial.crunchbase_investments
where funding_round_type = 'series-a'),
d as (
select distinct a.COMPANY_NAME as Acquired from tutorial.crunchbase_investments a
join tutorial.crunchbase_acquisitions b
ON a.company_name = b.company_name
where funding_round_type = 'series-a'
and b.dateacquired > a.funded_at)

select count(C.COMP) AS TOTAL_COMPANIES,
COUNT(D.ACQUIRED) AS TOTAL_ACQUIRED,
CAST((COUNT(D.ACQUIRED)::DECIMAL / COUNT(c.comp)::DECIMAL)*100.00 AS DECIMAL(8,2)) AS PERCENT_ACQUIRED
FROM C
LEFT JOIN D
ON C.COMP = D.ACQUIRED