# esql5
elsh is an interactive esql5 command line interface (CLI) SQL shell with autocompletion. support elasticserch5.x,2.x,1.x
![](https://github.com/unimassystem/esql5/blob/master/elsh.png)


特性介绍
----------------
#接近标准SQL语法

    create table my_index.my_table (
         id keyword,
         name text,
         age long,
         birthday date
    );
    
    select * from my_index.my_type;
    
    select count(*) from my_index.my_table group by age;
    

#Create table

	字段参数,ES中分词规则、索引类型、字段格式等高级参数的支持
	
	create table my_table (
		name text (analyzer = ik_max_word),
		dd text (index=no),
		age long (include_in_all=false)
	);
	
	
	对象、嵌套字段支持 as
	
	create table my_index (
		id long,
		name text,
         obj object as (
             first_name text,
             second_name text (analyzer=pinyin)
         )
    );
	
	
	create table my_index (
		id long,
		name text,
       obj nested as (
             first_name text,
             second_name text (analyzer=pinyin)
       )
    );


	ES索引高级参数支持 with option
	
	create table my_index (
		id long,
		name text
    ) with option (
    	index.number_of_shards=10,
       index.number_of_replicas = 1
    );
	

#Insert/Bulk

	单条数据插入
	insert into my_index.index (name,age) values ('zhangsan',24);
	
	多条插入
	bulk into my_index.index (name,age) values ('zhangsan',24),('lisi',24);

	
	对象数据插入,[]list,{}Map
	
	insert into my_index.index (ds) values (['zhejiang','hangzhou']);
			
	insert into my_index.index (dd) values ({address='zhejiang',postCode='330010'});
	
	
#select/Aggregations

	select * from my_table.my_index where name like 'john *' and age between 20 and 30 and (hotel = 'hanting' or flight = 'MH4510');
	
	地理位置中心点查询
	select * from hz_point where geo_distance({distance='1km',location='30.306378,120.247427'});
	
	地理坐标区域查询
	select * from hz_point where geo_bounding_box({location={top_left='31.306378,119.247427',bottom_right='29.285797,122.172329'}});
	
	pipeline统计 move_avg
	select count(*) as total, moving_avg({buckets_path=total}) from my_index group by date_histogram({field=timestamp,interval='1h'});
	
	
Getting Started
----------------
	环境要求python >= 2.7

	export PYTHONHOME=(%python_path)
	export PATH=$PYTHONHOME/bin:$PATH
	
	
	安装第三方依赖包
	pip install -r esql5.egg-info/requires.txt (或pip3 install -r esql5.egg-info/requires.txt)
	或python setup.py install (或python3 setup.py install)
	
	运行esql5服务:
	cd esql5
	python -m App.app (或python3 -m App.app)
	
	shell终端:
	python -m elsh.Command (或python3 -m elsh.Command )




