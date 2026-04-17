---
title: Spain News Monitor
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
---

# 🏗️ The Spanish Market Intelligence Refinery 2026

![Status](https://img.shields.io/badge/Status-In%20Production-success?style=for-the-badge&logo=statuspage)
![Market](https://img.shields.io/badge/Market-Northern%20Spain-blue?style=for-the-badge&logo=googlemaps)
![Stack](https://img.shields.io/badge/Stack-Modern%20Data%20Refinery-orange?style=for-the-badge&logo=databricks)

> **"Turning the digital sludge of the Spanish job market into high-purity strategic gold."**

## 🌟 Project Vision
In an era of information overload, this project acts as a **Digital Refinery**. It automatically monitors the pulse of the Spanish news cycle and the tech job market (specifically for the industrial and tech hubs of **Bilbao** and **Gijón**). 

The architecture is built on the principle of **"Purity of Character" (1 Tim 4:12)**: ensuring that every data point served to the dashboard is honest, tested, and deduplicated.

---

## 🍽️ The "Refinery" Architecture (How it Works)
Our system follows a **Decoupled Sibling Structure**, separating Ingestion from Transformation.

1.  **The Ingestion (Mage AI):** Our **Head Chef**. Every 6 hours, it bypasses "Walled Gardens" using an RSS loophole to pull thousands of job postings from LinkedIn and InfoJobs.
2.  **The AI Enrichment (Robertuito NLP):** Our **Specialist Saucier**. A specialized AI model trained on native Spanish text that analyzes the "Mood" of every headline with 99% accuracy.
3.  **The Warehouse (PostgreSQL/DuckDB):** Our **Vault**. A dual-storage strategy optimized for industrial concurrency and local speed.
4.  **The Transformation (dbt):** Our **Bouncer**. It cleans the data using high-level logic (Window Functions, `QUALIFY`) and runs 13+ automated tests to ensure no "Ghost Data" reaches the plate.
5.  **The UI (Streamlit):** Our **Waiter**. A clean, Plotly-powered dashboard that visualizes the "Vibe Check" of the Spanish economy in real-time.

---

## 🛠️ The "Sustainable AI" Tech Stack
| Component | Technology | The Practitioner's Choice |
| :--- | :--- | :--- |
| **Orchestration** | **Mage.ai** | Chosen for its native dbt integration and low-latency DAG execution. |
| **Transformation** | **dbt** | To enforce **Data Purity**. Every model is versioned and tested. |
| **Language AI** | **pysentimiento** | Utilizing the **Robertuito** model for high-fidelity Spanish sentiment analysis. |
| **Visualization** | **Streamlit** | Turning complex SQL Marts into a visual narrative for stakeholders. |
| **Environment** | **Docker** | Creating an **Immutable Refinery** that runs identically in BCN or Bilbao. |

---

## ⚖️ Data Purity & Integrity (The Bouncer's Rules)
We don't trust data; we verify it.
*   **Self-Healing Paths:** The refinery automatically rebuilds its own infrastructure (directories/schema) if the environment is wiped.
*   **Content Fingerprinting:** Deduplication is based on semantic metadata (Title + Company) rather than fragile tracking URLs.

---

## 🚀 Quick Start (Launch the Refinery)
If you have Docker installed, you can start the entire refinery with one command:

```bash
docker-compose up -d
```
*   **Mage Factory:** `localhost:6789`
*   **Job Dashboard:** `localhost:8501`

---

## 🏛️ Architect's Note
This project was built during the spring of 2026 as a strategic bridge to the industrial powerhouses of **Northern Spain**. It represents a commitment to **Infrastructure Sovereignty** and **Sustainable Data Engineering**—minimizing compute waste while maximizing insight purity.

**Built with :coffee: in Barcelona | April 2026.**

---

### 💡 Objective Comparison: Why this approach is superior
*   **vs. Manual Search:** Replaces 4 hours of browsing with a 10-second automated brief.
*   **vs. Basic Scraping:** Avoids IP bans through "Sustainable Fetching" and ensures data longevity via warehouse archiving.
*   **vs. Legacy BI:** dbt-tested logic ensures the "Truth" on the dashboard is never compromised by "Shadow Data."