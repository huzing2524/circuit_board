create table circuit_board (
  uuid varchar(36) primary key default uuid_generate_v4(),
  shape varchar(10),
  x_location varchar(30),
  y_location varchar(30)
);
