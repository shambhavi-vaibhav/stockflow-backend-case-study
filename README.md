# StockFlow - B2B Inventory Management System

This repository contains the technical solution for the **Bynry Backend Engineering Intern** case study. 

##📄 Detailed Documentation & Analysis
For a deep dive into the architectural decisions, database normalization logic, and scalability strategies (including the Expert, Architect, and Builder perspectives), please refer to the full case study document:
https://docs.google.com/document/d/1p9gihZxd7Y-0ADakc2hTAivPOT0dIIM5Q5j64bGEPss/edit?tab=t.0

## 🚀 Project Overview
StockFlow is a specialized SaaS platform designed for small businesses to manage inventory across multiple warehouses. This solution addresses core backend challenges: data integrity, scalable database design, and intelligent alerting.

## 🛠️ Key Components

### 1. API Debugging & Optimization
- **Atomicity:** Refactored the product creation flow to use a single database transaction, preventing "ghost products."
- **Validation:** Implemented strict input validation for SKUs, pricing (using Decimal for precision), and warehouse existence.
- **Error Handling:** Added comprehensive try-except blocks with proper HTTP status codes (201, 400, 409, 500).

### 2. Database Schema Design
Designed a normalized PostgreSQL-ready schema that supports:
- **Multi-Tenancy:** Scoped by `companies`.
- **Complex Inventory:** Multi-warehouse support with an immutable audit log (`inventory_changes`).
- **Product Bundling:** Self-referencing many-to-many relationship for kit/bundle management.
- **Supplier Mapping:** Optimized for preferred supplier tracking.

### 3. Low-Stock Alert Engine
Implemented a business-centric API to identify items at risk.
- **Sales Velocity:** Calculates `days_until_stockout` based on historical sales data.
- **Threshold Management:** Supports variable thresholds based on product categories.
- **Performance:** Optimized using subqueries and batch-fetching to avoid the N+1 problem.

## 📂 File Structure
- `part1_debugging.py`: Corrected Flask/SQLAlchemy logic.
- `part2_schema.sql`: Full DDL with indexing and constraints.
- `part3_api.py`: Implementation of the Alerting API.

---
**Candidate:** Shambhavi Vaibhav  
**Role:** Backend Engineering Intern (Case Study)
