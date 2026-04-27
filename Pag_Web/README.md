# Monitor de Calidad de Aire En Interiores

Aplicación web desarrollada con **Streamlit** para visualizar en tiempo real los datos de calidad de aire interior del Laboratorio Mancera. Se conecta a una base de datos **InfluxDB** y muestra un dashboard embebido de **Grafana**.

---

## Parámetros monitoreados

| Parámetro | Unidad | Umbral OMS |
|-----------|--------|------------|
| Temperatura | °C | 18–24 °C |
| Humedad Relativa | % | 30–60% |
| CO₂ | ppm | < 1.000 ppm |
| CO | ppm | < 9 ppm |
| PM2.5 | µg/m³ | 15 µg/m³ (24h) |
| PM10 | µg/m³ | 45 µg/m³ (24h) |
| Luz | lux | 300–500 lux |

---

## Estructura del proyecto

```
pag_web_MCAEI/
├── app.py                  # Punto de entrada principal
├── config.py               # Configuración de conexión y parámetros
├── requirements.txt        # Dependencias Python
├── Dockerfile              # Imagen Docker de la app
├── component/
│   ├── kpi_card.py         # Tarjetas de indicadores
│   └── kpi_detail.py       # Vista de detalle por parámetro
├── data/
│   └── influx.py           # Consultas a InfluxDB
└── pages/
    └── dashboard.py        # Página principal del dashboard
```

---

## Variables de entorno

La aplicación requiere las siguientes variables de entorno. Es necesario crea un archivo `.env` en la raíz del proyecto:

```env
INFLUX_URL=http://influxdb:8086
INFLUX_TOKEN=tu_token_aqui
INFLUX_ORG=tu_org_id
INFLUX_BUCKET=Tu_Bucket
```

---

## Instalación y ejecución

### Con Docker 

Con Docker Desktop instalado y el archivo `.env` creado, ejecuta desde la raíz del proyecto (donde está el `docker-compose.yml`):

```bash
docker-compose up --build -d
```

### Sin Docker (desarrollo local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Detener los servicios

```bash
docker-compose down
```

---

## Dependencias principales

- [Streamlit](https://streamlit.io/)
- [influxdb-client](https://github.com/influxdata/influxdb-client-python)
- [streamlit-autorefresh](https://github.com/kmcgrady/streamlit-autorefresh)
