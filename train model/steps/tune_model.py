from sklearn.metrics import mean_absolute_error
import optuna
import xgboost as xgb
import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def tune_model(file_dirs, CONFIG):

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_uniform('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_uniform('subsample', 0.5, 1),
            'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1),
            'gamma': trial.suggest_uniform('gamma', 0, 1)
        }
        
        # Train and evaluate the model with the current hyperparameters
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = mean_absolute_error(y_test, y_pred)
        
        return score

    # Load data
    train_df = pd.read_csv(file_dirs['train-data-dir'], index_col='datetime')
    test_df = pd.read_csv(file_dirs['test-data-dir'], index_col='datetime')

    # Split target and features
    target_columns = ['temperature_3', 'temperature_6', 'temperature_9', 'temperature_12',
                       'temperature_15', 'temperature_18', 'temperature_21', 'temperature_24']
    X_train = train_df.drop(target_columns, axis=1)
    y_train = train_df[target_columns]
    X_test = test_df.drop(target_columns, axis=1)
    y_test = test_df[target_columns]

    # Run the optimization with Optuna
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=100)
    
    params = study.best_params

    # Print the best hyperparameters and score
    print('Best hyperparameters: ', params)
    print('Best score: ', study.best_value)

    # Change HP in config on tunned
    for key in params:
        if params[key] is not None:
            CONFIG['params'][key] = params[key] 

    print(f"{bcolors.WARNING}Config HP settings was changed on tunned HP{bcolors.ENDC}")

    return study.best_params