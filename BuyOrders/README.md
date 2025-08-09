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

# 🛒 BuyOrders Service

The `BuyOrders` service is responsible for managing all procurement-related activities in the Slaughterhouse ERP system. It handles the creation and tracking of purchase orders, from initiation to completion.

---

## 📖 Service Overview

This service provides the necessary tools to manage the company's purchasing operations. It allows users to create purchase orders, track their status, and manage related information like pricing and delivery details. The service uses a combination of MongoDB and Elasticsearch to store and search data efficiently.

---

## ✨ Features

- **Purchase Order Management**: Create, track, and manage purchase orders.
- **Status Tracking**: Follow the status of each order (e.g., "pending", "verified", "received").
- **MongoDB Backend**: Uses MongoDB for flexible and scalable data storage.
- **Elasticsearch Integration**: Provides powerful search and filtering capabilities.
- **GraphQL API**: Offers a GraphQL endpoint for flexible data querying.
- **RESTful API**: Exposes REST endpoints for managing purchase orders.

---

## 📦 Data Models

The service uses `mongoengine` to define its data models as MongoDB documents. The core document is:

- **ProductionOrder**: Represents a purchase order with the following key fields:
    - `id`: A unique identifier for the order.
    - `car`: A reference to the vehicle used for transportation.
    - `order_information`: Details about the product being ordered.
    - `required_weight`: The required weight of the product.
    - `status`: The current status of the order.
    - `price`: The price of the order.

---

## API Endpoints
The main endpoints for this service are:
- **/api/v1/buy/**: for managing buy orders.
- **/api/v1/order/**: for managing generic order information.
- **/api/v1/core/**: for core data related to buying.

---

## 🚀 Setup and Installation

To run this service locally, follow these steps:

1.  **Navigate to the service directory**:
    ```bash
    cd BuyOrders/
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
