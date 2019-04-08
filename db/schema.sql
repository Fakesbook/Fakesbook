CREATE TABLE IF NOT EXISTS User (
    id integer primary key autoincrement,
    username text unique,
    password text,
    gender text default null,
    image text default "none",
    age integer default null,
    phone text default null,
    fav_color text default null,
    interests text default null,
    hometown text default null,
    permissions integer default 222222,
    requests text default "[]"
);

CREATE TABLE IF NOT EXISTS Friend (
    id integer primary key autoincrement,
    f1 integer not null,
    f2 integer not null,
    foreign key (f1) references User(id),
    foreign key (f2) references User(id),
    constraint friendship unique (f1, f2)
);
