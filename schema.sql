create table maps (
  id integer primary key not null,
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp,
  width int not null,
  height int not null,
  tiles text
);

create trigger update_maps_timestamp
after update on maps
begin
  update maps set updated_at = current_timestamp
  where id = new.id;
end;

create table tiles (
  id integer primary key not null,
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp,
  name text not null,
  texture text not null
);

create trigger update_tiles_timestamp
after update on tiles
begin
  update tiles set updated_at = current_timestamp
  where id = new.id;
end;
