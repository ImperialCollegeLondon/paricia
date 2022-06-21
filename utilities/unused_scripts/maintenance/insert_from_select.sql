INSERT INTO validacion_var1validado(estacion_id, fecha, valor, usado_para_horario)
SELECT m.estacion_id, m.fecha, m.valor, FALSE FROM medicion_var1medicion m;

INSERT INTO validacion_var10validado(estacion_id, fecha, valor, maximo, minimo, usado_para_horario)
SELECT m.estacion_id, m.fecha, m.valor, m.maximo, m.minimo, FALSE FROM medicion_var10medicion m;

INSERT INTO validacion_var11validado(estacion_id, fecha, valor, maximo, minimo, usado_para_horario)
SELECT m.estacion_id, m.fecha, m.valor, m.maximo, m.minimo, FALSE FROM medicion_var11medicion m;


INSERT INTO validacion_var10validado(estacion_id, fecha, valor, usado_para_horario)
SELECT m.estacion_i*d, m.fecha, m.valor, FALSE FROM medicion_var10medicion m where m.estacion_id = 12 order by m.fecha;