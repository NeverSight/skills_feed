---
name: optimization
description: Implements optimization techniques for rendering, scripting, memory, physics, and networking. Use when improving game performance, reducing lag, or preparing for mobile/low-end devices.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Performance Optimization

When optimizing games, follow these patterns for better performance across all devices.

## Rendering Optimization

### Part Count Reduction
```lua
-- Combine multiple parts into unions or meshes
local function combineStaticParts(model)
    local parts = {}
    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") and part.Anchored then
            table.insert(parts, part)
        end
    end

    if #parts > 1 then
        local union = parts[1]:UnionAsync(parts, Enum.CollisionFidelity.Box)
        union.Name = model.Name .. "_Combined"
        union.Parent = model.Parent

        for _, part in ipairs(parts) do
            part:Destroy()
        end

        return union
    end
end

-- Better: Use MeshPart for complex static geometry
-- Import optimized meshes from Blender with proper LODs
```

### Level of Detail (LOD)
```lua
local LODManager = {}
local LOD_DISTANCES = {50, 100, 200}  -- Distance thresholds

function LODManager.setup(model)
    local lodLevels = {
        model:FindFirstChild("LOD0"),  -- Highest detail
        model:FindFirstChild("LOD1"),
        model:FindFirstChild("LOD2"),
        model:FindFirstChild("LOD3")   -- Lowest detail
    }

    local function updateLOD()
        local camera = workspace.CurrentCamera
        local distance = (model.PrimaryPart.Position - camera.CFrame.Position).Magnitude

        local activeLOD = 1
        for i, threshold in ipairs(LOD_DISTANCES) do
            if distance > threshold then
                activeLOD = i + 1
            end
        end

        for i, lod in ipairs(lodLevels) do
            if lod then
                lod.Visible = (i == activeLOD)
            end
        end
    end

    RunService.RenderStepped:Connect(updateLOD)
end

-- Automatic LOD using Roblox's built-in system
local function setupAutomaticLOD(meshPart)
    -- RenderFidelity controls automatic LOD
    meshPart.RenderFidelity = Enum.RenderFidelity.Automatic

    -- CollisionFidelity affects physics performance
    meshPart.CollisionFidelity = Enum.CollisionFidelity.Box  -- Simplest
end
```

### Streaming Enabled
```lua
-- Enable instance streaming for large worlds
workspace.StreamingEnabled = true
workspace.StreamingMinRadius = 64    -- Min loaded radius
workspace.StreamingTargetRadius = 256 -- Target loaded radius
workspace.StreamingIntegrityMode = Enum.StreamingIntegrityMode.Default

-- For important models that must always be loaded
local importantModel = workspace.ImportantModel
importantModel.ModelStreamingMode = Enum.ModelStreamingMode.Atomic -- Load together
-- or
importantModel.ModelStreamingMode = Enum.ModelStreamingMode.Persistent -- Always loaded
```

### Texture Optimization
```lua
-- Use appropriate texture sizes
-- Mobile: 256x256 or 512x512
-- Desktop: 512x512 or 1024x1024 max

-- Reduce unique materials
local function consolidateMaterials(model)
    local materials = {}
    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") then
            local key = tostring(part.Material) .. "_" .. tostring(part.Color)
            materials[key] = (materials[key] or 0) + 1
        end
    end
    -- Identify and consolidate similar materials
end
```

## Script Optimization

### Avoid wait() and Use task Library
```lua
-- BAD: Uses deprecated wait()
wait(1)
spawn(function() ... end)
delay(1, function() ... end)

-- GOOD: Use task library
task.wait(1)
task.spawn(function() ... end)
task.delay(1, function() ... end)

-- Even better: Use events when possible
part.Touched:Wait()  -- Yields until event fires
```

### Event Connection Management
```lua
-- BAD: Memory leak - connection never disconnected
part.Touched:Connect(function()
    -- This connection persists even after part is destroyed
end)

-- GOOD: Store and disconnect connections
local connection
connection = part.Touched:Connect(function(hit)
    if someCondition then
        connection:Disconnect()
    end
end)

-- BEST: Use Maid/Janitor pattern for cleanup
local Maid = {}
Maid.__index = Maid

function Maid.new()
    return setmetatable({_tasks = {}}, Maid)
end

function Maid:GiveTask(task)
    table.insert(self._tasks, task)
end

function Maid:Cleanup()
    for _, task in ipairs(self._tasks) do
        if typeof(task) == "RBXScriptConnection" then
            task:Disconnect()
        elseif typeof(task) == "Instance" then
            task:Destroy()
        elseif type(task) == "function" then
            task()
        end
    end
    self._tasks = {}
end
```

### Caching and Avoiding Repeated Lookups
```lua
-- BAD: Repeated FindFirstChild every frame
RunService.Heartbeat:Connect(function()
    local hrp = player.Character:FindFirstChild("HumanoidRootPart")
    local humanoid = player.Character:FindFirstChildOfClass("Humanoid")
    -- ...
end)

-- GOOD: Cache references
local character, hrp, humanoid

local function cacheCharacter()
    character = player.Character
    if character then
        hrp = character:WaitForChild("HumanoidRootPart")
        humanoid = character:WaitForChild("Humanoid")
    end
end

player.CharacterAdded:Connect(cacheCharacter)
cacheCharacter()

RunService.Heartbeat:Connect(function()
    if hrp then
        -- Use cached reference
    end
end)
```

### Table Operations
```lua
-- BAD: Creating new tables constantly
RunService.Heartbeat:Connect(function()
    local data = {x = 1, y = 2, z = 3}  -- New table every frame
end)

-- GOOD: Reuse tables
local data = {x = 0, y = 0, z = 0}
RunService.Heartbeat:Connect(function()
    data.x, data.y, data.z = 1, 2, 3
end)

-- Use table.create for known sizes
local arr = table.create(1000, 0)  -- Pre-allocate 1000 slots

-- Clear table without creating new one
local function clearTable(t)
    for k in pairs(t) do
        t[k] = nil
    end
end
```

### Local vs Global Variables
```lua
-- BAD: Accessing globals is slower
for i = 1, 1000000 do
    local x = math.sin(i)  -- Global lookup each time
end

-- GOOD: Cache in local variable
local sin = math.sin
for i = 1, 1000000 do
    local x = sin(i)  -- Local lookup is faster
end
```

## Memory Optimization

### Instance Destruction
```lua
-- Properly destroy instances to free memory
local function cleanup(instance)
    -- Disconnect all connections first
    for _, connection in ipairs(instance:GetConnections()) do
        connection:Disconnect()
    end

    -- Clear attributes
    for _, attr in ipairs(instance:GetAttributes()) do
        instance:SetAttribute(attr, nil)
    end

    instance:Destroy()
end

-- Nil references after destroy
local part = Instance.new("Part")
part:Destroy()
part = nil  -- Allow garbage collection
```

### Object Pooling
```lua
local ObjectPool = {}
ObjectPool.__index = ObjectPool

function ObjectPool.new(template, initialSize)
    local pool = setmetatable({
        template = template,
        available = {},
        active = {}
    }, ObjectPool)

    for i = 1, initialSize do
        local obj = template:Clone()
        obj.Parent = nil
        table.insert(pool.available, obj)
    end

    return pool
end

function ObjectPool:get()
    local obj = table.remove(self.available)
    if not obj then
        obj = self.template:Clone()
    end
    table.insert(self.active, obj)
    return obj
end

function ObjectPool:release(obj)
    local index = table.find(self.active, obj)
    if index then
        table.remove(self.active, index)
    end
    obj.Parent = nil  -- Remove from world
    -- Reset state...
    table.insert(self.available, obj)
end
```

### Garbage Collection Awareness
```lua
-- Avoid creating garbage in hot loops
-- BAD:
RunService.Heartbeat:Connect(function()
    local info = {  -- Creates garbage every frame
        position = hrp.Position,
        velocity = hrp.AssemblyLinearVelocity
    }
end)

-- GOOD: Use primitives or reuse tables
local cachedPosition = Vector3.new()
local cachedVelocity = Vector3.new()

RunService.Heartbeat:Connect(function()
    -- Vectors are value types, no garbage created
    local pos = hrp.Position
    local vel = hrp.AssemblyLinearVelocity
end)

-- Manual GC control (use sparingly)
local function forceGC()
    collectgarbage("collect")
end
```

## Physics Optimization

### Collision Groups
```lua
local PhysicsService = game:GetService("PhysicsService")

-- Create collision groups
PhysicsService:RegisterCollisionGroup("Players")
PhysicsService:RegisterCollisionGroup("Enemies")
PhysicsService:RegisterCollisionGroup("Projectiles")
PhysicsService:RegisterCollisionGroup("Debris")

-- Disable unnecessary collisions
PhysicsService:CollisionGroupSetCollidable("Players", "Players", false)
PhysicsService:CollisionGroupSetCollidable("Projectiles", "Projectiles", false)
PhysicsService:CollisionGroupSetCollidable("Debris", "Debris", false)

-- Assign to parts
local function setCollisionGroup(part, groupName)
    part.CollisionGroup = groupName
end
```

### Anchored Parts
```lua
-- Anchor static parts to remove from physics simulation
local function optimizeStaticParts(model)
    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") then
            local isStatic = not part:FindFirstChildOfClass("Motor6D")
                         and not part:FindFirstChildOfClass("Weld")
            if isStatic then
                part.Anchored = true
            end
        end
    end
end
```

### Simplified Collision
```lua
-- Use simpler collision shapes
meshPart.CollisionFidelity = Enum.CollisionFidelity.Box  -- Fastest
meshPart.CollisionFidelity = Enum.CollisionFidelity.Hull -- Medium
meshPart.CollisionFidelity = Enum.CollisionFidelity.Default -- Detailed

-- Disable collisions for visual-only parts
visualPart.CanCollide = false
visualPart.CanQuery = false  -- Excludes from raycasts too
visualPart.CanTouch = false  -- Excludes from Touched events
```

## Network Optimization

### Minimize RemoteEvent Traffic
```lua
-- BAD: Fire every frame
RunService.Heartbeat:Connect(function()
    PositionRemote:FireServer(hrp.Position)
end)

-- GOOD: Throttle updates
local lastUpdate = 0
local UPDATE_RATE = 1/20  -- 20 updates per second

RunService.Heartbeat:Connect(function()
    local now = os.clock()
    if now - lastUpdate >= UPDATE_RATE then
        lastUpdate = now
        PositionRemote:FireServer(hrp.Position)
    end
end)

-- BETTER: Only send when changed significantly
local lastSentPosition = Vector3.new()
local POSITION_THRESHOLD = 0.5

RunService.Heartbeat:Connect(function()
    local pos = hrp.Position
    if (pos - lastSentPosition).Magnitude > POSITION_THRESHOLD then
        lastSentPosition = pos
        PositionRemote:FireServer(pos)
    end
end)
```

### Data Compression
```lua
-- Quantize positions to reduce data size
local function quantizeVector3(v, precision)
    precision = precision or 0.1
    return Vector3.new(
        math.floor(v.X / precision) * precision,
        math.floor(v.Y / precision) * precision,
        math.floor(v.Z / precision) * precision
    )
end

-- Pack multiple values
local function packColor(color)
    return color.R * 65536 + color.G * 256 + color.B
end

local function unpackColor(packed)
    local r = math.floor(packed / 65536)
    local g = math.floor((packed % 65536) / 256)
    local b = packed % 256
    return Color3.fromRGB(r, g, b)
end
```

## Profiling Tools

### MicroProfiler
```lua
-- Use debug.profilebegin/end for custom profiling
debug.profilebegin("MyExpensiveFunction")
-- ... expensive code ...
debug.profileend()

-- View in MicroProfiler (Ctrl+F6 in Studio)
```

### Performance Stats
```lua
local Stats = game:GetService("Stats")

local function logPerformance()
    print("Memory:", Stats:GetTotalMemoryUsageMb(), "MB")
    print("Instances:", Stats.InstanceCount)
    print("Data Receive:", Stats.DataReceiveKbps, "Kbps")
    print("Data Send:", Stats.DataSendKbps, "Kbps")
    print("Physics Step:", Stats.PhysicsStepTimeMs, "ms")
end
```

### Frame Rate Monitoring
```lua
local frameCount = 0
local lastTime = os.clock()

RunService.RenderStepped:Connect(function()
    frameCount = frameCount + 1

    local now = os.clock()
    if now - lastTime >= 1 then
        local fps = frameCount / (now - lastTime)
        print("FPS:", math.floor(fps))
        frameCount = 0
        lastTime = now
    end
end)
```
