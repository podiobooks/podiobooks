#!/bin/sh

# base command to pull from MySQL
dump_base="mysqldump -u root -p"

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
$dump_base --no-create-info podiobooks $tables > pb_data.sql
