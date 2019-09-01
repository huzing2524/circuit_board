create table circuit_board (
  id serial primary key,
  shape varchar(10),
  x_location float,
  y_location float,
  direction varchar(1) -- 0: 竖直, 1: 水平
);
