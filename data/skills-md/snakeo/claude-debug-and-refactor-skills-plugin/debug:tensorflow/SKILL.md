---
name: debug:tensorflow
description: Debug TensorFlow and Keras issues systematically. This skill helps diagnose and resolve machine learning problems including tensor shape mismatches, GPU/CUDA detection failures, out-of-memory errors, NaN/Inf values in loss functions, vanishing/exploding gradients, SavedModel loading errors, and data pipeline bottlenecks. Provides tf.debugging assertions, TensorBoard profiling, eager execution debugging, and version compatibility guidance.
---

# TensorFlow Debugging Guide

This skill provides a systematic approach to debugging TensorFlow applications, covering common error patterns, debugging tools, and resolution strategies.

## Common Error Patterns

### 1. Shape Mismatch Errors

**Symptoms:**
- `InvalidArgumentError: Incompatible shapes`
- `ValueError: Shapes (X,) and (Y,) are incompatible`
- Matrix multiplication failures

**Diagnostic Steps:**
```python
# Print shapes at key points
print(f"Input shape: {x.shape}")
print(f"Expected shape: {model.input_shape}")

# Use tf.debugging for assertions
tf.debugging.assert_shapes([
    (x, ('batch', 'features')),
    (y, ('batch', 'classes'))
])

# Enable eager execution for immediate shape inspection
tf.config.run_functions_eagerly(True)
```

**Common Causes:**
- Batch dimension mismatch (missing or extra dimension)
- Incorrect reshape operations
- Mismatched layer input/output dimensions
- Broadcasting issues with incompatible shapes

**Solutions:**
```python
# Expand dimensions if needed
x = tf.expand_dims(x, axis=0)  # Add batch dimension

# Reshape explicitly
x = tf.reshape(x, [-1, height, width, channels])

# Use tf.ensure_shape for runtime validation
x = tf.ensure_shape(x, [None, 224, 224, 3])
```

### 2. OOM (Out of Memory) Errors

**Symptoms:**
- `ResourceExhaustedError: OOM when allocating tensor`
- `CUDA_ERROR_OUT_OF_MEMORY`
- Training crashes after a few epochs

**Diagnostic Steps:**
```python
# Check GPU memory usage
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        details = tf.config.experimental.get_device_details(gpu)
        print(f"GPU: {gpu.name}, Details: {details}")

# Monitor memory during training
tf.debugging.experimental.enable_dump_debug_info(
    '/tmp/tfdbg2_logdir',
    tensor_debug_mode='FULL_HEALTH',
    circular_buffer_size=1000
)
```

**Solutions:**
```python
# Enable memory growth (prevent TF from allocating all GPU memory)
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Limit GPU memory
tf.config.set_logical_device_configuration(
    gpus[0],
    [tf.config.LogicalDeviceConfiguration(memory_limit=4096)]  # 4GB
)

# Reduce batch size
BATCH_SIZE = 16  # Try smaller values

# Use gradient checkpointing for large models
# (recompute activations during backward pass)

# Clear session between runs
tf.keras.backend.clear_session()

# Use mixed precision training
tf.keras.mixed_precision.set_global_policy('mixed_float16')
```

### 3. NaN/Inf in Loss

**Symptoms:**
- Loss becomes `nan` or `inf` during training
- Model predictions are all NaN
- Gradient norm explodes

**Diagnostic Steps:**
```python
# Enable numeric checking
tf.debugging.enable_check_numerics()

# Check for NaN in tensors
tf.debugging.check_numerics(tensor, "Tensor contains NaN or Inf")

# Use TensorBoard Debugger V2
tf.debugging.experimental.enable_dump_debug_info(
    logdir='/tmp/tfdbg2_logdir',
    tensor_debug_mode='FULL_HEALTH',
    circular_buffer_size=1000
)
```

**Common Causes:**
- Learning rate too high
- Exploding gradients
- Log of zero or negative numbers
- Division by zero
- Incorrect loss function for data range

**Solutions:**
```python
# Reduce learning rate
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)

# Add gradient clipping
optimizer = tf.keras.optimizers.Adam(clipnorm=1.0)
# or
optimizer = tf.keras.optimizers.Adam(clipvalue=0.5)

# Use numerically stable operations
# Instead of: tf.math.log(x)
tf.math.log(x + 1e-7)  # Add epsilon

# Instead of: x / y
tf.math.divide_no_nan(x, y)

# Add batch normalization
model.add(tf.keras.layers.BatchNormalization())

# Check data for NaN before training
assert not tf.reduce_any(tf.math.is_nan(train_data)).numpy()
```

### 4. Gradient Issues

**Symptoms:**
- Vanishing gradients (weights not updating)
- Exploding gradients (loss becomes NaN)
- Training stalls, loss doesn't decrease

**Diagnostic Steps:**
```python
# Inspect gradients with GradientTape
with tf.GradientTape() as tape:
    predictions = model(x, training=True)
    loss = loss_fn(y, predictions)

gradients = tape.gradient(loss, model.trainable_variables)

for var, grad in zip(model.trainable_variables, gradients):
    if grad is not None:
        print(f"{var.name}: grad_norm={tf.norm(grad).numpy():.6f}")
    else:
        print(f"{var.name}: NO GRADIENT (disconnected)")

# Check for dead ReLUs
activations = model.layers[5].output
dead_neurons = tf.reduce_mean(tf.cast(activations <= 0, tf.float32))
```

**Solutions:**
```python
# For vanishing gradients
# Use He initialization for ReLU networks
initializer = tf.keras.initializers.HeNormal()

# Use LeakyReLU instead of ReLU
model.add(tf.keras.layers.LeakyReLU(alpha=0.1))

# Add residual connections (skip connections)

# For exploding gradients
# Apply gradient clipping
gradients, _ = tf.clip_by_global_norm(gradients, 5.0)

# Use proper weight initialization
initializer = tf.keras.initializers.GlorotUniform()
```

### 5. GPU Not Detected

**Symptoms:**
- `tf.config.list_physical_devices('GPU')` returns empty list
- Training runs on CPU (slow)
- CUDA errors on startup

**Diagnostic Steps:**
```python
# Check available devices
print("Physical devices:", tf.config.list_physical_devices())
print("GPU devices:", tf.config.list_physical_devices('GPU'))
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("GPU available:", tf.test.is_gpu_available())

# Check CUDA/cuDNN versions
import subprocess
result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
print(result.stdout)

# Verify TensorFlow GPU package
import tensorflow as tf
print(tf.__version__)
print(tf.sysconfig.get_build_info())
```

**Common Causes:**
- Wrong TensorFlow package (CPU-only version)
- CUDA/cuDNN version mismatch
- NVIDIA driver issues
- GPU not visible to container (Docker)

**Solutions:**
```bash
# Install correct TensorFlow GPU package
pip install tensorflow[and-cuda]  # TF 2.15+
# or
pip install tensorflow-gpu  # Older versions

# Verify CUDA compatibility
# TF 2.15: CUDA 12.x, cuDNN 8.9
# TF 2.14: CUDA 11.8, cuDNN 8.7
# TF 2.13: CUDA 11.8, cuDNN 8.6

# For Docker, use nvidia-docker
docker run --gpus all -it tensorflow/tensorflow:latest-gpu
```

```python
# Force GPU visibility
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU

# Verify GPU is being used
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print(c.device)  # Should show GPU
```

### 6. SavedModel Loading Errors

**Symptoms:**
- `OSError: SavedModel file does not exist`
- `ValueError: Unknown layer` when loading
- Version compatibility errors

**Diagnostic Steps:**
```python
# Check SavedModel structure
import os
for root, dirs, files in os.walk('saved_model_dir'):
    for file in files:
        print(os.path.join(root, file))

# Verify model signature
loaded = tf.saved_model.load('saved_model_dir')
print(list(loaded.signatures.keys()))
```

**Solutions:**
```python
# Save model correctly
model.save('my_model')  # SavedModel format (recommended)
model.save('my_model.keras')  # Keras format

# Load with custom objects
custom_objects = {
    'CustomLayer': CustomLayer,
    'custom_loss': custom_loss
}
model = tf.keras.models.load_model('my_model', custom_objects=custom_objects)

# For version mismatches, save weights only
model.save_weights('model_weights.weights.h5')
# Then rebuild model architecture and load weights
new_model.load_weights('model_weights.weights.h5')
```

### 7. Data Pipeline Issues

**Symptoms:**
- `InvalidArgumentError` during training
- Slow training (input bottleneck)
- Memory leaks during data loading

**Diagnostic Steps:**
```python
# Profile input pipeline
import tensorflow as tf

# Enable profiler
tf.profiler.experimental.start('/tmp/logdir')
# ... run training ...
tf.profiler.experimental.stop()

# Check dataset element spec
print(dataset.element_spec)

# Iterate and inspect
for batch in dataset.take(1):
    print(f"Batch shape: {batch[0].shape}")
    print(f"Dtype: {batch[0].dtype}")
```

**Solutions:**
```python
# Optimize pipeline
dataset = tf.data.Dataset.from_tensor_slices((x, y))
dataset = dataset.cache()  # Cache after expensive operations
dataset = dataset.shuffle(buffer_size=1000)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE)  # Overlap data loading

# Use parallel processing
dataset = dataset.map(
    preprocess_fn,
    num_parallel_calls=tf.data.AUTOTUNE
)

# Handle variable-length sequences
dataset = dataset.padded_batch(32, padded_shapes=([None], []))
```

## Debugging Tools

### tf.debugging Module

```python
# Shape assertions
tf.debugging.assert_shapes([
    (x, ('N', 'H', 'W', 'C')),
    (y, ('N', 'num_classes'))
])

# Value assertions
tf.debugging.assert_non_negative(x)
tf.debugging.assert_near(x, y, rtol=1e-5)
tf.debugging.assert_equal(x.shape, expected_shape)

# Numeric checking
tf.debugging.check_numerics(tensor, "check: tensor contains NaN/Inf")
tf.debugging.enable_check_numerics()  # Global check

# Type assertions
tf.debugging.assert_type(x, tf.float32)
```

### TensorBoard

```python
# Set up TensorBoard logging
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,
    profile_batch='500,520'  # Profile batches 500-520
)

model.fit(
    x_train, y_train,
    epochs=5,
    callbacks=[tensorboard_callback]
)

# Launch TensorBoard
# tensorboard --logdir logs/fit
```

### TensorBoard Debugger V2

```python
# Enable debug info dumping
tf.debugging.experimental.enable_dump_debug_info(
    logdir='/tmp/tfdbg2_logdir',
    tensor_debug_mode='FULL_HEALTH',
    circular_buffer_size=1000
)

# Run training...
model.fit(x_train, y_train, epochs=5)

# View in TensorBoard
# tensorboard --logdir /tmp/tfdbg2_logdir
```

### Eager Execution Debugging

```python
# Enable eager execution (default in TF 2.x)
tf.config.run_functions_eagerly(True)

# Debug with breakpoints in @tf.function
@tf.function
def my_function(x):
    tf.print("Debug:", x)  # Works in graph mode
    # Use tf.debugging.assert_* for runtime checks
    tf.debugging.assert_positive(x)
    return x * 2

# Disable tf.function for debugging
@tf.function
def buggy_function(x):
    # Temporarily remove @tf.function decorator
    # or use tf.config.run_functions_eagerly(True)
    return x
```

### tf.print() for Graph Mode

```python
@tf.function
def compute(x):
    # Regular print won't work in graph mode
    tf.print("Shape:", tf.shape(x))
    tf.print("Values:", x, summarize=-1)  # -1 for all values
    tf.print("Stats - min:", tf.reduce_min(x),
             "max:", tf.reduce_max(x),
             "mean:", tf.reduce_mean(x))
    return x * 2
```

### Memory Profiler

```python
# Profile memory usage
tf.config.experimental.set_memory_growth(gpu, True)

# Use TensorFlow Profiler
with tf.profiler.experimental.Profile('/tmp/logdir'):
    model.fit(x_train, y_train, epochs=1)

# Check memory info
tf.config.experimental.get_memory_info('GPU:0')
# Returns: {'current': bytes, 'peak': bytes}
```

## The Four Phases of TensorFlow Debugging

### Phase 1: Reproduce and Isolate

1. **Create minimal reproduction**
   ```python
   # Minimal test case
   import tensorflow as tf

   # Smallest possible model
   model = tf.keras.Sequential([
       tf.keras.layers.Dense(10, input_shape=(5,))
   ])

   # Synthetic data
   x = tf.random.normal((32, 5))
   y = tf.random.normal((32, 10))

   model.compile(optimizer='adam', loss='mse')
   model.fit(x, y, epochs=1)
   ```

2. **Enable eager execution for line-by-line debugging**
   ```python
   tf.config.run_functions_eagerly(True)
   ```

3. **Add assertions at key points**
   ```python
   def debug_forward_pass(model, x):
       for i, layer in enumerate(model.layers):
           x = layer(x)
           tf.debugging.check_numerics(x, f"Layer {i} output")
           print(f"Layer {i}: {x.shape}, range=[{tf.reduce_min(x):.3f}, {tf.reduce_max(x):.3f}]")
       return x
   ```

### Phase 2: Analyze and Understand

1. **Inspect tensor shapes throughout the pipeline**
   ```python
   def trace_shapes(model, x):
       shapes = []
       for layer in model.layers:
           x = layer(x)
           shapes.append((layer.name, x.shape))
       return shapes
   ```

2. **Check gradient flow**
   ```python
   def analyze_gradients(model, x, y, loss_fn):
       with tf.GradientTape() as tape:
           pred = model(x, training=True)
           loss = loss_fn(y, pred)

       grads = tape.gradient(loss, model.trainable_variables)

       analysis = []
       for var, grad in zip(model.trainable_variables, grads):
           if grad is None:
               analysis.append((var.name, "NONE - disconnected"))
           else:
               norm = tf.norm(grad).numpy()
               analysis.append((var.name, f"norm={norm:.6f}"))
       return analysis
   ```

3. **Profile performance**
   ```python
   # Use tf.profiler
   tf.profiler.experimental.start('/tmp/logdir')
   model.fit(x, y, epochs=1)
   tf.profiler.experimental.stop()
   ```

### Phase 3: Fix and Verify

1. **Apply targeted fixes based on diagnosis**
   - Shape issues: Add explicit reshapes and assertions
   - NaN issues: Add epsilon, reduce learning rate, clip gradients
   - OOM issues: Reduce batch size, enable memory growth
   - GPU issues: Check CUDA compatibility, install correct packages

2. **Verify fix doesn't break other functionality**
   ```python
   # Run comprehensive tests
   def test_model_components():
       # Test forward pass
       output = model(sample_input)
       assert output.shape == expected_shape

       # Test backward pass
       with tf.GradientTape() as tape:
           loss = loss_fn(model(x), y)
       grads = tape.gradient(loss, model.trainable_variables)
       assert all(g is not None for g in grads)

       # Test save/load
       model.save('/tmp/test_model')
       loaded = tf.keras.models.load_model('/tmp/test_model')
       assert tf.reduce_all(model(x) == loaded(x))
   ```

### Phase 4: Prevent and Document

1. **Add permanent assertions for critical invariants**
   ```python
   class RobustModel(tf.keras.Model):
       def call(self, x, training=False):
           tf.debugging.assert_shapes([(x, ('batch', 'features'))])

           x = self.layer1(x)
           tf.debugging.check_numerics(x, "After layer1")

           return self.output_layer(x)
   ```

2. **Set up monitoring callbacks**
   ```python
   class NanCallback(tf.keras.callbacks.Callback):
       def on_batch_end(self, batch, logs=None):
           if logs and tf.math.is_nan(logs.get('loss', 0)):
               self.model.stop_training = True
               raise ValueError(f"NaN detected at batch {batch}")
   ```

3. **Document the issue and solution**
   ```python
   # BUGFIX: Shape mismatch in attention layer
   # Issue: Input was (batch, seq, features) but attention expected (batch, heads, seq, features)
   # Solution: Added reshape before attention layer
   x = tf.reshape(x, [batch_size, num_heads, seq_len, -1])
   ```

## Quick Reference Commands

### Device and Configuration

```python
# List devices
tf.config.list_physical_devices()
tf.config.list_physical_devices('GPU')

# GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Force CPU execution
with tf.device('/CPU:0'):
    result = model(x)

# Check if built with CUDA
tf.test.is_built_with_cuda()
```

### Debugging Assertions

```python
# Numeric checks
tf.debugging.check_numerics(tensor, message)
tf.debugging.enable_check_numerics()

# Shape checks
tf.debugging.assert_shapes([(tensor, shape_tuple)])
tf.ensure_shape(tensor, shape)

# Value checks
tf.debugging.assert_positive(tensor)
tf.debugging.assert_non_negative(tensor)
tf.debugging.assert_near(a, b, rtol=1e-5)
tf.debugging.assert_equal(a, b)
tf.debugging.assert_less(a, b)
tf.debugging.assert_greater(a, b)
```

### Profiling and Logging

```python
# TensorBoard logging
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir='./logs',
    histogram_freq=1
)

# Start profiler
tf.profiler.experimental.start('/tmp/logdir')
# ... code ...
tf.profiler.experimental.stop()

# Debug info for TensorBoard Debugger V2
tf.debugging.experimental.enable_dump_debug_info(
    '/tmp/tfdbg2',
    tensor_debug_mode='FULL_HEALTH'
)
```

### Memory Management

```python
# Clear session
tf.keras.backend.clear_session()

# Get memory info
tf.config.experimental.get_memory_info('GPU:0')

# Mixed precision
tf.keras.mixed_precision.set_global_policy('mixed_float16')
```

### Gradient Debugging

```python
# Inspect gradients
with tf.GradientTape() as tape:
    loss = compute_loss()
gradients = tape.gradient(loss, model.trainable_variables)

# Clip gradients
gradients, _ = tf.clip_by_global_norm(gradients, 5.0)

# Check for None gradients (disconnected graph)
for var, grad in zip(model.trainable_variables, gradients):
    if grad is None:
        print(f"Warning: {var.name} has no gradient")
```

## Version Compatibility Reference

| TensorFlow | Python    | CUDA   | cuDNN |
|------------|-----------|--------|-------|
| 2.16.x     | 3.9-3.12  | 12.3   | 8.9   |
| 2.15.x     | 3.9-3.11  | 12.2   | 8.9   |
| 2.14.x     | 3.9-3.11  | 11.8   | 8.7   |
| 2.13.x     | 3.8-3.11  | 11.8   | 8.6   |
| 2.12.x     | 3.8-3.11  | 11.8   | 8.6   |

## Additional Resources

- [TensorFlow Debugging Guide](https://www.tensorflow.org/guide/effective_tf2#debugging)
- [TensorBoard Debugger V2](https://www.tensorflow.org/tensorboard/debugger_v2)
- [GPU Performance Analysis](https://www.tensorflow.org/guide/gpu_performance_analysis)
- [Profiler Guide](https://www.tensorflow.org/guide/profiler)
