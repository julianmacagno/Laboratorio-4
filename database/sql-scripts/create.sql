create table user (
	id integer not null primary key auto_increment,
	name varchar(30) not null unique,
	email varchar(60) not null unique,
	pass varchar(60) not null
);

create table location_type (
	id integer not null primary key auto_increment,
	name varchar(30) not null
);

create table location (
	id integer not null primary key auto_increment,
	name varchar(60) not null,
	coord varchar(30),
	id_loc_type integer not null references location_type(id),
	id_owner integer not null references user(id)
);

create table role (
	id integer not null primary key auto_increment,
	name varchar(30) not null
);

create table guest_list (
	id integer not null primary key auto_increment,
	name varchar(60) not null,
	id_owner integer not null references user(id)
);

create table user_list (
	id_guest_list integer not null references guest_list(id),
	id_user integer not null references user(id),
	id_role integer not null references role(id),
	primary key(id_guest_list, id_user, id_role)
);

create table event (
	id integer not null primary key auto_increment,
	name varchar(60) not null,
	date timestamp not null,
	id_guest_list integer not null references guest_list(id)
);