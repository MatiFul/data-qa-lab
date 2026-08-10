# SQL legado

Estos archivos conservan la primera implementación pedagógica:

```text
raw → curado → refinado → consumo
```

Ya no forman parte del pipeline activo ni son ejecutados por el bootstrap o por
Airflow. Se mantienen únicamente como referencia histórica para comparar SQL
suelto con el proyecto dbt actual:

```text
raw → dbt_staging → dbt_intermediate → dbt_marts
```
