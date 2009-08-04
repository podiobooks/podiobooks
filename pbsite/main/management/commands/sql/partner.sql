alter table main_partner alter column name drop default;

alter table main_partner alter column url drop default;
alter table main_partner alter column url type varchar(200) using substr(trim(both ' ' from url), 0, 200);

alter table main_partner alter column logo drop default;
alter table main_partner alter column logo type varchar(100) using substr(trim(both ' ' from url), 0, 200);

alter table main_partner rename column datecreated to date_created;
alter table main_partner alter column date_created drop default;
alter table main_partner alter column date_created type timestamp with time zone;