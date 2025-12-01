create  database production;
use bike_database;
use production;
create table customers(customer_id integer primary key, first_name varchar(100), last_name varchar(50), phone varchar(20), email varchar(50), street varchar(100), city varchar(50), state varchar(50), zip_code varchar(10));
create table categories(category_id integer primary key, category_name varchar(100));
create table brands(brand_id integer primary key, brand_name varchar(50));
create table products(product_id integer primary key, product_name varchar(50),brand_id integer not null, category_id integer not null, model_year year, list_price float, foreign key(brand_id) references production.brands(brand_id), foreign key(category_id) references production.categories(category_id)); 
create table stores (store_id integer primary key, store_name varchar(50), phone varchar(20), email varchar(50), street varchar(100), city varchar(50), state varchar(50), zip_code varchar(50)); 
create table stocks(store_id integer not null, product_id integer not null, quantity integer, primary key(store_id, product_id), foreign key(store_id) references bike_database.stores(store_id), foreign key(product_id) references production.products(product_id));
create table staffs(staff_id integer primary key, first_name varchar(50), last_name varchar(50), phone varchar(20), email varchar(50), active varchar(20), store_id integer not null, manager_id integer, foreign key(store_id) references bike_database.stores(store_id), foreign key(manager_id) references bike_database.staffs(staff_id));
create table orders(order_id varchar(10) primary key, customer_id integer, order_status varchar(20), order_date datetime, required_date date, shipped_date datetime, store_id integer, staff_id integer, foreign key(customer_id) references bike_database.customers(customer_id), foreign key(store_id) references bike_database.stores(store_id), foreign key(staff_id) references bike_database.staffs(staff_id));
create table order_items(order_id varchar(10), item_id varchar(10), product_id integer, quantity varchar(20), list_price float, discount float, primary key(order_id, item_id), foreign key(order_id) references bike_database.orders(order_id), foreign key(product_id) references production.products(product_id));

insert into orders values('ord1', 1, 'booked', '2025-09-23', '2025-10-01', '2025-09-03', 1,3);
drop table customers;
delete from orders where order_id = 'ord1'; 
desc orders;


