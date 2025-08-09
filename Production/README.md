<!-- Banner Image -->
<p align="center">
  <img src="https://i.imgur.com/8SgR2aW.png" alt="Slaughterhouse ERP Banner" width="800"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/django-3.2-blue.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/mongodb-4.4-brightgreen.svg" alt="MongoDB Version">
  <img src="https://img.shields.io/badge/elasticsearch-7.x-005571.svg" alt="Elasticsearch Version">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

# 🛠️ Production Service

The `Production` service is the core of the Slaughterhouse ERP system, managing the entire production process from raw material intake to finished goods output.

---

## 📖 Service Overview

This service orchestrates the production workflow, including planning, execution, and tracking. It handles the import of raw materials, the production process itself, and the export of finished products. The service is designed to provide a detailed, real-time view of all production activities.

---

## ✨ Features

- **Production Planning**: Plan and manage production runs.
- **Production Execution**: Track the production process through multiple stages.
- **Material Import**: Manage the import of raw materials from various sources.
- **Finished Goods Export**: Handle the export of finished products.
- **Product Returns**: Process product returns.
- **MongoDB Backend**: Utilizes MongoDB for flexible and scalable data storage.
- **Elasticsearch Integration**: Provides powerful search and filtering capabilities.
- **GraphQL API**: Offers a GraphQL endpoint for flexible data querying.
- **RESTful API**: Exposes REST endpoints for managing production processes.

---

## 📦 Data Models

The service uses `mongoengine` to define its data models as MongoDB documents. The core documents are:

- **ProductionSeries**: Represents a production run, with a unique ID and status.
- **ImportProduct**: Models the import of raw materials, with seven distinct steps from entrance to finish.
- **ImportProductFromWareHouse**: Manages the import of products from a warehouse for production.
- **ExportProduct**: Represents the export of finished products.
- **ReturnProduct**: Handles the return of products from sales or production.
- **PoultryCuttingProduction**: Manages the poultry cutting process, a specific type of production.

---

## API Endpoints
The main endpoints for this service are:
- **/api/v1/production/**: for managing production series, import, export, and returns.
- **/api/v1/poultry_cutting_production/**: for managing the poultry cutting process.
- **/api/v1/planning/**: for production planning.
- **/api/v1/core/**: for core data related to production.

---

## 🚀 Setup and Installation

To run this service locally, follow these steps:

1.  **Navigate to the service directory**:
    ```bash
    cd Production/
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment**:
    - Make sure you have a running instance of MongoDB and Elasticsearch.
    - Create a `.env` file and set the necessary environment variables (e.g., database connection strings).

4.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```

---

## 🤝 Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).
