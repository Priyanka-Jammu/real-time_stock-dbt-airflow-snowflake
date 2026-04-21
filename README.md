# 📊 Real-Time Stock Data Pipeline

**Kafka | MinIO | Airflow | Snowflake | dbt | Power BI**

---

## 🧠 Overview

This project builds a **real-time data pipeline** to ingest, process, transform, and visualize stock market data using modern data engineering tools.

The pipeline collects live stock data from an API, streams it through Kafka, stores it in MinIO, loads it into Snowflake, transforms it using dbt (Bronze → Silver → Gold), and visualizes insights in Power BI.

---

## 💼 Business Context

In real-world scenarios, financial and operations teams rely on near real-time data to monitor performance, detect anomalies, and make timely decisions. However, raw streaming data is often unstructured and not directly usable for analytics.

This pipeline simulates how organizations transform streaming data into structured, analytics-ready datasets to support KPI tracking, trend analysis, and decision-making.

---

## 🏗️ Architecture

```
Finnhub API
     ↓
Kafka (Producer → Topic → Consumer)
     ↓
MinIO (Raw JSON Storage)
     ↓
Airflow (Orchestration)
     ↓
Snowflake (Data Warehouse)
     ↓
dbt (Bronze → Silver → Gold)
     ↓
Power BI (Dashboard)
```

---

## ⚙️ Tech Stack

* **Python** → API ingestion, Kafka producer/consumer
* **Kafka** → Real-time streaming
* **MinIO** → Object storage (S3-compatible)
* **Airflow** → Workflow orchestration
* **Snowflake** → Cloud data warehouse
* **dbt** → Data transformation
* **Power BI** → Data visualization

---

## 🔄 Data Flow

### 1. Producer

* Fetches stock data from API (Finnhub)
* Sends data to Kafka topic (`stock-quotes`)

### 2. Consumer

* Reads messages from Kafka
* Stores JSON files in MinIO bucket

### 3. Airflow DAG

* Downloads files from MinIO
* Uploads to Snowflake stage
* Loads data into Snowflake table

### 4. Snowflake

* Stores raw JSON data in:

```sql
CREATE TABLE BRONZE_STOCK_QUOTES_RAW (
    v VARIANT
);
```

### 5. dbt

* Transforms data into structured layers:

  * Bronze → parsed
  * Silver → cleaned
  * Gold → analytics-ready

---

## 🧱 Data Modeling (dbt Layers)

---

### 🥉 Bronze Layer (Raw → Structured)

* Extracts JSON fields from `VARIANT`
* Converts into structured columns
* Minimal transformation

```sql
SELECT
    v:c::float AS current_price,
    v:symbol::string AS symbol
FROM {{ source('raw', 'BRONZE_STOCK_QUOTES_RAW') }}
```

---

### 🥈 Silver Layer (Cleaned Data)

* Removes null values
* Standardizes numeric precision
* Prepares consistent dataset

```sql
SELECT *
FROM {{ ref('bronze_stg_stock_quotes') }}
WHERE current_price IS NOT NULL
```

---

### 🥇 Gold Layer (Business Insights)

Final models used for analytics and dashboards.

---

#### 📌 1. KPI Model (`gold_kpi.sql`)

```text
Returns the latest price and change metrics for each stock.
```

---

#### 🕯️ 2. Candlestick Model (`gold_candlestick.sql`)

```text
Aggregates stock data into daily open, close, high, low, and trend values.
```

**Candlestick meaning:**

* Open → first price of day
* Close → last price
* High → maximum
* Low → minimum

Used in trading dashboards.

---

#### 📈 3. Volatility Model (`gold_threechart.sql`)

```text
Calculates average price, volatility, and relative volatility for each stock.
```

---

## 📊 What is Volatility? (Simple Explanation)

Volatility measures **how much a stock price moves over time**.

### Example

Low volatility:

```
100 → 101 → 102
```

High volatility:

```
100 → 120 → 80 → 130
```

---

### Calculation

```sql
STDDEV_POP(current_price)
```

* Measures spread of values
* Higher = more fluctuation

---

### Relative Volatility

```sql
STDDEV / AVG
```

* Normalizes volatility
* Helps compare stocks

---

## 📊 Analytical Insights

This pipeline enables:

- Tracking real-time stock performance using KPI metrics  
- Identifying trends and price movements over time  
- Comparing volatility across stocks to assess stability and risk  
- Supporting data-driven decisions similar to financial analytics and operations monitoring  

These insights demonstrate how raw data can be transformed into actionable intelligence for business use cases.

---

## ⚙️ dbt Concepts

### 🔹 source()

```sql
{{ source('raw', 'BRONZE_STOCK_QUOTES_RAW') }}
```

Refers to existing Snowflake table.

---

### 🔹 ref()

```sql
{{ ref('silver_clean_stock_quotes') }}
```

References another dbt model.

---

### 🔹 version: 2

Used in YAML files for defining sources and metadata.

---

## 🧩 Materialization Strategy

| Layer  | Materialization |
| ------ | --------------- |
| Bronze | View            |
| Silver | View            |
| Gold   | Table           |

### Why?

* Views → fast, lightweight
* Tables → better performance for dashboards

---

## 📊 Power BI Dashboard
<img width="1132" height="632" alt="image" src="https://github.com/user-attachments/assets/d38cc3e5-6a44-4f76-b143-aedaf07b10e4" />


### 🧠 Overview

The Power BI dashboard visualizes the gold layer data.

---

### 📌 Components

#### 🔹 KPI Cards

* Latest stock prices (AAPL, AMZN, GOOGL, MSFT, TSLA)

#### 🔹 Gauge Charts

* Shows volatility levels

#### 🔹 Change Percent Chart

* Green → positive
* Red → negative

#### 🔹 Candlestick Chart

* Shows daily stock movement

#### 🔹 Tree Map

* Compares stock performance and volatility

---

### 🔗 Data Source

Power BI connects to:

* `gold_kpi`
* `gold_candlestick`
* `gold_threechart`

---

## 🚀 How to Run

### 1. Start services

```bash
docker compose up -d
```

---

### 2. Run Producer

```bash
python producer.py
```

---

### 3. Run Consumer

```bash
python consumer.py
```

---

### 4. Run Airflow

* Open: `http://localhost:8080`
* Trigger DAG: `minio_to_snowflake`

---

### 5. Run dbt

```bash
dbt run
```

---

## 🎯 Key Takeaways

This project demonstrates my ability to not only build data pipelines, but also transform data into meaningful insights that support business decision-making — which is critical for analytics-driven roles.
* Built end-to-end real-time data pipeline
* Implemented modern architecture (Bronze → Silver → Gold)
* Used Kafka for streaming and Snowflake for warehousing
* Applied dbt for scalable transformations
* Created Power BI dashboard for business insights

---

## 📌 Future Improvements

* Add incremental dbt models
* Add dbt tests (data quality)
* Integrate alerting in Airflow
* Optimize for production scalability

---

## 👤 Author

**Priyanka Jammu**
Data Engineer | Analytics Engineer
Tampa, FL

---
