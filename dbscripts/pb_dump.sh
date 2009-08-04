#!/bin/sh

echo -n "Enter MySQL password for root: "
read pwd

# base command to pull from MySQL
dump_base="mysqldump -u $1 -p$pwd"

# these are in dependency order
tables="bookcategory \
userstatus \
role \
partner \
user \
book \
bookrating \
chapter \
downloads \
subscription"

$dump_base --no-create-db --no-data podiobooks $tables > pb_schema.sql
perl mysql2pgsql.perl --char2varchar pb_schema.sql pb_schema_pg.sql

for table in $tables
do
    echo "Dumping $table."
    $dump_base --no-create-info podiobooks $table > pb_data_$table.sql
	perl mysql2pgsql.perl --char2varchar pb_data_$table.sql pb_data_${table}_pg.sql
done


