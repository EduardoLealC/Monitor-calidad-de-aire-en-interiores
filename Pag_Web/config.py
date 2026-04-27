# ── Conexión InfluxDB ──────────────────────────────────────────────
INFLUX_URL = ""
TOKEN      = ""
ORG        = ""
BUCKET     = ""
DEVICE     = ""

# ── Campos a consultar ────────────────────────────────────────────
FIELDS = ["temperatura", "humedad", "co2", "co", "pm25", "pm10", "luz"]

# ── Umbrales y metadata por parámetro ────────────────────────────
PARAMS = {
    "temperatura": {
        "label": "Temperatura",
        "unit": "°C",
        "ok_range": (18, 26),          # verde si está dentro
        "alert_low": 18,
        "alert_high": 26,
        "oms": "18–24 °C (confort)",
        "epa": "—",
        "description": (
            "La temperatura afecta directamente el confort térmico y la "
            "productividad. Fuera del rango de confort puede generar fatiga, "
            "dificultad de concentración y estrés térmico."
        ),
        "tips": [
            "Realiza la ventilación preferentemente cuando no haya personas en la sala.",
            "Durante la ventilación, abre completamente puertas o ventanas para permitir "
            "una renovación rápida del aire.",
            "Evita ventilaciones parciales prolongadas, ya que pueden generar lecturas ambiguas "
            "en el sistema.",
            "Considera que descensos bruscos de temperatura pueden deberse a ventilación y no "
            "necesariamente a condiciones de confort inadecuadas.",
            "La temperatura tenderá a volver al rango de confort una vez finalizada la ventilación; "
            "sin embargo, asegúrate de que los niveles de CO₂ sean adecuados antes de cerrar ventanas "
            "o puertas."
        ],
    },
    "humedad": {
        "label": "Humedad Relativa",
        "unit": "%",
        "ok_range": (30, 60),
        "alert_low": 30,
        "alert_high": 60,
        "oms": "30–60%",
        "epa": "—",
        "description": (
            "La humedad relativa influye en la calidad del aire y la salud respiratoria. "
            "Niveles muy bajos resecan las mucosas, mientras que niveles altos favorecen "
            "la aparición de hongos, ácaros y condensación. Cambios durante la ventilación "
            "pueden afectar temporalmente las mediciones del sistema."
        ),
        "tips": [
            "Mantén la humedad idealmente entre 40% y 60%.",
            "Ventila de forma breve e intensiva para reducir humedad acumulada, especialmente en invierno.",
            "Evita ventilaciones parciales prolongadas, ya que pueden generar lecturas "
            "inestables en el sistema.",
            "Considera que aumentos o descensos bruscos pueden estar asociados a ventilación.",
            "Si la humedad se mantiene alta de forma constante, considerar el uso de un deshumidificador.",
            "El efecto de la ventilación sobre la humedad depende de la condición del aire exterior"
        ],
    },
    "co2": {
        "label": "CO₂",
        "unit": "ppm",
        "ok_range": (0, 1000),
        "alert_low": None,
        "alert_high": 1000,
        "oms": "< 1.000 ppm",
        "epa": "< 1.000 ppm",
        "description": (
            "El CO₂ es el principal indicador de ventilación en espacios interiores. Niveles elevados "
            "reducen la concentración, causan somnolencia y pueden generar dolores de cabeza. Es una "
            "variable clave para activar o finalizar procesos de ventilación en el sistema."
        ),
        "tips": [
            "Inicia ventilación cuando el CO₂ supere los 1000 ppm.",
            "Durante la ventilación, abre completamente ventanas o puertas para favorecer una "
            "rápida renovación del aire.",
            "Finaliza la ventilación una vez que el CO₂ vuelva a niveles adecuados "
            "(por ejemplo, bajo 800 ppm).",
            "Considera que descensos rápidos de CO₂ suelen estar asociados a ventilación efectiva"
        ],
    },
    "co": {
        "label": "CO",
        "unit": "ppm",
        "ok_range": (0, 9),
        "alert_low": None,
        "alert_high": 9,
        "oms": "4 mg/m³ (24h)",
        "epa": "< 9 ppm",
        "description": (
            "El monóxido de carbono (CO) es un gas inodoro y altamente tóxico, generado por "
            "combustiones incompletas, no forma parte de la lógica de confort ambiental, sino de "
            "seguridad crítica. Su presencia en interiores representa un riesgo grave para la salud, "
            "por lo que debe tratarse como una condición de alerta crítica dentro del sistema."
        ),
        "tips": [
            "Activa ventilación inmediata si se detecta cualquier nivel anormal de CO.",
            "Desaloja el espacio ante niveles elevados y evita la exposición prolongada.",
            "Identifica y detiene posibles fuentes de combustión (calefactores, estufas, cocinas).",
            "Considera que cualquier lectura de CO no es normal en ambientes interiores y "
            "requiere atención inmediata.",
            "Prioriza la seguridad por sobre cualquier otra variable (temperatura, humedad o CO₂)."

        ],
    },
    "pm25": {
        "label": "PM2.5",
        "unit": "µg/m³",
        "ok_range": (0, 35),
        "alert_low": None,
        "alert_high": 35,
        "oms": "15 µg/m³ (24h)",
        "epa": "35 µg/m³ (24h)",
        "description": (
            "Las partículas finas PM2.5 penetran profundamente en los pulmones y el torrente "
            "sanguíneo. Son uno de los contaminantes más dañinos para la salud respiratoria y "
            "cardiovascular. Su concentración puede depender tanto de fuentes internas como de la "
            "calidad del aire exterior, lo que debe considerarse en la gestión del sistema."
        ),
        "tips": [
            "Evita generar fuentes internas de partículas (velas, incienso, cocción sin ventilación)",
            "Antes de ventilar, considera la calidad del aire exterior; ventilar con alta "
            "contaminación puede empeorar la situación.",
            "Prioriza ventilación solo cuando el aire exterior sea más limpio que el interior.",
            "Considera que aumentos bruscos pueden deberse a fuentes internas o ingreso "
            "de aire contaminado."
        ],
    },
    "pm10": {
        "label": "PM10",
        "unit": "µg/m³",
        "ok_range": (0, 45),
        "alert_low": None,
        "alert_high": 45,
        "oms": "45 µg/m³ (24h)",
        "epa": "150 µg/m³ (24h)",
        "description": (
            "Las partículas PM10 afectan principalmente las vías respiratorias superiores. "
            "Suelen provenir de polvo, polen, moho o material en suspensión, y pueden aumentar "
            "por actividades dentro del espacio o por el ingreso de aire exterior. Sus niveles "
            "pueden variar rápidamente, lo que debe considerarse en la interpretación del sistema."
        ),
        "tips": [
            "Identifica aumentos bruscos como posibles eventos puntuales "
            "(limpieza, movimiento de personas, ingreso de polvo).",
            "Durante estos eventos, prioriza ventilación breve e intensiva si el aire exterior"
            " es más limpio.",
            "Evita ventilación si el exterior presenta alta carga de polvo",
            "Considera que el polvo puede permanecer en suspensión tras actividades, "
            "afectando temporalmente las mediciones.",
            "Mantener rutinas de limpieza puede reducir fuentes persistentes de PM10."
        ],
    },
    "luz": {
        "label": "Luz",
        "unit": "lux",

        "ok_range": (300, 500),        # rango típico de confort visual en aulas
        "alert_low": 300,
        "alert_high": None,
        "oms": "—",
        "epa": "—",
        "description": (
            "La iluminación influye directamente en la fatiga visual, el confort y la concentración."
            " Niveles inadecuados pueden dificultar tareas visuales, mientras que una iluminación "
            "bien gestionada mejora el desempeño en actividades como lectura y escritura. "
            "En aulas y oficinas se recomiendan entre 300–500 lux."
        ),
        "tips": [
            "Ajusta la iluminación artificial para mantener niveles entre 300–500 lux según la actividad.",
            "Prioriza el uso de luz natural cuando esté disponible, evitando deslumbramientos.",
            "Revisa si las luminarias están en buen estado.",
        ],
    },
}