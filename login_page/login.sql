USE Personal_Finance_Management;;

CREATE TABLE if not exists User (
  user_id INT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  registered_date DATE NOT NULL,
  dob DATE NOT NULL,
  mobile_number VARCHAR(20) NOT NULL,
  email VARCHAR(100) unique NOT NULL
);;

CREATE TABLE if not exists Account (
  account_id BIGINT PRIMARY KEY,
  bank_name VARCHAR(50) NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  ifsc_code VARCHAR(20) NOT NULL,
  account_type VARCHAR(20) NOT NULL,
  balance DECIMAL(20, 2) NOT NULL,
  nominee_name VARCHAR(100) NOT NULL,
  interest_rate DECIMAL(5, 2) NOT NULL,
  open_date DATE NOT NULL
);;

CREATE TABLE IF NOT EXISTS Income (
  income_id INT PRIMARY KEY,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  account_id BIGINT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES Account(account_id),
  amount DECIMAL(15, 2) NOT NULL,
  income_date DATE NOT NULL,
  source VARCHAR(255) NOT NULL,
  remarks VARCHAR(255) not null,
  category VARCHAR(255) NOT NULL
);;

CREATE TABLE if not exists Expenditure (
  expense_id INT PRIMARY KEY,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  account_id BIGINT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES Account(account_id),
  expense DECIMAL(15, 2) NOT NULL,
  category VARCHAR(50) NOT NULL,
  expense_date DATE NOT NULL,
  source VARCHAR(255) NOT NULL,
  remarks VARCHAR(255) not null
);;

CREATE TABLE if not exists Investment (
  investment_id INT PRIMARY KEY,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES User(user_id),
  account_id BIGINT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES Account(account_id),
  investment_type VARCHAR(50) NOT NULL,
  investment_name VARCHAR(100) NOT NULL,
  purchase_date DATE NOT NULL,
  purchase_price DECIMAL(15, 2) NOT NULL,
  current_value DECIMAL(15, 2) not null,
  return_rate DECIMAL(5,2) NOT NULL,
  number_of_units DECIMAL(15, 5) not null,
  remarks VARCHAR(255) not null
);;