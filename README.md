# Plataforma Distribuida de Análisis Geoespacial con Caché 



Esta plataforma implementa una arquitectura de microservicios basada en contenedores para procesar consultas geoespaciales sobre el dataset *Google Open Buildings* en la Región Metropolitana de Santiago.El sistema utiliza un patrón de caché *look-aside* para mitigar la carga computacional generada por consultas repetitivas.

Además de su función operativa, el sistema actúa como un banco de pruebas experimental para medir el impacto de distintas configuraciones de memoria, políticas de evicción (LRU, LFU, Random) y Tiempos de Vida (TTL) bajo distribuciones de tráfico Uniforme y de Zipf.

## 🏗️ Arquitectura y Componentes

]El ecosistema está compuesto por tres contenedores orquestados a través de Docker Compose:

1. **`response-gen` (Backend Analítico):** Servicio HTTP *stateless* construido con Flask y NumPy. ]Carga el dataset en memoria al iniciar y expone una API REST para procesar 5 tipos de consultas geoespaciales (conteo, densidad, área, etc.) sobre zonas predefinidas (ej. Providencia, Maipú).
2. **`cache-redis` (Caché en Memoria):** Instancia de Redis que almacena las respuestas serializadas en JSON. Absorbe la carga de las llaves más "calientes" para reducir la latencia general del sistema.
3. **`traffic-gen` (Generador y Cliente):** Script en Python que simula múltiples clientes inyectando tráfico.Decide probabilísticamente qué zona consultar (Uniforme o Zipf), consulta a Redis o al backend, y registra la telemetría (HIT/MISS, latencia p50/p95, throughput) en un archivo `metricas_experimento.csv`

## 🚀 Requisitos Previos

- Docker y Docker Compose instalados.
- Puerto `5000` (Flask) y `6379` (Redis) disponibles en la máquina host.

## 🛠️ Instrucciones de Ejecución

1. Clonar el repositorio y posicionarse en la carpeta raíz.
2. Construir y levantar los contenedores en segundo plano:
   ```bash
   docker-compose up --build
