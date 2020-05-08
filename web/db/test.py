from mysqlpool import Mysql

mysql = Mysql()


insert = "insert into test (id, name) values (%s, %s)"
result = mysql.insertOne(insert, (9, 3L))
print(result)
mysql.end()
sqlAll = "select * from test"
result = mysql.getAll(sqlAll)
if result :
    print "get all"
    for row in result :
        print row