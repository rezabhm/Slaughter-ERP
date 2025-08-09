<!-- Banner Image -->
<p align="center">
  <img src="https://i.imgur.com/8SgR2aW.png" alt="Slaughterhouse ERP Banner" width="800"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/django-3.2-blue.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

# 🐮 SlaughterERP Service

The `slaughterERP` service is a core component of the Slaughterhouse ERP system. It manages fundamental data related to user accounts, product information, and ownership, providing a centralized source of truth for other microservices.

---

## 📖 Service Overview

This service is responsible for handling the master data of the entire system. It ensures that data for users, roles, products, and units is consistent and accessible to other services that need it. By centralizing this information, we avoid data duplication and maintain a single source of truth.

---

## ✨ Features

- **User and Role Management**: Manages users, roles, and their associations.
- **Product Catalog**: Handles products, product categories, and units of measurement.
- **Contact Management**: Stores contact information.
- **Centralized Data**: Provides a single source of truth for core data models.
- **RESTful API**: Exposes endpoints for managing the core data.

---

## 📦 Data Models

The service manages the following data models:

### Accounts
- **Role**: Represents user roles (e.g., "Admin", "Manager").
- **CustomUser**: An extension of Django's default user model, with added roles.
- **Contact**: Stores contact information for individuals or entities.

### Product
- **Unit**: Defines units of measurement (e.g., "kg", "pcs").
- **ProductCategory**: Organizes products into categories (e.g., "Meat", "By-products").
- **Product**: Represents the actual products, with details like name, code, and category.

---

## Endpoints summary
The service provides a set of RESTful endpoints to manage its data models. The main endpoints are:
- **/api/v1/accounts/**: for user and role management.
- **/api/v1/product/**: for product catalog management.
- **/api/v1/core_ownership/**: for ownership data management.
- **/api/v1/core_transportation/**: for transportation data management.

---

## 🚀 Setup and Installation

To run this service locally, follow these steps:

1.  **Navigate to the service directory**:
    ```bash
    cd slaughterERP/
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```

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
