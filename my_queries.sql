"Count the total number of records."

SELECT COUNT(*) as total_number FROM sales_data;

"Find the total sales amount by region."

SELECT region, SUM(total_sales) as total_sales_amount FROM sales_data GROUP BY region

"Find the average sales amount per transaction."

SELECT AVG(net_sale) as average_sale_transaction FROM sales_data

"Ensure there are no duplicate OrderId values."

SELECT OrderId, COUNT(OrderId) as count FROM sales_data GROUP BY OrderId HAVING count >1