---
name: deep-learning
description: "Comprehensive guide for Deep Learning with Keras 3 (Multi-Backend: JAX, TensorFlow, PyTorch). Use when building neural networks, CNNs for computer vision, RNNs/Transformers for NLP, time series forecasting, or generative models (VAEs, GANs). Covers model building (Sequential/Functional/Subclassing APIs), custom training loops, data augmentation, transfer learning, and production best practices."
---

# Deep Learning with Keras 3
 
Patterns and best practices based on *Deep Learning with Python, 2nd Edition* by François Chollet, updated for Keras 3 (Multi-Backend).

## Core Workflow

1. **Prepare Data**: Normalize, split train/val/test, create `tf.data.Dataset`
2. **Build Model**: Sequential, Functional, or Subclassing API
3. **Compile**: `model.compile(optimizer, loss, metrics)`
4. **Train**: `model.fit(data, epochs, validation_data, callbacks)`
5. **Evaluate**: `model.evaluate(test_data)`

## Model Building APIs

**Sequential** - Simple stack of layers:
```python
model = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax")
])
```

**Functional** - Multi-input/output, shared layers, non-linear topologies:
```python
inputs = keras.Input(shape=(64,))
x = layers.Dense(64, activation="relu")(inputs)
outputs = layers.Dense(10, activation="softmax")(x)
model = keras.Model(inputs=inputs, outputs=outputs)
```

**Subclassing** - Full flexibility with `call()` method:
```python
class MyModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = layers.Dense(64, activation="relu")
        self.dense2 = layers.Dense(10, activation="softmax")

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)
```

## Quick Reference: Loss & Optimizer Selection

| Task | Loss | Final Activation |
|------|------|------------------|
| Binary classification | `binary_crossentropy` | `sigmoid` |
| Multiclass (one-hot) | `categorical_crossentropy` | `softmax` |
| Multiclass (integers) | `sparse_categorical_crossentropy` | `softmax` |
| Regression | `mse` or `mae` | None |

**Optimizers**: `rmsprop` (default), `adam` (popular), `sgd` (with momentum for fine-tuning)

## Domain-Specific Guides

| Topic | Reference | When to Use |
|-------|-----------|-------------|
| **Keras 3 Migration** | [keras3_changes.md](references/keras3_changes.md) | **START HERE**: Multi-backend setup, `keras.ops`, `import keras` |
| **Fundamentals** | [basics.md](references/basics.md) | Overfitting, regularization, data prep, K-fold validation |
| **Keras Deep Dive** | [keras_working.md](references/keras_working.md) | Custom metrics, callbacks, training loops, `tf.function` |
| **Computer Vision** | [computer_vision.md](references/computer_vision.md) | Convnets, data augmentation, transfer learning |
| **Advanced CV** | [advanced_cv.md](references/advanced_cv.md) | Segmentation, ResNets, Xception, Grad-CAM |
| **Time Series** | [timeseries.md](references/timeseries.md) | RNNs (LSTM/GRU), 1D convnets, forecasting |
| **NLP & Transformers** | [nlp_transformers.md](references/nlp_transformers.md) | Text processing, embeddings, Transformer encoder/decoder |
| **Generative DL** | [generative_dl.md](references/generative_dl.md) | Text generation, VAEs, GANs, style transfer |
| **Best Practices** | [best_practices.md](references/best_practices.md) | KerasTuner, mixed precision, multi-GPU, TPU |

## Essential Callbacks

```python
callbacks = [
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=3),
    keras.callbacks.ModelCheckpoint("best.keras", save_best_only=True),
    keras.callbacks.TensorBoard(log_dir="./logs")
]
model.fit(..., callbacks=callbacks)
```

## Utility Scripts

| Script | Description |
|--------|-------------|
| [quick_train.py](scripts/quick_train.py) | Reusable training template with standard callbacks and history plotting |
| [visualize_filters.py](scripts/visualize_filters.py) | Visualize convnet filter patterns via gradient ascent |
