CREATE TABLE Customers (
  customer_id INT PRIMARY KEY,
  name VARCHAR(100),
  segment ENUM('Consumer','Corporate','Small Business') NOT NULL,
  city VARCHAR(80),
  country VARCHAR(80)
);
CREATE TABLE Suppliers (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  city VARCHAR(80),
  country VARCHAR(80)
);
CREATE TABLE Products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(120),
  category VARCHAR(80),
  unit_price DECIMAL(10,2),
  supplier_id INT,
  FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);
CREATE TABLE Orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  status ENUM('Pending','Shipped','Cancelled') NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
CREATE TABLE OrderItems (
  order_item_id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  qty INT,
  unit_price DECIMAL(10,2),
  discount DECIMAL(4,2) DEFAULT 0, -- e.g., 0.10 = 10%
  FOREIGN KEY (order_id) REFERENCES Orders(order_id),
  FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
CREATE TABLE Payments (
  payment_id INT PRIMARY KEY,
  order_id INT,
  amount DECIMAL(10,2),
  payment_date DATE,
  method ENUM('Card','UPI','Bank','COD') NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
CREATE TABLE Shipments (
  shipment_id INT PRIMARY KEY,
  order_id INT,
  shipped_date DATE,
  carrier VARCHAR(50),
  freight DECIMAL(10,2),
  FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
CREATE TABLE Departments (
  dept_id INT PRIMARY KEY,
  dept_name VARCHAR(80)
);
CREATE TABLE Employees (
  emp_id INT PRIMARY KEY,
  emp_name VARCHAR(100),
  manager_id INT NULL,
  dept_id INT,
  city VARCHAR(80),
  salary DECIMAL(10,2),
  FOREIGN KEY (manager_id) REFERENCES Employees(emp_id),
  FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);
INSERT INTO Customers VALUES
(1,'Asha Nair','Consumer','Mumbai','India'),
(2,'Ravi Kumar','Corporate','Bengaluru','India'),
(3,'Priya Shah','Small Business','Ahmedabad','India'),
(4,'John Doe','Consumer','New York','USA');
INSERT INTO Suppliers VALUES
(10,'ZenSupply','Mumbai','India'),
(11,'NorthStar Ltd','Chennai','India'),
(12,'BlueOcean','Dallas','USA');
INSERT INTO Products VALUES
(101,'USB-C Hub','Accessories',2499.00,10),
(102,'Mechanical Keyboard','Peripherals',5999.00,10),
(103,'4K Monitor','Displays',18999.00,12),
(104,'Ergo Chair','Furniture',12999.00,11);
INSERT INTO Orders VALUES
(5001,1,'2025-09-01','Shipped'),
(5002,2,'2025-09-05','Pending'),
(5003,2,'2025-09-07','Shipped'),
(5004,3,'2025-09-10','Cancelled'),
(5005,4,'2025-09-12','Shipped');
INSERT INTO OrderItems VALUES
(90001,5001,101,2,2499.00,0.10),
(90002,5001,102,1,5999.00,0),
(90003,5002,103,1,18999.00,0.05),
(90004,5003,101,3,2399.00,0.15),  -- promo override price
(90005,5003,104,1,12999.00,0.05),
(90006,5004,104,2,12999.00,0),
(90007,5005,103,2,17999.00,0.10);
INSERT INTO Payments VALUES
(70001,5001, 2499*2*(1-0.10)+5999,'2025-09-02','Card'),
(70002,5003, 2399*3*(1-0.15)+12999*(1-0.05),'2025-09-08','UPI'),
(70003,5005, 17999*2*(1-0.10),'2025-09-13','Bank');
INSERT INTO Shipments VALUES
(80001,5001,'2025-09-02','Delhivery',350.00),
(80002,5003,'2025-09-08','Bluedart',500.00),
(80003,5005,'2025-09-13','FedEx',700.00);
INSERT INTO Departments VALUES
(1,'Sales'),(2,'Analytics'),(3,'Ops');
INSERT INTO Employees VALUES
(1010,'Meera Iyer',NULL,1,'Mumbai',180000.00),
(1011,'Kiran Rao',1010,1,'Pune',120000.00),
(1012,'Lakshmi Menon',1010,2,'Mumbai',135000.00),
(1013,'Arun Singh',1012,2,'Delhi',110000.00);


-- Question 1
-- view 1
create view view1 as select o.order_id, i.unit_price, i.discount, i.qty, i.product_id, o.status from orders o inner join orderitems i on o.order_id = i.order_id where o.status = 'Shipped';
-- view 2
create view view2 as select s.supplier_name, p.supplier_id, p.product_id from suppliers s inner join products p on s.supplier_id = p.supplier_id;

select v2.supplier_name, SUM(v1.qty * v1.unit_price * (1 - v1.discount)) as 
total_revenue, count(v1.product_id) as line_count from 
view1 v1 inner join view2 v2 on 
v1.product_id = v2.product_id 
group by(v2.supplier_name);

-- Question 2
-- view 3
create view view3 as select c.customer_id, c.name, o.order_id from customers c inner join orders o on c.customer_id = o.customer_id;
-- view 4
create view view4 as SELECT 
    os.order_id,
    os.gvm,
    sum(p.amount) AS total_payment
FROM order_sum os
left JOIN payments p ON p.order_id = os.order_id
group by os.order_id;
-- order sum view
create view order_sum as SELECT 
        order_id,
        SUM(qty * unit_price * (discount)) AS gvm
    FROM 
        orderitems
    GROUP BY 
        order_id;

SELECT 
    v3.name, 
    COUNT(v3.customer_id) AS order_count, 
    sum(v4.gvm),
    sum(v4.total_payment)
FROM 
    view3 v3 
RIGHT JOIN 
    view4 v4 
ON  
    v3.order_id = v4.order_id 
GROUP BY 
    v3.name;

-- Question 3

-- views
create view 
split_revenue 
as select 
i.order_id, SUM(i.qty * i.unit_price * (1-i.discount)) as 
revenue, p.product_name, i.qty from 
orderitems i inner join products p 
on i.product_id = p.product_id 
group by i.order_id, p.product_id, i.qty; 

create view country_revenue 
as select c.customer_id, o.order_id, c.country from 
customers c inner join orders o 
on c.customer_id = o.customer_id where o.status = 'Shipped';

select sr.product_name, sum(sr.revenue) total_revenue, sum(sr.qty) as shipped_units, cr.country from 
split_revenue sr inner join country_revenue cr 
on sr.order_id = cr.order_id group by cr.country, sr.product_name;

-- Question 4
select o.order_id, c.name, o.order_date from 
customers c inner join orders o on 
c.customer_id = o.customer_id where o.status = 'Pending';  

-- Question 5
-- views 
create view shipped_lines as 
SELECT v2.supplier_name, sum(v1.qty) shipped_lines FROM 
view1 v1 join view2 v2 on 
v1.product_id = v2.product_id group by v2.supplier_name;

create view order_lines as 
SELECT v2.supplier_name, sum(i.qty) as order_lines FROM 
orderitems i join view2 v2 on 
i.product_id = v2.product_id group by v2.supplier_name;

select sl.supplier_name, sl.shipped_lines, ol.order_lines, (shipped_lines/order_lines) as fill_rate from 
shipped_lines sl join order_lines ol on 
sl.supplier_name = ol.supplier_name;

-- Question 6

select * from 
(select sr.product_name, sum(sr.revenue) total_revenue, sum(sr.qty) as shipped_units, cr.country,
ROW_NUMBER() OVER (PARTITION BY cr.country ORDER BY SUM(sr.revenue) DESC) AS rnk
from 
split_revenue sr inner join country_revenue cr 
on sr.order_id = cr.order_id group by cr.country, sr.product_name) ranked
where rnk <= 2 order by total_revenue, country desc; 

-- Question 7
select e1.emp_name, count(e2.manager_id), sum(e2.salary) from 
employees e1 join employees e2 on 
e1.emp_id = e2.manager_id group by e2.manager_id, emp_name; 

-- Question 8












