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

# 💰 SaleOrders Service

The `SaleOrders` service manages all sales-related operations within the Slaughterhouse ERP system. It handles the process of selling products, from loading them onto trucks to tracking their delivery.

---

## 📖 Service Overview

This service is designed to streamline the sales workflow. It allows users to manage the loading of trucks, track the weight of products being sold, and record sales transactions. By using MongoDB, the service can handle a large volume of sales data and provide fast, efficient querying.

---

## ✨ Features

- **Sales Order Management**: Manages the entire sales process, from truck loading to final sale.
- **Truck Loading and Weighing**: Tracks the loading of trucks and records their weight at different stages.
- **Product Loading**: Manages the products being loaded onto trucks for sale.
- **MongoDB Backend**: Utilizes MongoDB for flexible and scalable data storage.
- **Elasticsearch Integration**: Provides powerful search and filtering capabilities.
- **GraphQL API**: Offers a GraphQL endpoint for flexible data querying.
- **RESTful API**: Exposes REST endpoints for managing sales orders.

---

## 📦 Data Models

The service uses `mongoengine` to define its data models as MongoDB documents. The core documents are:

- **TruckLoading**: Represents the process of loading a truck with products for sale. It includes details about the car, weight, and buyer.
- **CarWeight**: An embedded document that stores the weight of a truck at a specific point in time.
- **LoadedProduct**: Represents a product that has been loaded onto a truck for sale. It includes information about the product, price, and car.
- **LoadedProductItem**: Represents a specific item of a loaded product, with its weight and number.

---

## API Endpoints
The main endpoints for this service are:
- **/api/v1/sale/**: for managing sales and truck loading.
- **/api/v1/order/**: for managing sales orders.
- **/api/v1/core/**: for core data related to sales.

---

## 🚀 Setup and Installation

To run this service locally, follow these steps:

1.  **Navigate to the service directory**:
    ```bash
    cd SaleOrders/
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
