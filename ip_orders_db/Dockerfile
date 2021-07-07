FROM mysql

ENV MYSQL_DATABASE=ip_orders_db \
    MYSQL_ROOT_PASSWORD=zmp24DSSQL

ADD dump.sql /docker-entrypoint-initdb.d

EXPOSE 3306



