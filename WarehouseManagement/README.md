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

# 🏭 WarehouseManagement Service

The `WarehouseManagement` service is responsible for managing inventory and warehouse operations within the Slaughterhouse ERP system. It tracks the movement of products in and out of the warehouses and maintains an accurate inventory count.

---

## 📖 Service Overview

This service provides a comprehensive solution for warehouse management. It allows users to manage multiple warehouses, track inventory levels, and record all transactions (imports and exports). By using MongoDB, the service can handle complex inventory data and provide real-time updates.

---

## ✨ Features

- **Warehouse Management**: Create and manage multiple warehouses.
- **Inventory Tracking**: Keep track of the quantity and shelf life of products in each warehouse.
- **Transaction Logging**: Record all inventory movements, including imports and exports.
- **MongoDB Backend**: Utilizes MongoDB for flexible and scalable data storage.
- **Elasticsearch Integration**: Provides powerful search and filtering capabilities.
- **GraphQL API**: Offers a GraphQL endpoint for flexible data querying.
- **RESTful API**: Exposes REST endpoints for managing warehouses and inventory.

---

## 📦 Data Models

The service uses `mongoengine` to define its data models as MongoDB documents. The core documents are:

- **Warehouse**: Represents a physical warehouse with a name, description, and status.
- **Inventory**: Represents the stock of a specific product in a warehouse. It includes the product, quantity, and shelf life.
- **Transaction**: Records the movement of inventory, such as when a product is imported into or exported from a warehouse.
- **Quantity**: An embedded document that stores the weight and number of a product.
- **ShelfLife**: An embedded document that stores the production and expiration dates of a product.

---

## API Endpoints
The main endpoints for this service are:
- **/api/v1/warehouse/**: for managing warehouses, inventory, and transactions.
- **/api/v1/core/**: for core data related to warehouse management.

---

## 🚀 Setup and Installation

To run this service locally, follow these steps:

1.  **Navigate to the service directory**:
    ```bash
    cd WarehouseManagement/
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
