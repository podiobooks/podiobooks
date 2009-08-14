insert into main_contributor
(user_id, firstname, lastname, displayname, slug, deleted, date_created, date_updated)
select distinct t.userid,
	u.first_name,
	u.last_name,
	u.first_name || ' ' || u.last_name,
	lower(regexp_replace(substr(u.first_name || ' ' || u.last_name, 0, 50), ' ', '-')),
	u.is_active = false,
	u.date_joined,
	now()
from auth_user u
join main_title t on t.userid = u.id;

insert into main_titlecontributors
(title_id, contributor_id, contributor_type_id, date_created)
select t.id,
    c.id,
    (select id from main_contributortype where slug = 'maintainer'),
    t.date_created
from auth_user u
join main_title t on t.userid = u.id
join main_contributor c on t.userid = c.user_id;

insert into main_titlecontributors
(title_id, contributor_id, contributor_type_id, date_created)
select t.id,
	c.id,
    (select id from main_contributortype where slug = 'author'),
    t.date_created
from main_title t
join main_contributor c on c.displayname = t.authors;

create table main_invalidtitle as
select t.id, t.userid, t.authors, t.date_created
from main_title t
where t.id not in (
        select title_id
        from main_titlecontributors
        where contributor_type_id = (select id from main_contributortype where slug = 'author')
);

insert into main_titlecontributors
(title_id, contributor_id, contributor_type_id, date_created)
select i.id,
    c.id,
    (select id from main_contributortype where slug = 'author'),
    i.date_created
from main_contributor c,
main_invalidtitle i
where strpos(lower(i.authors), lower(c.firstname)) > 0
and strpos(lower(i.authors), lower(c.lastname)) > 0
and nullif(c.firstname, '') is not null
and nullif(c.lastname, '') is not null
and lower(i.authors) not like ('%%and %%')
and lower(i.authors) not like ('%%narrated %%')
and lower(i.authors) not like ('%%interpreted %%')
and lower(i.authors) not like ('%%read %%')
and lower(i.authors) not like ('%%with %%')
and lower(i.authors) not like ('%%as %%')
and lower(i.authors) not like ('%%compiled %%')
and lower(i.authors) not like ('%%edit%%');

create table main_contributornames as
select distinct c.id,
	trim(both ' ' from i.authors) as displayname
from main_contributor c,
main_invalidtitle i
where strpos(lower(i.authors), lower(c.firstname)) > 0
and strpos(lower(i.authors), lower(c.lastname)) > 0
and nullif(c.firstname, '') is not null
and nullif(c.lastname, '') is not null
and lower(i.authors) not like ('%%and %%')
and lower(i.authors) not like ('%%narrated %%')
and lower(i.authors) not like ('%%interpreted %%')
and lower(i.authors) not like ('%%read %%')
and lower(i.authors) not like ('%%with %%')
and lower(i.authors) not like ('%%as %%')
and lower(i.authors) not like ('%%compiled %%')
and lower(i.authors) not like ('%%edit%%');

delete from main_invalidtitle where id in (
select i.id
from main_contributor c,
main_invalidtitle i
where strpos(lower(i.authors), lower(c.firstname)) > 0
and strpos(lower(i.authors), lower(c.lastname)) > 0
and nullif(c.firstname, '') is not null
and nullif(c.lastname, '') is not null
and lower(i.authors) not like ('%%and %%')
and lower(i.authors) not like ('%%narrated %%')
and lower(i.authors) not like ('%%interpreted %%')
and lower(i.authors) not like ('%%read %%')
and lower(i.authors) not like ('%%with %%')
and lower(i.authors) not like ('%%as %%')
and lower(i.authors) not like ('%%compiled %%')
and lower(i.authors) not like ('%%edit%%');

update main_contributor
set displayname = n.display_name
from main_contributornames n
where main_contributor.id = n.id;

drop table main_contributornames;
