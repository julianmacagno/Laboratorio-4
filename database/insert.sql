insert into role values
  (0, 'owner'), (1, 'guest');
  
insert into location_type values
  (0, 'Resto'), (1, 'Disco');

insert into user values
  (0, 'admin', 'admin@admin.com', 'admin'),
  (1, 'julian', 'julian@julian.com', 'julian'),
  (2, 'javi', 'javi@javi.com', 'javi');

insert into location values
  (0,'Depto Julian','-31.1542, -64.2325',1,1),
  (1,'Le Parc','-31.4242,-64.1925',1,0),
  (2,'Le Pont','-31.4242, -64.1925',1,1),
  (3,'La Casona','-31.4242, -64.1925',1,1),
  (4,'Tu Casa','-31.4242, -64.1925',1,1);
  
insert into event values
  (0, 'Noche Halloween', '2018-10-31', 1),
  (1, 'Cumple 15', '2018-11-3', 2),
  (2, 'Fiesta sexo salvaje', '2018-11-5', 0);

insert into guest_list values
  (0, 'lista1', 0), (1, 'lista2', 0),
  (2, 'lista3', 1), (3, 'lista4', 1);

insert into user_list values
  (0, 0, 1), (0, 1, 0), (0, 2, 1), (1, 0, 1),
  (1, 1, 0), (1, 2, 1), (2, 0, 1), (2, 1, 0);
