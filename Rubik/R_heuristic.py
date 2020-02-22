import pandas as pd
import numpy as np
import pickle
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

df_X = pd.read_pickle("states.pickle").to_numpy()
df_y = pd.read_pickle("lens.pickle").to_numpy()

# Parameters
rand_seed = 42

X_train, X_test, y_train, y_test = train_test_split(
    df_X, df_y, test_size=0.33, random_state=42
    )


print(f"Training model with {len(X_train)} on data points")
M = MLPRegressor(hidden_layer_sizes=(100, 100, 100, 100), verbose=1)
Model = M.fit(X_train, y_train.ravel())
print(f"Training complete.")

Model.score(X_test, y_test.ravel())

# Filename
f = "Rubik_scramble_heuristic_2.sav"

print(f"Attempting to save model as {f}...")
pickle.dump(Model, open(f, 'wb'))
print(f"Model saved as {f}")
