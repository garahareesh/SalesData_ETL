pip install pandas
pip install openpyxl


Project : SalesData ETL and validation

This Project reads sales data from two different csv or excel files for different regions, applies business logic to transform data and loads it into a  Sqlite3database.
The database then queried for validation.

Run the program:
1.Set up environment
.Ensure Python 3 and SQLite are installed.
.install python required packages
    pip install pandas
    pip install openpyxl

2. Run the script
=======================
Place the excel files (order_region_a.xlsx and order_region_b.xlsx) in the same directory as the script.
Update the file paths in the script.
run the script python my_program.py


Database Setup:
======================
The script automatically creates and populates the SQLite database sales_data.db with the transformed data.

Business Rules Applied:
===========================
Combined data from both regions into a single table.
Calculated total_sales as QuantityOrdered * ItemPrice.
Added a region column to identify the sales region.
Removed duplicate entries based on OrderId.
Calculated net_sale as total_sales - PromotionDiscount.
Excluded records where net_sale was non-positive.

SQL Queries for Validation:
=============================
Count total records: SELECT COUNT(*) AS total_records FROM sales_data;
Total sales by region: SELECT region, SUM(total_sales) AS total_sales_amount FROM sales_data GROUP BY region;
Average sales per transaction: SELECT AVG(net_sale) AS average_sales_per_transaction FROM sales_data;
Check for duplicate OrderIds: SELECT OrderId, COUNT(OrderId) AS count FROM sales_data GROUP BY OrderId HAVING count > 1;
