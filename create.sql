create table templates
(
  id           serial primary key,
  shape        varchar(10),
  top_left     float[], -- 左上
  bottom_right float[]  -- 右下
);
