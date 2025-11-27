-- schema.sql
CREATE DATABASE IF NOT EXISTS carols_ims;
USE carols_ims;

-- categories table
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(64) NOT NULL UNIQUE, -- e.g., bev-cof
  name VARCHAR(128) NOT NULL,
  parent_id INT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- products table
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_code VARCHAR(64) UNIQUE, -- optional product code/id
  name VARCHAR(255) NOT NULL,
  category_id INT NULL,
  price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  current_quantity INT NOT NULL DEFAULT 0,
  reorder_threshold INT NULL,
  archived TINYINT(1) NOT NULL DEFAULT 0, -- 0 = active, 1 = archived (soft-delete)
  created_by INT NULL,
  last_updated_by INT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
  INDEX idx_name (name),
  INDEX idx_category (category_id)
);

-- optional: users table minimal for storing user ids (used in last_updated_by)
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(128) UNIQUE NOT NULL,
  role VARCHAR(32) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
