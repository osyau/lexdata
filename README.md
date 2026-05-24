# LexData 🔍 | Auditoría Inteligente de Datos Empresariales
LexData es una plataforma de software desarrollada en Python diseñada para la auditoría inteligente, análisis y detección de anomalías en grandes volúmenes de datos empresariales. El sistema integra principios de Ciencia de Datos, Estadística Aplicada y Motores de Reglas para identificar patrones irregulares, automatizar el control de calidad de la información y generar reportes analíticos de alto impacto.

El proyecto está construido bajo una arquitectura modular por capas, priorizando el aislamiento de dependencias mediante entornos virtuales (`venv`) y un control de versiones estricto.

---

## 🏗️ Arquitectura del Sistema (Capas)
Para garantizar la escalabilidad y el mantenimiento limpio del código, **LexData** se estructura en las siguientes capas de software:

*   **A. Capa de Base de Datos (DATABASE):** Persistencia y gestión estructurada de datos relacionales, utilizando operaciones SQL optimizadas (DDL, DML, TCL) para asegurar la integridad transaccional.
*   **B. Motor de Reglas:** Lógica de negocio centralizada en Python que evalúa las condiciones, restricciones y políticas empresariales predefinidas sobre los conjuntos de datos.
*   **C. Detección de Anomalías:** Componente enfocado en aplicar modelos estadísticos y algoritmos analíticos para descubrir desviaciones, posibles fraudes o registros corruptos en el sistema.
*   **D. Dashboard & Reportes:** Módulo de visualización encargado de transformar los datos auditados en paneles interactivos y métricas clave para la toma de decisiones.
  
	[ Capa D: Dashboard / UI ]
				│
				▼
	[ Capa B: Motor de Reglas ] ◄───(Usa los modelos de)───► [ Capa C: Detección Estadistica ]
				│
				▼
	[ Capa A: Acceso a Datos / SQL ]

---

## 🛠️ Stack Tecnológico
*   **Lenguaje Base:** Python 3.x
*   **Gestión de Datos:** SQL Transaccional (PostgreSQL / MySQL / SQLite)
*   **Core Científico:** Ciencia de Datos, Estadística Aplicada y Algoritmos de Detección
*   **Visualización:** Dashboards y Reportes Analíticos
*   **Control de Versiones:** Git & GitHub

---

## 📂 Estructura del Proyecto
```text
	LEXDATA/
		│
		├── src/                    # código fuente de la app
		│   ├── __init__.py
		│   ├── database.py         # archivo databse
		│   ├── parser.py           # archivo de procesamiento
		│   │
		│   ├── config/             # CARPETA Para conexiones y variables
		│   │   └── __init__.py
		│   │
		│   └── core/               # CARPETA Para motor de reglas y anomalías
		│       ├── __init__.py
		│       ├── rules_engine.py
		│       └── anomaly_detect.py
		│
		├── venv/                   # entorno virtual 
		├── .gitignore              # Configuración de Git
		├── main.py                 # archivo principal 
		├── README.md               # documentación
		└── requirements.txt        # dependencias 
```
---
## 🚀 Instalación y Uso

### Prerrequisitos
* Python 3.10 o superior
* Git

### Clonar e Instalar
1. Clona el repositorio:
   
```bash
   git clone [https://github.com/osyau/lexdata.git](https://github.com/osyau/lexdata.git)
   cd lexdata
```
2. Crea y activa el entorno virtual:
   python -m venv venv
   # En Windows (Git Bash, CMD o PowerShell):
   .\venv\Scripts\activate
   # En Linux / macOS:
   source venv/Scripts/activate

3. Instala las dependencias (próximamente):
   pip install -r requirements.txt

---

## 📈 Estado del Proyecto & Roadmap

Actualmente, **LexData** se encuentra en su fase inicial de desarrollo. El avance del proyecto se gestiona mediante sprints semanales para asegurar un crecimiento modular y controlado.

### 🗓️ Semana 1: Arquitectura y Configuración Base (Actual)
- [x] Inicialización del repositorio Git y estructuración del portafolio.
- [x] Configuración del entorno virtual (`venv`) y definición de dependencias base.
- [x] Diseño de la arquitectura de software por capas y árbol de directorios.
- [x] archivo Parseador definido.
- [ ] Creación de scripts SQL iniciales (Modelado DDL para persistencia de datos).
- [ ] Configuración del punto de entrada de la aplicación (`main.py`) y testing de conexión.

### 🗓️ Semana 2: Core del Sistema (Por Definir)
*Las tareas específicas de esta fase se terminarán de detallar una vez completados los objetivos de la Semana 1, priorizando:*
- [ ] Desarrollo y testing del Motor de Reglas en Python (Lógica de negocio).
- [ ] Estructuración de los primeros módulos de la capa de Detección de Anomalías.