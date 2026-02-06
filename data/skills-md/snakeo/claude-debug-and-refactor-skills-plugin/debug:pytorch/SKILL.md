---
name: debug:pytorch
description: Debug PyTorch issues systematically. Use when encountering tensor errors, CUDA out of memory errors, gradient problems like NaN loss or exploding gradients, shape mismatches between layers, device conflicts between CPU and GPU, autograd graph issues, DataLoader problems, dtype mismatches, or training instabilities in deep learning workflows.
---

# PyTorch Debugging Guide

This guide provides systematic approaches to debugging PyTorch models, from common tensor errors to complex training issues.

## Common Error Patterns

### 1. CUDA Out of Memory (OOM)

**Error Message:**
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Causes:**
- Batch size too large for GPU memory
- Accumulating gradients without clearing
- Storing tensors on GPU unnecessarily
- Memory leaks from not detaching tensors

**Solutions:**
```python
# Check current memory usage
print(torch.cuda.memory_summary(device=None, abbreviated=False))
print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"Cached: {torch.cuda.memory_reserved() / 1e9:.2f} GB")

# Clear cache
torch.cuda.empty_cache()

# Reduce batch size
batch_size = batch_size // 2

# Use gradient checkpointing for large models
from torch.utils.checkpoint import checkpoint
output = checkpoint(self.heavy_layer, input)

# Use mixed precision training
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
with autocast():
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

# Detach tensors when storing for logging
logged_loss = loss.detach().cpu().item()

# Use gradient accumulation instead of large batches
accumulation_steps = 4
for i, (inputs, labels) in enumerate(dataloader):
    outputs = model(inputs)
    loss = criterion(outputs, labels) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 2. Tensor Size/Shape Mismatch

**Error Message:**
```
RuntimeError: size mismatch, m1: [32 x 512], m2: [256 x 10]
RuntimeError: The size of tensor a (64) must match the size of tensor b (32)
```

**Causes:**
- Incorrect layer dimensions
- Wrong tensor reshaping
- Mismatched batch sizes
- Incorrect input preprocessing

**Solutions:**
```python
# Debug by printing shapes at each layer
class DebugModel(nn.Module):
    def forward(self, x):
        print(f"Input shape: {x.shape}")
        x = self.layer1(x)
        print(f"After layer1: {x.shape}")
        x = self.layer2(x)
        print(f"After layer2: {x.shape}")
        return x

# Add shape assertions as contracts
def forward(self, x):
    assert x.dim() == 4, f"Expected 4D input, got {x.dim()}D"
    assert x.shape[1] == 3, f"Expected 3 channels, got {x.shape[1]}"
    # ... rest of forward pass

# Use einops for clearer reshaping
from einops import rearrange
x = rearrange(x, 'b c h w -> b (c h w)')

# Calculate dimensions programmatically
def _get_conv_output_size(self, shape):
    with torch.no_grad():
        dummy = torch.zeros(1, *shape)
        output = self.conv_layers(dummy)
        return output.numel()
```

### 3. NaN in Gradients/Loss

**Error Message:**
```
Loss is nan
RuntimeError: Function 'XXXBackward' returned nan values
```

**Causes:**
- Learning rate too high
- Numerical instability in operations
- Division by zero
- Log of zero or negative numbers
- Exploding gradients

**Solutions:**
```python
# Enable anomaly detection to find the source
torch.autograd.set_detect_anomaly(True)

# Check for NaN in tensors
def check_nan(tensor, name="tensor"):
    if torch.isnan(tensor).any():
        print(f"NaN detected in {name}")
        print(f"Shape: {tensor.shape}")
        print(f"NaN count: {torch.isnan(tensor).sum()}")
        raise ValueError(f"NaN in {name}")

# Add epsilon for numerical stability
eps = 1e-8
log_probs = torch.log(probs + eps)
normalized = x / (x.norm() + eps)

# Gradient clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)

# Check gradients after backward
def check_gradients(model):
    for name, param in model.named_parameters():
        if param.grad is not None:
            if torch.isnan(param.grad).any():
                print(f"NaN gradient in {name}")
            if torch.isinf(param.grad).any():
                print(f"Inf gradient in {name}")
            grad_norm = param.grad.norm()
            print(f"{name}: grad_norm = {grad_norm:.4f}")

# Use stable loss functions
# BAD: nn.CrossEntropyLoss on softmax output
# GOOD: nn.CrossEntropyLoss on logits (raw scores)
loss = nn.CrossEntropyLoss()(logits, targets)  # Not softmax(logits)
```

### 4. Device Mismatch (CPU/GPU)

**Error Message:**
```
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
RuntimeError: Input type (torch.cuda.FloatTensor) and weight type (torch.FloatTensor) should be the same
```

**Causes:**
- Model on GPU, data on CPU (or vice versa)
- Loading model saved on different device
- Creating new tensors without specifying device
- Mixing tensors from different GPUs

**Solutions:**
```python
# Always explicitly move to device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
inputs = inputs.to(device)
targets = targets.to(device)

# Load model with map_location
model.load_state_dict(torch.load('model.pt', map_location=device))

# Create tensors on the correct device
new_tensor = torch.zeros(10, device=device)
new_tensor = torch.zeros_like(existing_tensor)  # Same device as existing

# Check device of all model parameters
def check_model_device(model):
    devices = {p.device for p in model.parameters()}
    print(f"Model parameters on devices: {devices}")

# Debug device issues
print(f"Model device: {next(model.parameters()).device}")
print(f"Input device: {inputs.device}")
print(f"Target device: {targets.device}")
```

### 5. Autograd Graph Issues

**Error Message:**
```
RuntimeError: Trying to backward through the graph a second time
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

**Causes:**
- Calling backward() twice without retain_graph
- In-place operations on tensors requiring gradients
- Detaching tensors incorrectly
- Not enabling gradients on input tensors

**Solutions:**
```python
# For multiple backward passes
loss.backward(retain_graph=True)  # Use sparingly - memory intensive

# Avoid in-place operations on tensors with gradients
# BAD:
x += 1
x[0] = 0
x.add_(1)

# GOOD:
x = x + 1
x = x.clone()
x[0] = 0

# Ensure requires_grad is set
input_tensor = torch.randn(10, requires_grad=True)

# Clone before in-place modification
x_modified = x.clone()
x_modified[0] = 0

# Check if tensor has gradient function
print(f"requires_grad: {tensor.requires_grad}")
print(f"grad_fn: {tensor.grad_fn}")
print(f"is_leaf: {tensor.is_leaf}")

# Properly detach for logging/storage
logged_value = tensor.detach().cpu().numpy()
```

### 6. DataLoader Problems

**Error Message:**
```
RuntimeError: DataLoader worker (pid X) is killed
BrokenPipeError: [Errno 32] Broken pipe
RuntimeError: Cannot re-initialize CUDA in forked subprocess
```

**Causes:**
- Too many workers
- Memory issues in workers
- CUDA operations before DataLoader fork
- Shared memory issues

**Solutions:**
```python
# Reduce number of workers
dataloader = DataLoader(dataset, batch_size=32, num_workers=2)

# Use spawn instead of fork for CUDA
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)

# Pin memory for faster GPU transfer (but uses more memory)
dataloader = DataLoader(dataset, pin_memory=True)

# Increase shared memory for Docker
# In docker-compose.yml: shm_size: '2gb'

# Debug DataLoader issues
dataloader = DataLoader(dataset, num_workers=0)  # Single process for debugging

# Use persistent workers to avoid respawning
dataloader = DataLoader(dataset, num_workers=4, persistent_workers=True)

# Custom collate function with error handling
def safe_collate(batch):
    try:
        return torch.utils.data.dataloader.default_collate(batch)
    except Exception as e:
        print(f"Collate error: {e}")
        print(f"Batch: {batch}")
        raise
```

### 7. Dtype Mismatch

**Error Message:**
```
RuntimeError: expected scalar type Float but found Double
RuntimeError: expected scalar type Long but found Int
```

**Causes:**
- Mixing float32 and float64
- Wrong dtype for loss functions
- NumPy default dtype conflicts

**Solutions:**
```python
# Explicitly set dtype
tensor = torch.tensor(data, dtype=torch.float32)
tensor = tensor.float()  # Convert to float32
tensor = tensor.long()   # Convert to int64

# Set default dtype globally
torch.set_default_dtype(torch.float32)

# CrossEntropyLoss expects Long targets
targets = targets.long()

# BCELoss expects Float targets
targets = targets.float()

# Convert NumPy arrays properly
numpy_array = np.array([1.0, 2.0])  # float64 by default
tensor = torch.from_numpy(numpy_array).float()  # Convert to float32
```

## Debugging Tools

### 1. Anomaly Detection

```python
# Enable for debugging (disable in production - slow)
torch.autograd.set_detect_anomaly(True)

# Use as context manager
with torch.autograd.detect_anomaly():
    output = model(input)
    loss = criterion(output, target)
    loss.backward()
```

### 2. Python Debugger

```python
# Insert breakpoint
breakpoint()  # Python 3.7+
import pdb; pdb.set_trace()  # Older Python

# In Jupyter
from IPython.core.debugger import set_trace
set_trace()

# Common pdb commands:
# n - next line
# s - step into
# c - continue
# p variable - print variable
# pp variable - pretty print
# l - list source code
# q - quit
```

### 3. Memory Profiling

```python
# GPU memory summary
print(torch.cuda.memory_summary())

# Memory snapshots
torch.cuda.memory._record_memory_history()
# ... run code ...
torch.cuda.memory._dump_snapshot("memory_snapshot.pickle")

# Profile memory allocation
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             profile_memory=True) as prof:
    model(input)
print(prof.key_averages().table(sort_by="self_cuda_memory_usage"))
```

### 4. TensorBoard Integration

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

# Log scalars
writer.add_scalar('Loss/train', loss.item(), epoch)
writer.add_scalar('Accuracy/val', accuracy, epoch)

# Log histograms of weights and gradients
for name, param in model.named_parameters():
    writer.add_histogram(f'weights/{name}', param, epoch)
    if param.grad is not None:
        writer.add_histogram(f'gradients/{name}', param.grad, epoch)

# Log model graph
writer.add_graph(model, input_tensor)

# Log images
writer.add_images('predictions', predicted_images, epoch)

writer.close()

# Launch: tensorboard --logdir=runs
```

### 5. PyTorch Profiler

```python
from torch.profiler import profile, record_function, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=True,
    with_stack=True
) as prof:
    with record_function("model_inference"):
        model(input)

# Print summary
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))

# Export for Chrome trace viewer
prof.export_chrome_trace("trace.json")

# Export for TensorBoard
prof.export_stacks("profiler_stacks.txt", "self_cuda_time_total")
```

## The Four Phases of PyTorch Debugging

### Phase 1: Reproduce and Isolate

```python
# Set seeds for reproducibility
def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

# Create minimal reproducible example
# Isolate the problematic component
# Test with synthetic data first
dummy_input = torch.randn(2, 3, 224, 224, device=device)
dummy_target = torch.randint(0, 10, (2,), device=device)

# Run single forward/backward pass
model.train()
output = model(dummy_input)
loss = criterion(output, dummy_target)
loss.backward()
```

### Phase 2: Validate Data Pipeline

```python
# Check dataset
print(f"Dataset size: {len(dataset)}")
sample = dataset[0]
print(f"Sample type: {type(sample)}")
print(f"Sample shapes: {[s.shape if hasattr(s, 'shape') else type(s) for s in sample]}")

# Check DataLoader output
batch = next(iter(dataloader))
for i, item in enumerate(batch):
    print(f"Batch item {i}: shape={item.shape}, dtype={item.dtype}, device={item.device}")

# Validate data ranges
inputs, targets = batch
print(f"Input range: [{inputs.min():.4f}, {inputs.max():.4f}]")
print(f"Input mean: {inputs.mean():.4f}, std: {inputs.std():.4f}")
print(f"Target unique values: {targets.unique()}")

# Check for data issues
assert not torch.isnan(inputs).any(), "NaN in inputs"
assert not torch.isinf(inputs).any(), "Inf in inputs"
```

### Phase 3: Validate Model Architecture

```python
# Test with tiny data to check for bugs
def overfit_single_batch(model, batch, epochs=100):
    """Model should be able to overfit a single batch."""
    model.train()
    inputs, targets = batch
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}: Loss = {loss.item():.6f}")

    # Loss should be very low if model can learn
    assert loss.item() < 0.1, "Model cannot overfit single batch!"

# Check model parameters
def inspect_model(model):
    total_params = 0
    trainable_params = 0
    for name, param in model.named_parameters():
        total_params += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
        print(f"{name}: shape={param.shape}, requires_grad={param.requires_grad}")
    print(f"\nTotal params: {total_params:,}")
    print(f"Trainable params: {trainable_params:,}")

# Verify forward pass shape transformations
def trace_shapes(model, input_shape):
    """Trace shapes through the model."""
    hooks = []
    shapes = []

    def hook(module, input, output):
        shapes.append({
            'module': module.__class__.__name__,
            'input': [i.shape for i in input if hasattr(i, 'shape')],
            'output': output.shape if hasattr(output, 'shape') else type(output)
        })

    for layer in model.modules():
        hooks.append(layer.register_forward_hook(hook))

    dummy = torch.randn(1, *input_shape)
    model(dummy)

    for h in hooks:
        h.remove()

    for s in shapes:
        print(s)
```

### Phase 4: Validate Training Loop

```python
# Comprehensive training loop debugging
def debug_training_step(model, batch, criterion, optimizer):
    model.train()
    inputs, targets = batch

    # Check inputs
    print(f"Input shape: {inputs.shape}, dtype: {inputs.dtype}")
    print(f"Target shape: {targets.shape}, dtype: {targets.dtype}")

    # Zero gradients
    optimizer.zero_grad()

    # Forward pass
    with torch.autograd.detect_anomaly():
        outputs = model(inputs)
        print(f"Output shape: {outputs.shape}")
        print(f"Output range: [{outputs.min():.4f}, {outputs.max():.4f}]")

        # Check for NaN in outputs
        if torch.isnan(outputs).any():
            print("WARNING: NaN in outputs!")

        # Compute loss
        loss = criterion(outputs, targets)
        print(f"Loss: {loss.item():.6f}")

        if torch.isnan(loss):
            print("WARNING: NaN loss!")
            return

        # Backward pass
        loss.backward()

    # Check gradients
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm().item()
            print(f"{name}: grad_norm = {grad_norm:.6f}")
            if torch.isnan(param.grad).any():
                print(f"  WARNING: NaN gradient in {name}!")

    # Optimizer step
    optimizer.step()

    return loss.item()
```

## Quick Reference Commands

### Environment and Device Checks

```python
# PyTorch version
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"cuDNN version: {torch.backends.cudnn.version()}")

# GPU information
if torch.cuda.is_available():
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"Current GPU: {torch.cuda.current_device()}")
    print(f"GPU name: {torch.cuda.get_device_name()}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

### Gradient Checking

```python
# Numerical gradient check
from torch.autograd import gradcheck

# For custom autograd functions
input = torch.randn(10, requires_grad=True, dtype=torch.double)
test = gradcheck(my_function, input, eps=1e-6, atol=1e-4)
print(f"Gradient check passed: {test}")

# For modules
def check_module_gradients(module, input_shape):
    module = module.double()
    input = torch.randn(*input_shape, requires_grad=True, dtype=torch.double)
    return gradcheck(module, input, eps=1e-6, atol=1e-4)
```

### Memory Management

```python
# Clear GPU memory
torch.cuda.empty_cache()

# Memory stats
print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"Cached: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
print(f"Max allocated: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")

# Reset peak stats
torch.cuda.reset_peak_memory_stats()

# Find memory leaks
import gc
gc.collect()
torch.cuda.empty_cache()
```

### Model Inspection

```python
# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total: {total_params:,}, Trainable: {trainable_params:,}")

# Model summary (requires torchsummary)
from torchsummary import summary
summary(model, input_size=(3, 224, 224))

# Export model to ONNX for visualization
torch.onnx.export(model, dummy_input, "model.onnx", opset_version=11)
```

### Tensor Debugging

```python
# Comprehensive tensor info
def tensor_info(t, name="tensor"):
    print(f"{name}:")
    print(f"  shape: {t.shape}")
    print(f"  dtype: {t.dtype}")
    print(f"  device: {t.device}")
    print(f"  requires_grad: {t.requires_grad}")
    print(f"  is_leaf: {t.is_leaf}")
    print(f"  grad_fn: {t.grad_fn}")
    print(f"  min: {t.min().item():.6f}")
    print(f"  max: {t.max().item():.6f}")
    print(f"  mean: {t.mean().item():.6f}")
    print(f"  std: {t.std().item():.6f}")
    print(f"  has_nan: {torch.isnan(t).any().item()}")
    print(f"  has_inf: {torch.isinf(t).any().item()}")
```

## Best Practices Summary

1. **Always use explicit device placement** - Never assume tensors are on the right device
2. **Use loss functions on logits** - CrossEntropyLoss expects raw scores, not softmax output
3. **Register modules properly** - Use nn.ModuleList/ModuleDict for parameter detection
4. **Avoid in-place operations** - They can break autograd graphs
5. **Set seeds for reproducibility** - Makes debugging deterministic
6. **Start with small data** - Test overfitting on a single batch first
7. **Use anomaly detection** - Enable during development, disable in production
8. **Monitor gradients** - Check for NaN, Inf, and exploding/vanishing gradients
9. **Profile memory** - Use memory_summary() to identify leaks
10. **Print shapes liberally** - Most bugs are shape mismatches

## Resources

- [UvA Deep Learning Notebooks - Debugging Guide](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/guide3/Debugging_PyTorch.html)
- [PyTorch Lightning Debugging Guide](https://lightning.ai/docs/pytorch/stable/debug/debugging_basic.html)
- [PyTorch Performance Tuning Guide](https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
- [TorchRL Common Errors and Solutions](https://docs.pytorch.org/rl/stable/reference/generated/knowledge_base/PRO-TIPS.html)
- [Machine Learning Mastery - Debugging PyTorch](https://machinelearningmastery.com/debugging-pytorch-machine-learning-models-a-step-by-step-guide/)
