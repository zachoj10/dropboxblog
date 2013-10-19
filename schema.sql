drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text null,
  url text not null
);