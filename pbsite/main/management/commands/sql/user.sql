alter table auth_user rename column handle to username;
alter table auth_user alter column username type varchar(30) using trim(both ' ' from username);
alter table auth_user alter column username drop default;

alter table auth_user rename column firstname to first_name;
alter table auth_user alter column first_name type varchar(30) using substr(trim(both ' ' from first_name), 0, 30);
alter table auth_user alter column first_name drop default;

alter table auth_user rename column lastname to last_name;
alter table auth_user alter column last_name type varchar(30) using substr(trim(both ' ' from last_name), 0, 30);
alter table auth_user alter column last_name drop default;

alter table auth_user alter column email type varchar(75);
alter table auth_user alter column email drop default;

alter table auth_user alter column password type varchar(128);
alter table auth_user alter column password drop default;

alter table auth_user drop constraint user_enabled_check;
alter table auth_user alter column enabled drop default;
alter table auth_user rename column enabled to is_active;
alter table auth_user alter column is_active type boolean using is_active = 1;

alter table auth_user rename column datecreated to date_joined;
alter table auth_user alter column date_joined type timestamp with time zone;
alter table auth_user alter column date_joined drop default;