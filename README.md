# [cite_start]Plataforma Distribuida de Análisis Geoespacial con Caché 

[cite_start]Proyecto desarrollado para el curso **Sistemas Distribuidos (2026-1)**. 

[cite_start]Esta plataforma implementa una arquitectura de microservicios basada en contenedores para procesar consultas geoespaciales sobre el dataset *Google Open Buildings* en la Región Metropolitana de Santiago[cite: 1, 32]. [cite_start]El sistema utiliza un patrón de caché *look-aside* para mitigar la carga computacional generada por consultas repetitivas[cite: 4, 23].

[cite_start]Además de su función operativa, el sistema actúa como un banco de pruebas experimental para medir el impacto de distintas configuraciones de memoria, políticas de evicción (LRU, LFU, Random) y Tiempos de Vida (TTL) bajo distribuciones de tráfico Uniforme y de Zipf[cite: 13, 135].

## 🏗️ Arquitectura y Componentes

[cite_start]El ecosistema está compuesto por tres contenedores orquestados a través de Docker Compose[cite: 4, 84]:

1. [cite_start]**`response-gen` (Backend Analítico):** Servicio HTTP *stateless* construido con Flask y NumPy[cite: 14, 15]. [cite_start]Carga el dataset en memoria al iniciar y expone una API REST para procesar 5 tipos de consultas geoespaciales (conteo, densidad, área, etc.) sobre zonas predefinidas (ej. Providencia, Maipú)[cite: 14, 38].
2. [cite_start]**`cache-redis` (Caché en Memoria):** Instancia de Redis que almacena las respuestas serializadas en JSON[cite: 13, 29]. [cite_start]Absorbe la carga de las llaves más "calientes" para reducir la latencia general del sistema[cite: 55].
3. [cite_start]**`traffic-gen` (Generador y Cliente):** Script en Python que simula múltiples clientes inyectando tráfico[cite: 11]. [cite_start]Decide probabilísticamente qué zona consultar (Uniforme o Zipf), consulta a Redis o al backend, y registra la telemetría (HIT/MISS, latencia p50/p95, throughput) en un archivo `metricas_experimento.csv`[cite: 11, 28, 30].

## 🚀 Requisitos Previos

- Docker y Docker Compose instalados.
- [cite_start]Puerto `5000` (Flask) y `6379` (Redis) disponibles en la máquina host[cite: 14, 78].

## 🛠️ Instrucciones de Ejecución

1. Clonar el repositorio y posicionarse en la carpeta raíz.
2. Construir y levantar los contenedores en segundo plano:
   ```bash
   docker-compose up --build
