---
name: animation-system
description: Implements animation systems including custom animators, animation blending, procedural animation, and IK. Use when creating character animations, custom rigs, or procedural movement.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Animation Systems

When implementing animations, follow these patterns for smooth, performant character and object animations.

## Animation Basics

### Loading and Playing Animations
```lua
local function setupAnimations(character)
    local humanoid = character:WaitForChild("Humanoid")
    local animator = humanoid:WaitForChild("Animator")

    -- Create animation instance
    local walkAnim = Instance.new("Animation")
    walkAnim.AnimationId = "rbxassetid://123456789"

    -- Load animation track
    local walkTrack = animator:LoadAnimation(walkAnim)

    -- Configure track
    walkTrack.Priority = Enum.AnimationPriority.Movement
    walkTrack.Looped = true

    -- Play with parameters
    walkTrack:Play(
        0.1,  -- Fade in time
        1,    -- Weight (0-1)
        1     -- Speed multiplier
    )

    return walkTrack
end
```

### Animation Priorities
```lua
-- Priority order (lowest to highest):
-- Core < Idle < Movement < Action < Action2 < Action3 < Action4

local function setAnimationPriority(track, priority)
    track.Priority = priority
end

-- Example priority usage
idleTrack.Priority = Enum.AnimationPriority.Idle
walkTrack.Priority = Enum.AnimationPriority.Movement
attackTrack.Priority = Enum.AnimationPriority.Action
-- Action always overrides Movement, Movement overrides Idle
```

### Animation Events (Keyframe Markers)
```lua
-- Add markers in Animation Editor, then listen:
local function setupAnimationEvents(track)
    -- Listen for specific marker
    track:GetMarkerReachedSignal("Footstep"):Connect(function(paramValue)
        playFootstepSound()
    end)

    track:GetMarkerReachedSignal("DamageFrame"):Connect(function()
        applyDamage()
    end)

    track:GetMarkerReachedSignal("SpawnVFX"):Connect(function(vfxName)
        spawnEffect(vfxName)
    end)
end

-- Animation completion
track.Stopped:Connect(function()
    print("Animation stopped or completed")
end)

-- Check if playing
if track.IsPlaying then
    -- Animation is active
end
```

## Animation Controller

### State-Based Animation Controller
```lua
local AnimationController = {}
AnimationController.__index = AnimationController

function AnimationController.new(character)
    local self = setmetatable({}, AnimationController)

    self.character = character
    self.humanoid = character:WaitForChild("Humanoid")
    self.animator = self.humanoid:WaitForChild("Animator")
    self.tracks = {}
    self.currentState = "Idle"
    self.stateAnimations = {}

    return self
end

function AnimationController:loadAnimation(name, animationId, config)
    config = config or {}

    local animation = Instance.new("Animation")
    animation.AnimationId = animationId

    local track = self.animator:LoadAnimation(animation)
    track.Priority = config.priority or Enum.AnimationPriority.Movement
    track.Looped = config.looped or false

    self.tracks[name] = track
    return track
end

function AnimationController:setState(stateName, fadeTime)
    fadeTime = fadeTime or 0.1

    if self.currentState == stateName then return end

    -- Stop current state animation
    local currentTrack = self.tracks[self.currentState]
    if currentTrack and currentTrack.IsPlaying then
        currentTrack:Stop(fadeTime)
    end

    -- Play new state animation
    local newTrack = self.tracks[stateName]
    if newTrack then
        newTrack:Play(fadeTime)
    end

    self.currentState = stateName
end

function AnimationController:playOneShot(name, fadeTime, weight, speed)
    local track = self.tracks[name]
    if track then
        track:Play(fadeTime or 0.1, weight or 1, speed or 1)
    end
    return track
end

-- Usage
local controller = AnimationController.new(character)
controller:loadAnimation("Idle", "rbxassetid://idle", {looped = true, priority = Enum.AnimationPriority.Idle})
controller:loadAnimation("Walk", "rbxassetid://walk", {looped = true, priority = Enum.AnimationPriority.Movement})
controller:loadAnimation("Attack", "rbxassetid://attack", {priority = Enum.AnimationPriority.Action})

controller:setState("Idle")
-- When moving:
controller:setState("Walk")
-- Attack (plays on top):
controller:playOneShot("Attack")
```

### Movement-Based Animation Selection
```lua
local function setupMovementAnimations(character)
    local humanoid = character:WaitForChild("Humanoid")
    local animator = humanoid:WaitForChild("Animator")
    local hrp = character:WaitForChild("HumanoidRootPart")

    local animations = {
        idle = loadAnimation(animator, "rbxassetid://idle"),
        walk = loadAnimation(animator, "rbxassetid://walk"),
        run = loadAnimation(animator, "rbxassetid://run"),
        jump = loadAnimation(animator, "rbxassetid://jump"),
        fall = loadAnimation(animator, "rbxassetid://fall")
    }

    -- Set looping
    animations.idle.Looped = true
    animations.walk.Looped = true
    animations.run.Looped = true
    animations.fall.Looped = true

    local currentAnim = nil

    local function updateAnimation()
        local velocity = hrp.AssemblyLinearVelocity
        local horizontalSpeed = Vector3.new(velocity.X, 0, velocity.Z).Magnitude
        local isGrounded = humanoid.FloorMaterial ~= Enum.Material.Air

        local targetAnim

        if not isGrounded then
            if velocity.Y > 1 then
                targetAnim = animations.jump
            else
                targetAnim = animations.fall
            end
        elseif horizontalSpeed < 0.5 then
            targetAnim = animations.idle
        elseif horizontalSpeed < 12 then
            targetAnim = animations.walk
            -- Adjust speed based on movement
            animations.walk:AdjustSpeed(horizontalSpeed / 8)
        else
            targetAnim = animations.run
            animations.run:AdjustSpeed(horizontalSpeed / 16)
        end

        if targetAnim ~= currentAnim then
            if currentAnim then
                currentAnim:Stop(0.2)
            end
            targetAnim:Play(0.2)
            currentAnim = targetAnim
        end
    end

    RunService.Heartbeat:Connect(updateAnimation)
end
```

## Animation Blending

### Weight-Based Blending
```lua
local BlendedAnimator = {}

function BlendedAnimator.new(animator)
    return {
        animator = animator,
        layers = {}
    }
end

function BlendedAnimator:addLayer(name, animationId, priority)
    local animation = Instance.new("Animation")
    animation.AnimationId = animationId

    local track = self.animator:LoadAnimation(animation)
    track.Priority = priority or Enum.AnimationPriority.Movement
    track.Looped = true

    self.layers[name] = {
        track = track,
        weight = 0,
        targetWeight = 0
    }

    track:Play(0, 0)  -- Start at weight 0
    return track
end

function BlendedAnimator:setLayerWeight(name, weight, blendTime)
    local layer = self.layers[name]
    if not layer then return end

    layer.targetWeight = math.clamp(weight, 0, 1)

    if blendTime and blendTime > 0 then
        -- Smooth blend
        local startWeight = layer.weight
        local startTime = os.clock()

        local conn
        conn = RunService.Heartbeat:Connect(function()
            local elapsed = os.clock() - startTime
            local t = math.min(elapsed / blendTime, 1)

            layer.weight = startWeight + (layer.targetWeight - startWeight) * t
            layer.track:AdjustWeight(layer.weight)

            if t >= 1 then
                conn:Disconnect()
            end
        end)
    else
        layer.weight = layer.targetWeight
        layer.track:AdjustWeight(layer.weight)
    end
end

-- Usage: Blend between walk and limp
local blender = BlendedAnimator.new(animator)
blender:addLayer("Walk", "rbxassetid://walk", Enum.AnimationPriority.Movement)
blender:addLayer("Limp", "rbxassetid://limp", Enum.AnimationPriority.Movement)

-- Normal walking
blender:setLayerWeight("Walk", 1, 0.3)
blender:setLayerWeight("Limp", 0, 0.3)

-- Injured (blend to limp)
blender:setLayerWeight("Walk", 0.3, 0.5)
blender:setLayerWeight("Limp", 0.7, 0.5)
```

### Additive Animation Blending
```lua
-- Additive animations add on top of base animation
local function setupAdditiveBlending(animator)
    local baseWalk = loadAnimation(animator, "rbxassetid://walk")
    local leanLeft = loadAnimation(animator, "rbxassetid://lean_left")
    local leanRight = loadAnimation(animator, "rbxassetid://lean_right")

    baseWalk.Looped = true
    leanLeft.Looped = true
    leanRight.Looped = true

    baseWalk:Play()
    leanLeft:Play(0, 0)  -- Start at 0 weight
    leanRight:Play(0, 0)

    -- Update lean based on input
    local function updateLean(turnAmount)
        -- turnAmount: -1 (left) to 1 (right)
        if turnAmount < 0 then
            leanLeft:AdjustWeight(math.abs(turnAmount))
            leanRight:AdjustWeight(0)
        else
            leanLeft:AdjustWeight(0)
            leanRight:AdjustWeight(turnAmount)
        end
    end

    return updateLean
end
```

## Procedural Animation

### Procedural Head Look
```lua
local function setupHeadLook(character, target)
    local neck = character:FindFirstChild("Neck", true)
    if not neck then return end

    local originalC0 = neck.C0

    RunService.RenderStepped:Connect(function()
        if not target then
            neck.C0 = originalC0
            return
        end

        local headPos = neck.Part1.Position
        local targetPos = target.Position
        local direction = (targetPos - headPos).Unit

        -- Convert to local space
        local torsoLook = neck.Part0.CFrame.LookVector
        local torsoCFrame = neck.Part0.CFrame

        local localDirection = torsoCFrame:VectorToObjectSpace(direction)

        -- Calculate angles
        local yaw = math.atan2(localDirection.X, -localDirection.Z)
        local pitch = math.asin(localDirection.Y)

        -- Clamp to prevent unnatural rotation
        yaw = math.clamp(yaw, math.rad(-70), math.rad(70))
        pitch = math.clamp(pitch, math.rad(-40), math.rad(40))

        -- Apply rotation
        local lookCFrame = CFrame.Angles(pitch, yaw, 0)
        neck.C0 = originalC0 * lookCFrame
    end)
end
```

### Procedural Breathing
```lua
local function setupBreathing(character)
    local torso = character:FindFirstChild("UpperTorso") or character:FindFirstChild("Torso")
    if not torso then return end

    local waist = character:FindFirstChild("Waist", true)
    if not waist then return end

    local originalC0 = waist.C0
    local breathSpeed = 2  -- Cycles per second
    local breathIntensity = 0.02

    local time = 0

    RunService.RenderStepped:Connect(function(dt)
        time = time + dt

        local breathOffset = math.sin(time * breathSpeed * math.pi * 2) * breathIntensity

        waist.C0 = originalC0 * CFrame.new(0, breathOffset, 0)
    end)
end
```

### Procedural Tail/Cape Physics
```lua
local function setupProceduralChain(parts, config)
    config = config or {}
    local stiffness = config.stiffness or 0.5
    local damping = config.damping or 0.3
    local gravity = config.gravity or Vector3.new(0, -10, 0)

    local velocities = {}
    local restOffsets = {}

    -- Store rest positions
    for i, part in ipairs(parts) do
        velocities[i] = Vector3.new()
        if i > 1 then
            restOffsets[i] = parts[i-1].CFrame:ToObjectSpace(part.CFrame)
        end
    end

    RunService.Heartbeat:Connect(function(dt)
        for i = 2, #parts do
            local part = parts[i]
            local parent = parts[i-1]

            -- Target position (relative to parent)
            local targetCFrame = parent.CFrame * restOffsets[i]
            local targetPos = targetCFrame.Position

            -- Current position
            local currentPos = part.Position

            -- Spring force toward target
            local displacement = targetPos - currentPos
            local springForce = displacement * stiffness

            -- Apply gravity
            local totalForce = springForce + gravity

            -- Update velocity with damping
            velocities[i] = velocities[i] * (1 - damping) + totalForce * dt

            -- Update position
            local newPos = currentPos + velocities[i]

            -- Maintain distance constraint
            local toParent = parent.Position - newPos
            local distance = toParent.Magnitude
            local restDistance = restOffsets[i].Position.Magnitude

            if distance > restDistance then
                newPos = parent.Position - toParent.Unit * restDistance
            end

            -- Apply
            part.CFrame = CFrame.new(newPos) * (targetCFrame - targetCFrame.Position)
        end
    end)
end
```

## Inverse Kinematics (IK)

### Two-Bone IK (Arms/Legs)
```lua
local function solveTwoBoneIK(upperBone, lowerBone, target, pole)
    local upperLength = (lowerBone.Position - upperBone.Position).Magnitude
    local lowerLength = (target - lowerBone.Position).Magnitude

    local origin = upperBone.Position
    local targetPos = target
    local polePos = pole or (origin + Vector3.new(0, 0, 1))

    -- Calculate distance to target
    local targetDistance = (targetPos - origin).Magnitude
    local totalLength = upperLength + lowerLength

    -- Clamp target to reachable distance
    if targetDistance > totalLength * 0.999 then
        targetDistance = totalLength * 0.999
    end

    -- Law of cosines to find angles
    local a = upperLength
    local b = lowerLength
    local c = targetDistance

    -- Angle at upper joint
    local upperAngle = math.acos(
        math.clamp((a*a + c*c - b*b) / (2*a*c), -1, 1)
    )

    -- Angle at lower joint (elbow/knee)
    local lowerAngle = math.acos(
        math.clamp((a*a + b*b - c*c) / (2*a*b), -1, 1)
    )

    -- Direction to target
    local directionToTarget = (targetPos - origin).Unit

    -- Calculate pole plane
    local poleDirection = (polePos - origin).Unit
    local cross = directionToTarget:Cross(poleDirection)
    local normal = cross:Cross(directionToTarget).Unit

    -- Apply rotations
    local upperRotation = CFrame.fromAxisAngle(cross, -upperAngle)
    local elbowPosition = origin + upperRotation:VectorToWorldSpace(directionToTarget) * upperLength

    return elbowPosition, lowerAngle
end

-- Foot IK for terrain
local function setupFootIK(character)
    local humanoid = character:WaitForChild("Humanoid")
    local hrp = character:WaitForChild("HumanoidRootPart")

    local leftFoot = character:FindFirstChild("LeftFoot")
    local rightFoot = character:FindFirstChild("RightFoot")
    local leftLeg = character:FindFirstChild("LeftLowerLeg")
    local rightLeg = character:FindFirstChild("RightLowerLeg")

    local rayParams = RaycastParams.new()
    rayParams.FilterDescendantsInstances = {character}

    RunService.RenderStepped:Connect(function()
        if humanoid.FloorMaterial == Enum.Material.Air then return end

        -- Raycast for each foot
        for _, footData in ipairs({{leftFoot, leftLeg}, {rightFoot, rightLeg}}) do
            local foot, lowerLeg = footData[1], footData[2]

            local result = workspace:Raycast(
                foot.Position + Vector3.new(0, 1, 0),
                Vector3.new(0, -2, 0),
                rayParams
            )

            if result then
                local targetY = result.Position.Y
                local offset = targetY - foot.Position.Y + 0.1

                -- Apply IK offset (simplified)
                -- In practice, you'd solve the full IK chain
            end
        end
    end)
end
```

## Custom Rigs

### Motor6D Setup for Custom Rigs
```lua
local function createCustomRig(model)
    local root = model.PrimaryPart
    local parts = {}

    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") and part ~= root then
            table.insert(parts, part)
        end
    end

    -- Create Motor6Ds
    local motors = {}

    for _, part in ipairs(parts) do
        local motor = Instance.new("Motor6D")
        motor.Name = part.Name

        -- Find parent part (closest connected part toward root)
        local parentPart = findParentPart(part, root, parts)

        motor.Part0 = parentPart
        motor.Part1 = part

        -- Calculate C0 and C1 (joint positions)
        local jointPos = (parentPart.Position + part.Position) / 2
        motor.C0 = parentPart.CFrame:ToObjectSpace(CFrame.new(jointPos))
        motor.C1 = part.CFrame:ToObjectSpace(CFrame.new(jointPos))

        motor.Parent = parentPart
        motors[part.Name] = motor
    end

    return motors
end

-- Animate custom rig
local function animateCustomRig(motors, animationData)
    -- animationData: {motorName = {CFrame sequence}}

    local time = 0
    local duration = animationData.duration or 1

    RunService.RenderStepped:Connect(function(dt)
        time = (time + dt) % duration
        local t = time / duration

        for motorName, keyframes in pairs(animationData.motors or {}) do
            local motor = motors[motorName]
            if motor then
                -- Interpolate between keyframes
                local transform = interpolateKeyframes(keyframes, t)
                motor.Transform = transform
            end
        end
    end)
end
```

### Humanoid Description for NPCs
```lua
local function applyHumanoidDescription(character, description)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    -- Create or modify description
    local desc = description or Instance.new("HumanoidDescription")

    -- Body parts
    desc.Head = 123456789  -- Asset ID
    desc.Torso = 123456789
    desc.LeftArm = 123456789
    desc.RightArm = 123456789
    desc.LeftLeg = 123456789
    desc.RightLeg = 123456789

    -- Animations
    desc.IdleAnimation = 123456789
    desc.WalkAnimation = 123456789
    desc.RunAnimation = 123456789
    desc.JumpAnimation = 123456789
    desc.FallAnimation = 123456789

    -- Body scales
    desc.HeadScale = 1
    desc.BodyTypeScale = 0.5
    desc.ProportionScale = 1
    desc.WidthScale = 1
    desc.HeightScale = 1
    desc.DepthScale = 1

    humanoid:ApplyDescription(desc)
end
```

## Animation Performance

### Animation Caching
```lua
local AnimationCache = {}
AnimationCache.cache = {}

function AnimationCache.load(animator, animationId)
    local cacheKey = tostring(animator) .. "_" .. animationId

    if AnimationCache.cache[cacheKey] then
        return AnimationCache.cache[cacheKey]
    end

    local animation = Instance.new("Animation")
    animation.AnimationId = animationId

    local track = animator:LoadAnimation(animation)
    AnimationCache.cache[cacheKey] = track

    return track
end

function AnimationCache.clear(animator)
    local prefix = tostring(animator) .. "_"

    for key, track in pairs(AnimationCache.cache) do
        if string.sub(key, 1, #prefix) == prefix then
            track:Stop()
            track:Destroy()
            AnimationCache.cache[key] = nil
        end
    end
end
```

### LOD for Animations
```lua
local AnimationLOD = {}

function AnimationLOD.setup(character, camera)
    local animator = character:WaitForChild("Humanoid"):WaitForChild("Animator")
    local hrp = character:WaitForChild("HumanoidRootPart")

    local LOD_DISTANCES = {50, 100, 200}
    local UPDATE_RATES = {1, 0.5, 0.25, 0.1}  -- Animation update rate

    local lastUpdate = 0
    local currentLOD = 1

    RunService.Heartbeat:Connect(function()
        local distance = (hrp.Position - camera.CFrame.Position).Magnitude

        -- Determine LOD level
        local lodLevel = 1
        for i, threshold in ipairs(LOD_DISTANCES) do
            if distance > threshold then
                lodLevel = i + 1
            end
        end

        -- Update animation rate based on LOD
        if lodLevel ~= currentLOD then
            currentLOD = lodLevel

            -- Adjust all playing animations
            for _, track in ipairs(animator:GetPlayingAnimationTracks()) do
                -- Distant characters: slower animation updates
                -- This is a simplified approach; Roblox handles this internally
            end
        end
    end)
end
```

### Pooled Animation Tracks
```lua
local TrackPool = {}
TrackPool.pools = {}

function TrackPool.getTrack(animator, animationId)
    local poolKey = animationId

    if not TrackPool.pools[poolKey] then
        TrackPool.pools[poolKey] = {
            available = {},
            inUse = {}
        }
    end

    local pool = TrackPool.pools[poolKey]

    -- Check for available track
    local track = table.remove(pool.available)

    if not track then
        -- Create new track
        local animation = Instance.new("Animation")
        animation.AnimationId = animationId
        track = animator:LoadAnimation(animation)
    end

    table.insert(pool.inUse, track)
    return track
end

function TrackPool.releaseTrack(animationId, track)
    local pool = TrackPool.pools[animationId]
    if not pool then return end

    track:Stop(0)

    local index = table.find(pool.inUse, track)
    if index then
        table.remove(pool.inUse, index)
    end

    table.insert(pool.available, track)
end
```

## Animation Tools

### Animation Recording
```lua
local AnimationRecorder = {}

function AnimationRecorder.record(character, duration)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    local motors = {}

    -- Find all Motor6Ds
    for _, motor in ipairs(character:GetDescendants()) do
        if motor:IsA("Motor6D") then
            table.insert(motors, motor)
        end
    end

    local keyframes = {}
    local startTime = os.clock()
    local recording = true

    -- Record at 30 fps
    local frameTime = 1/30
    local lastFrame = 0

    local conn
    conn = RunService.Heartbeat:Connect(function()
        local elapsed = os.clock() - startTime

        if elapsed >= duration then
            recording = false
            conn:Disconnect()
            return
        end

        if elapsed - lastFrame >= frameTime then
            lastFrame = elapsed

            local frame = {
                time = elapsed,
                poses = {}
            }

            for _, motor in ipairs(motors) do
                frame.poses[motor.Name] = {
                    C0 = motor.C0,
                    C1 = motor.C1,
                    Transform = motor.Transform
                }
            end

            table.insert(keyframes, frame)
        end
    end)

    -- Return promise-like
    return {
        getKeyframes = function()
            while recording do
                task.wait()
            end
            return keyframes
        end
    }
end
```

### Animation Playback from Data
```lua
local function playRecordedAnimation(character, keyframes)
    local motors = {}

    for _, motor in ipairs(character:GetDescendants()) do
        if motor:IsA("Motor6D") then
            motors[motor.Name] = motor
        end
    end

    local duration = keyframes[#keyframes].time
    local startTime = os.clock()

    local conn
    conn = RunService.Heartbeat:Connect(function()
        local elapsed = os.clock() - startTime

        if elapsed >= duration then
            conn:Disconnect()
            return
        end

        -- Find surrounding keyframes
        local prevFrame, nextFrame
        for i, frame in ipairs(keyframes) do
            if frame.time <= elapsed then
                prevFrame = frame
                nextFrame = keyframes[i + 1]
            end
        end

        if not prevFrame or not nextFrame then return end

        -- Interpolate
        local t = (elapsed - prevFrame.time) / (nextFrame.time - prevFrame.time)

        for motorName, motor in pairs(motors) do
            local prevPose = prevFrame.poses[motorName]
            local nextPose = nextFrame.poses[motorName]

            if prevPose and nextPose then
                motor.Transform = prevPose.Transform:Lerp(nextPose.Transform, t)
            end
        end
    end)

    return conn
end
```
