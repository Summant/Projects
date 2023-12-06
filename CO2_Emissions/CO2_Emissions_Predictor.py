import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


data = pd.read_csv("CO2_Emissions_train.csv")
target_column = "CO2 Emissions(g/km)"
X = data.drop(columns=[target_column])
y = data[target_column]

categorical_columns = X.select_dtypes(include=['object']).columns.tolist()
numerical_columns = X.select_dtypes(exclude=['object']).columns.tolist()

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical data
scaler = StandardScaler()
X_train[numerical_columns] = scaler.fit_transform(X_train[numerical_columns])
X_test[numerical_columns] = scaler.transform(X_test[numerical_columns])

# Build model
input_layers = []
embedding_layers = []

for col in categorical_columns:
    input_layer = tf.keras.layers.Input(shape=(1,), name=f"{col}_input")
    embedding_layer = tf.keras.layers.Embedding(X[col].max() + 1, 5, input_length=1)(input_layer)
    embedding_layer = tf.keras.layers.Flatten()(embedding_layer)
    input_layers.append(input_layer)
    embedding_layers.append(embedding_layer)

numerical_input = tf.keras.layers.Input(shape=(len(numerical_columns),), name="numerical_input")
input_layers.append(numerical_input)

merged_layers = tf.keras.layers.concatenate(embedding_layers + [numerical_input])
output_layer = tf.keras.layers.Dense(1, activation='linear')(merged_layers)

model = tf.keras.Model(inputs=input_layers, outputs=output_layer)

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit([X_train[col] for col in categorical_columns] + [X_train[numerical_columns]], y_train, epochs=50, batch_size=32, validation_data=([X_test[col] for col in categorical_columns] + [X_test[numerical_columns]], y_test))


# test data
test_data = pd.read_csv("CO2_Emissions_Eval.csv")
for col, le in label_encoders.items():
    test_data[col] = le.transform(test_data[col])
test_data[numerical_columns] = scaler.transform(test_data[numerical_columns])

# Make predictions on the test data
test_inputs = [test_data[col] for col in categorical_columns] + [test_data[numerical_columns]]
predictions = model.predict(test_inputs)
print(f'Predictions: {predictions[0][0]:.2f} g/km')
