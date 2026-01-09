create database blinkit;
select count(*) from blinkit_data;
select * from blinkit_data;
ALTER TABLE blinkit_data CHANGE COLUMN `Item Fat Content` item_fat_content VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Item Identifier` item_identifier VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `item_type` item_type VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Outlet Establishment Year` outlet_establishment_year VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Outlet Identifier` outlet_identifier VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Outlet Location Type` outlet_Location_Type VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Outlet Size` outlet_size VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Outlet Type` outlet_type VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Item Visibility` item_visibility VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Item Weight` item_weight VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `sales` total_sales VARCHAR(255);
ALTER TABLE blinkit_data CHANGE COLUMN `Rating` rating VARCHAR(255);
update blinkit_data set item_fat_content = case when 
item_fat_content in ('LF', 'low fat') then 'Low Fat'
when item_fat_content = 'reg' then 'Regular' else 
item_fat_content end ;
select distinct(item_fat_content) from blinkit_data;
select cast(sum(total_sales) / 1000000 as decimal(10,2)) as total_sales from blinkit_data;
select cast(avg(total_sales) as decimal(10,1)) as avg_sales from blinkit_data;
select count(*) as no_of_item from blinkit_data;
select cast(sum(total_sales) /1000000 as decimal(10,2)) as low_fat_sales from blinkit_data where item_fat_content = 'low fat';
select cast(avg(rating) as decimal(10,2)) as avgerage_rating from blinkit_data;
select * from blinkit_data;
select item_fat_content,
cast(sum(total_sales) as decimal(10,2)) as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating		
from blinkit_data group by item_fat_content order by total_sales desc;
select item_type,
cast(sum(total_sales) as decimal(10,2)) as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating
from blinkit_data group by item_type order by total_sales asc; 
select outlet_establishment_year,cast(sum(total_sales) as decimal(10,2))as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating
from blinkit_data group by outlet_establishment_year order by total_sales asc;  
select outlet_Location_Type,item_fat_content,
cast(sum(total_sales) as decimal(10,2)) as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating
from blinkit_data group by outlet_Location_Type,item_fat_content order by total_sales asc;
select * from blinkit_data;
SELECT Outlet_Size,
	CAST(SUM(Total_Sales) AS DECIMAL(10,2)) AS Total_Sales,
	CAST((SUM(Total_Sales) * 100.0/ SUM(SUM(Total_Sales)) OVER()) AS DECIMAL(10,2)) AS Sales_Percentage
FROM blinkit_data GROUP BY Outlet_Size ORDER BY Total_Sales DESC;
select outlet_Location_Type,cast(sum(total_sales) as decimal(10,2)) as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating
 from blinkit_data group by outlet_Location_Type;
 select outlet_type,cast(sum(total_sales) as decimal(10,2)) as total_sales,
cast(avg(total_sales) as decimal(10,1)) as avg_sales,
count(*) as no_of_item,
cast(avg(rating) as decimal(10,2)) as avgerage_rating
 from blinkit_data group by outlet_type;