drop table if exists posts;
create table posts (
	id integer primary key autoincrement,
	title text not null,
	datePublished DateTime not null,
	text text not null,
);