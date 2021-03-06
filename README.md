# circuit-board
电路板铜线尺寸测量，效果在文件中有演示 [固定位置自动测量效果说明.pdf](https://github.com/huzing2524/circuit_board/blob/master/%E5%9B%BA%E5%AE%9A%E4%BD%8D%E7%BD%AE%E8%87%AA%E5%8A%A8%E6%B5%8B%E9%87%8F%E6%95%88%E6%9E%9C%E8%AF%B4%E6%98%8E.pdf)。

* Install the libraries in the file `requirements.txt` with the script below:  
`pip3 install -r requirements.txt`

* Run the HTTP server with the script like this below:   
`python3 manage.py runserver 127.0.0.1:8000`

* Create a HTTP API request to get the response, ues POST request method, the image should be encoded by base64, 
that means it's a string format. Another parameter is shape in URL query parameters, it means one particular shape:    
`127.0.0.1:8000/measurement?shape=1`

# Prepare model


```
python manage.py makemigrations measurement
python manage.py migrate
```

# Run data within Docker

On Ryzen 5 CPU the pre-create check fails, even though SVM is enabled
in the BIOS, this can be solved with skipping that check via

```
set VIRTUALBOX_NO_VTX_CHECK=true
docker-machine create -d virtualbox default
```

Then the postgres image can be pulled and started with following
commands:

```
docker run --name aoi-db -p 5432:5432 -e POSTGRES_PASSWORD=aoi2019 -d postgres
docker exec -it aoi-db psql -U postgres
```

And then within the psql command line

```
create database circuit_board;
\w circuit_board
create table templates
(
  id           serial primary key,
  shape        varchar(10),
  name         varchar(30),
  top_left     float[],   -- 左上
  bottom_right float[],   -- 右下
  direction    varchar(1) -- 水平: 0, 垂直: 1
);
\q
```

Start the AOI program with

```
set PG_HOST=127.0.0.1
set PG_PASSWORD=123456
python manage.py runserver 127.0.0.1:8000
```

