Write a SQL query using a Common Table Expression (CTE)						
Combine online and store orders into a single dataset using UNION. Add a column channel with values 'online' or 'store' to distinguish the source.	



				
For each customer: 						
Calculate the total amount spent.


Determine the first and most recent purchase date.						
Compute the running total of amount spent ordered by order date using a window function.						
Filter the result to include only customers whose total amount spent > 300.	



					
Convert the order date to 'YYYY-MM' format and format the amount to 2 decimal places.						
Return: customer_id, customer_name, channel, order_month, order_amount, running_total, first_order_date, last_order_date. 


WITH CombinedOrders AS (
    SELECT 
        order_id,
        customer_id,
        customer_name,
        order_date,
        amount,
        'online' AS channel
    FROM online_orders

    UNION ALL

    SELECT 
        order_id,
        customer_id,
        customer_name,
        order_date,
        amount,
        'store' AS channel
    FROM store_orders
),

CustomerStats AS (
    SELECT 
        customer_id,
        SUM(amount) AS total_spent,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM CombinedOrders
    GROUP BY customer_id
),

DetailedOrders AS (
    SELECT 
        o.customer_id,
        o.customer_name,
        o.channel,
        TO_CHAR(o.order_date, 'YYYY-MM') AS order_month,
        ROUND(o.amount, 2) AS order_amount,
        SUM(o.amount) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total,
        cs.first_order_date,
        cs.last_order_date,
        cs.total_spent
    FROM CombinedOrders o
    JOIN CustomerStats cs 
        ON o.customer_id = cs.customer_id
)

SELECT 
    customer_id,
    customer_name,
    channel,
    order_month,
    ROUND(order_amount, 2) AS order_amount,
    ROUND(running_total, 2) AS running_total,
    TO_CHAR(first_order_date, 'YYYY-MM-DD') AS first_order_date,
    TO_CHAR(last_order_date, 'YYYY-MM-DD') AS last_order_date
FROM DetailedOrders
WHERE total_spent > 300
ORDER BY customer_id, order_month;
