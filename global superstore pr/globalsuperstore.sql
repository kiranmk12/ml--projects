use [sql works]
select * from global_superstore_clean

select top 10 * from global_superstore_clean


begin transaction

alter table global_superstore_clean drop column postal_code
commit transaction


-- these are the most consistent customers who buys consistently from us
select top 10 customer_name,customer_id , count(order_id) as no_of_orders from global_superstore_clean group by customer_name,customer_id
   order by no_of_orders desc 


-- checking on customers who purchased the least .
-- reason  customer may not be satified with the product, maybe damaged , maybe not satisfied witht the price
----may found a new vendor
-- we need to give the same importance as the top customers because of the possibility of churn
---we can send mail etc to get their attraction

select top 20 customer_name,customer_id , count(order_id) as no_of_orders from global_superstore_clean group by customer_name,customer_id
   order by no_of_orders asc


--- to find the customers who stand in between these two 
-- if we wont  give attention to them they might loose 


select avg(no_of_orders) as avg_order 
   from (select customer_name,customer_id , count(order_id) as no_of_orders 
    from global_superstore_clean group by customer_name,customer_id
       ) as order_count
select customer_name,customer_id , count(order_id) as no_of_orders from global_superstore_clean 
  group by customer_name,customer_id
   having count(order_id)  between 25 and 40 
   



--which country's customer purchases from us the most

select country, count(order_id) as top_orders from global_superstore_clean 
   group by country order by top_orders desc

   -- united states shows the strongest customer base - so we need to improve the services here 
   -- from position 2 to 12 they also shows customer base and so improving the services helps us to grow
   --13-65 weaker less order have been recieved from here . they are not consistent
   -- 66-147 the weakest .these have the most chance to churn if we dont focus on them


   -- even if the orders  count is high on some countries that doesnt shows the 
   --- the profits are as high as the order counts 
   ---- so we need to verify it

select country,sum(profit) profit_gained,count(order_id)as order_count from global_superstore_clean  group by country
    order by profit_gained desc

	      --- from this united states stayed on top 
		  -- while others have shown a big diiference 
		  --- high order count with less profit and less order count with higher profit

		  -- reason heavy discount, shipping ,import cost etc
		  

--which shipment mode  is more used in each country


select country,Ship_Mode,count(order_id) as count_ from global_superstore_clean group by rollup(country,Ship_Mode)
    order by count_ desc


--avg shipping duration per country

select Country, avg(shipping_duration) as avg_processing_days from global_superstore_clean group by Country
order by avg_processing_days desc


-- category demands in each country

select Country ,Category,count(order_id) as cat_imp from global_superstore_clean
     group  by Country,category order by Country,cat_imp desc