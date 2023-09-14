CONFIG = {
    # Postgres connection
    'db_host' : 'localhost',
    'db_name' : 'postgres',
    'db_user' : 'username',
    'db_password' : 'qwerty',
    'db_port' : 5432,
    # Using date datetime limits to have reproducibility of data
    'date_from' : '2002-01-01 00:00:00.000', 
    'date_to': '2023-01-01 00:00:00.000',
    # Train/val/test split
    'val_size': 0.2,
    'test_size': 0.1,
    # Hyperparameters
    'params': {
        'n_estimators': 772,
        'max_depth': 8,
        'learning_rate': 0.04088,
        'subsample': 0.83884,
        'colsample_bytree': 0.97662,
        'gamma': 0.00317
    }
}