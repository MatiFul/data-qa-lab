COMMENT ON TABLE raw.transacciones_raw IS
'Tabla RAW con transacciones cargadas desde CSV sin reglas fuertes de limpieza.';

COMMENT ON TABLE curado.transacciones_curado IS
'Tabla curada de transacciones válidas luego de filtros básicos y joins contra catálogos.';

COMMENT ON TABLE refinado.transacciones_refinado IS
'Tabla refinada con cálculos de control entre monto informado y monto calculado por items.';

COMMENT ON TABLE consumo.transacciones_consumo IS
'Capa de consumo preparada para análisis y visualización en Power BI.';


COMMENT ON COLUMN refinado.transacciones_refinado.monto_transaccion IS
'Monto informado en la transacción original. Fuente: curado.transacciones_curado.monto.';

COMMENT ON COLUMN refinado.transacciones_refinado.monto_calculado_items IS
'Monto total calculado desde los items asociados a la transacción. Fórmula: SUM(cantidad * precio_unitario).';

COMMENT ON COLUMN refinado.transacciones_refinado.diferencia_monto IS
'Diferencia entre el monto informado y el monto calculado desde items. Fórmula: monto_transaccion - monto_calculado_items.';

COMMENT ON COLUMN refinado.transacciones_refinado.cantidad_items IS
'Cantidad de items asociados a la transacción. Fórmula: COUNT(id_item).';

COMMENT ON COLUMN refinado.transacciones_refinado.flag_sin_items IS
'Flag que indica si una transacción no tiene items asociados. 1 = sin items, 0 = con items.';

COMMENT ON COLUMN refinado.transacciones_refinado.flag_inconsistencia_monto IS
'Flag que indica diferencia significativa entre monto informado y monto calculado. 1 = inconsistente, 0 = consistente.';


COMMENT ON COLUMN consumo.transacciones_consumo.monto_transaccion IS
'Monto informado de la transacción, proveniente de refinado.transacciones_refinado.monto_transaccion.';

COMMENT ON COLUMN consumo.transacciones_consumo.monto_calculado_items IS
'Monto calculado desde items, proveniente de refinado.transacciones_refinado.monto_calculado_items.';

COMMENT ON COLUMN consumo.transacciones_consumo.diferencia_monto IS
'Diferencia entre monto informado y monto calculado desde items. Campo usado para análisis de inconsistencias.';

COMMENT ON COLUMN consumo.transacciones_consumo.anio_transaccion IS
'Año extraído desde fecha_transaccion para análisis temporal. Fórmula: EXTRACT(YEAR FROM fecha_transaccion).';

COMMENT ON COLUMN consumo.transacciones_consumo.mes_transaccion IS
'Mes extraído desde fecha_transaccion para análisis temporal. Fórmula: EXTRACT(MONTH FROM fecha_transaccion).';

COMMENT ON COLUMN consumo.transacciones_consumo.dia_transaccion IS
'Día extraído desde fecha_transaccion para análisis temporal. Fórmula: EXTRACT(DAY FROM fecha_transaccion).';