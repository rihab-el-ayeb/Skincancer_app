-- Create and use the database
CREATE DATABASE skin_cancer_db;
USE skin_cancer_db;

-- Users table for authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);

-- Patients table for diagnosis history
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    result VARCHAR(20) NOT NULL,
    probability FLOAT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: 1234)
INSERT INTO users (username, password) VALUES ('admin', '1234');