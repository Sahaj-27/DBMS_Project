WITH UserInfo AS (
      SELECT user_id, username, email, mobile_number, dob, registered_date
      FROM User
      WHERE user_id = {user_id}
    ),
    AccountInfo AS (
      SELECT COUNT(*) as num_accounts
      FROM Account
      WHERE user_id = {user_id}
    ),
    TransactionInfo AS (
      SELECT COUNT(*) as num_transactions
      FROM (
        SELECT income_id as trans_id FROM Income WHERE user_id = {user_id}
        UNION ALL
        SELECT expense_id as trans_id FROM Expenditure WHERE user_id = {user_id}
      ) t
    ),
    InvestmentInfo AS (
      SELECT COUNT(*) as num_investments
      FROM Investment
      WHERE user_id = {user_id}
    )
    SELECT CONCAT('User ID = ', user_id) as info
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('User Name = ', username) 
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('E Mail = ', email) 
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('Mobile Number = ', mobile_number) 
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('DOB = ', dob) 
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('Registered Date = ', registered_date)
    FROM UserInfo
    UNION ALL
    SELECT CONCAT('# of Accounts = ', num_accounts) 
    FROM AccountInfo
    UNION ALL
    SELECT CONCAT('# of Transactions = ', num_transactions) 
    FROM TransactionInfo
    UNION ALL
    SELECT CONCAT('# of Investments = ', num_investments) 
    FROM InvestmentInfo;