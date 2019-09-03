create table templates
(
  id           serial primary key,
  shape        varchar(10),
  top_left     float[],   -- 左上
  bottom_right float[],   -- 右下
  direction    varchar(1) -- 水平: 0, 垂直: 1
);
