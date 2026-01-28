---
name: vfx-effects
description: Implements visual effects including particle systems, camera effects, lighting, mesh effects, and UI animations. Use when creating combat VFX, environmental effects, feedback systems, or any visual polish.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Visual Effects (VFX)

When implementing VFX, use these patterns for impactful and performant effects.

## Particle Effects

### Anime Hit VFX
```lua
local function createHitEffect(position, direction, intensity)
    intensity = intensity or 1

    -- Impact flash
    local flash = Instance.new("Part")
    flash.Shape = Enum.PartType.Ball
    flash.Size = Vector3.new(0.1, 0.1, 0.1)
    flash.Position = position
    flash.Anchored = true
    flash.CanCollide = false
    flash.Material = Enum.Material.Neon
    flash.Color = Color3.new(1, 1, 1)
    flash.Parent = workspace.Effects

    -- Scale up and fade
    local tweenInfo = TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    TweenService:Create(flash, tweenInfo, {
        Size = Vector3.new(3, 3, 3) * intensity,
        Transparency = 1
    }):Play()

    -- Radial lines (speedlines)
    local numLines = 8
    for i = 1, numLines do
        local angle = (i / numLines) * math.pi * 2
        local lineDir = Vector3.new(math.cos(angle), 0, math.sin(angle))

        local line = Instance.new("Part")
        line.Size = Vector3.new(0.1, 0.1, 2)
        line.CFrame = CFrame.lookAt(position, position + lineDir) * CFrame.new(0, 0, -1)
        line.Anchored = true
        line.CanCollide = false
        line.Material = Enum.Material.Neon
        line.Color = Color3.new(1, 0.9, 0.8)
        line.Parent = workspace.Effects

        TweenService:Create(line, TweenInfo.new(0.2), {
            Size = Vector3.new(0.05, 0.05, 5) * intensity,
            CFrame = line.CFrame * CFrame.new(0, 0, -3),
            Transparency = 1
        }):Play()

        Debris:AddItem(line, 0.3)
    end

    -- Screen shake
    shakeCamera(0.3, intensity * 5)

    Debris:AddItem(flash, 0.2)
end
```

### Slash Trail
```lua
local function createSlashTrail(weapon, duration)
    local attachment0 = weapon:FindFirstChild("TrailAttachment0")
    local attachment1 = weapon:FindFirstChild("TrailAttachment1")

    if not attachment0 or not attachment1 then
        -- Create attachments at blade ends
        attachment0 = Instance.new("Attachment")
        attachment0.Name = "TrailAttachment0"
        attachment0.Position = Vector3.new(0, 0, 2)  -- Tip
        attachment0.Parent = weapon

        attachment1 = Instance.new("Attachment")
        attachment1.Name = "TrailAttachment1"
        attachment1.Position = Vector3.new(0, 0, 0)  -- Base
        attachment1.Parent = weapon
    end

    local trail = Instance.new("Trail")
    trail.Attachment0 = attachment0
    trail.Attachment1 = attachment1
    trail.Lifetime = 0.3
    trail.MinLength = 0
    trail.FaceCamera = true
    trail.Color = ColorSequence.new({
        ColorSequenceKeypoint.new(0, Color3.new(1, 1, 1)),
        ColorSequenceKeypoint.new(1, Color3.new(0.8, 0.8, 1))
    })
    trail.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.5, 0.3),
        NumberSequenceKeypoint.new(1, 1)
    })
    trail.WidthScale = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 1),
        NumberSequenceKeypoint.new(1, 0.2)
    })
    trail.Parent = weapon

    -- Disable after duration
    task.delay(duration, function()
        trail.Enabled = false
        Debris:AddItem(trail, trail.Lifetime)
    end)

    return trail
end
```

### Aura Effect
```lua
local function createAura(character, color, intensity)
    local hrp = character:FindFirstChild("HumanoidRootPart")
    if not hrp then return end

    local attachment = Instance.new("Attachment")
    attachment.Parent = hrp

    local particles = Instance.new("ParticleEmitter")
    particles.Color = ColorSequence.new(color)
    particles.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(0.5, 1),
        NumberSequenceKeypoint.new(1, 0)
    })
    particles.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(1, 1)
    })
    particles.Lifetime = NumberRange.new(0.5, 1)
    particles.Rate = 50 * intensity
    particles.Speed = NumberRange.new(2, 4)
    particles.SpreadAngle = Vector2.new(180, 180)
    particles.Acceleration = Vector3.new(0, 5, 0)
    particles.EmissionDirection = Enum.NormalId.Top
    particles.Parent = attachment

    -- Point light for glow
    local light = Instance.new("PointLight")
    light.Color = color
    light.Brightness = intensity
    light.Range = 10
    light.Parent = hrp

    return {
        stop = function()
            particles.Enabled = false
            TweenService:Create(light, TweenInfo.new(0.5), {Brightness = 0}):Play()
            Debris:AddItem(attachment, 1)
            Debris:AddItem(light, 0.5)
        end
    }
end
```

## Camera Effects

### Screen Shake
```lua
local ShakeModule = {}
local currentShake = Vector3.new()

function ShakeModule.shake(duration, magnitude, frequency)
    frequency = frequency or 20

    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        if elapsed > duration then
            currentShake = Vector3.new()
            conn:Disconnect()
            return
        end

        -- Decay over time
        local decay = 1 - (elapsed / duration)
        local shake = magnitude * decay

        -- Random offset
        currentShake = Vector3.new(
            (math.random() - 0.5) * 2 * shake,
            (math.random() - 0.5) * 2 * shake,
            0
        )
    end)
end

function ShakeModule.getOffset()
    return currentShake
end

-- Apply in camera update
RunService.RenderStepped:Connect(function()
    local offset = ShakeModule.getOffset()
    camera.CFrame = camera.CFrame * CFrame.new(offset)
end)
```

### Hit Stop (Frame Freeze)
```lua
local function hitStop(duration)
    duration = duration or 0.05

    -- Store original time scale
    local originalSpeed = 1

    -- Slow down animations
    for _, player in ipairs(Players:GetPlayers()) do
        local character = player.Character
        if character then
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                local animator = humanoid:FindFirstChildOfClass("Animator")
                if animator then
                    for _, track in ipairs(animator:GetPlayingAnimationTracks()) do
                        track:AdjustSpeed(0.01)
                    end
                end
            end
        end
    end

    task.wait(duration)

    -- Restore
    for _, player in ipairs(Players:GetPlayers()) do
        local character = player.Character
        if character then
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                local animator = humanoid:FindFirstChildOfClass("Animator")
                if animator then
                    for _, track in ipairs(animator:GetPlayingAnimationTracks()) do
                        track:AdjustSpeed(1)
                    end
                end
            end
        end
    end
end
```

### Zoom Punch Effect
```lua
local function zoomPunch(intensity, duration)
    intensity = intensity or 5
    duration = duration or 0.1

    local camera = workspace.CurrentCamera
    local originalFOV = camera.FieldOfView

    -- Quick zoom in
    TweenService:Create(camera, TweenInfo.new(duration * 0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
        FieldOfView = originalFOV - intensity
    }):Play()

    task.wait(duration * 0.3)

    -- Slower return
    TweenService:Create(camera, TweenInfo.new(duration * 0.7, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
        FieldOfView = originalFOV
    }):Play()
end
```

## Lighting Effects

### Dynamic Muzzle Flash
```lua
local function muzzleFlash(attachment)
    -- Light
    local light = Instance.new("PointLight")
    light.Color = Color3.new(1, 0.9, 0.5)
    light.Brightness = 5
    light.Range = 15
    light.Parent = attachment

    -- Flash particle
    local flash = Instance.new("ParticleEmitter")
    flash.Texture = "rbxassetid://123456789"  -- Muzzle flash texture
    flash.Size = NumberSequence.new(1.5)
    flash.Lifetime = NumberRange.new(0.05)
    flash.Rate = 0
    flash.Speed = NumberRange.new(0)
    flash.Parent = attachment

    flash:Emit(1)

    -- Fade light
    TweenService:Create(light, TweenInfo.new(0.1), {Brightness = 0}):Play()

    Debris:AddItem(light, 0.15)
    Debris:AddItem(flash, 0.1)
end
```

### Lightning Flash
```lua
local function lightningFlash()
    local lighting = game:GetService("Lighting")
    local originalAmbient = lighting.Ambient

    -- Flash white
    lighting.Ambient = Color3.new(1, 1, 1)

    task.wait(0.05)
    lighting.Ambient = originalAmbient
    task.wait(0.1)
    lighting.Ambient = Color3.new(0.8, 0.8, 0.8)
    task.wait(0.05)
    lighting.Ambient = originalAmbient
end
```

## Mesh & Material Effects

### Dissolve Effect
```lua
local function dissolve(part, duration)
    -- Create a dissolve texture
    local surfaceGui = Instance.new("SurfaceGui")
    surfaceGui.Face = Enum.NormalId.Front
    surfaceGui.LightInfluence = 0

    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, 0, 1, 0)
    frame.BackgroundTransparency = 1
    frame.Parent = surfaceGui

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = 90
    gradient.Parent = frame

    surfaceGui.Parent = part

    -- Animate gradient offset
    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / duration

        if t >= 1 then
            part:Destroy()
            conn:Disconnect()
            return
        end

        gradient.Offset = Vector2.new(0, t * 2 - 1)
        part.Transparency = t
    end)
end
```

### Outline Effect
```lua
local function addOutline(character, color, thickness)
    thickness = thickness or 0.05

    for _, part in ipairs(character:GetDescendants()) do
        if part:IsA("BasePart") and part.Name ~= "HumanoidRootPart" then
            local outline = part:Clone()
            outline.Name = "Outline"
            outline.Size = part.Size + Vector3.new(thickness, thickness, thickness)
            outline.Material = Enum.Material.SmoothPlastic
            outline.Color = color
            outline.CanCollide = false
            outline.Massless = true
            outline.Transparency = 0

            local weld = Instance.new("WeldConstraint")
            weld.Part0 = part
            weld.Part1 = outline
            weld.Parent = outline

            outline.Parent = part
        end
    end
end
```

## UI Visual Effects

### Damage Numbers
```lua
local function showDamageNumber(position, damage, isCrit)
    local billboardGui = Instance.new("BillboardGui")
    billboardGui.Size = UDim2.new(0, 100, 0, 50)
    billboardGui.StudsOffset = Vector3.new(0, 2, 0)
    billboardGui.Adornee = nil
    billboardGui.AlwaysOnTop = true

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, 0, 1, 0)
    label.BackgroundTransparency = 1
    label.Text = tostring(math.floor(damage))
    label.TextColor3 = isCrit and Color3.new(1, 0.8, 0) or Color3.new(1, 1, 1)
    label.TextStrokeTransparency = 0
    label.TextStrokeColor3 = Color3.new(0, 0, 0)
    label.TextScaled = true
    label.Font = Enum.Font.GothamBold
    label.Parent = billboardGui

    -- Position in world
    local part = Instance.new("Part")
    part.Anchored = true
    part.CanCollide = false
    part.Transparency = 1
    part.Size = Vector3.new(0.1, 0.1, 0.1)
    part.Position = position
    part.Parent = workspace.Effects

    billboardGui.Adornee = part
    billboardGui.Parent = part

    -- Animate: rise and fade
    local startY = position.Y
    local startTime = os.clock()

    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / 1

        if t >= 1 then
            part:Destroy()
            conn:Disconnect()
            return
        end

        -- Rise with easing
        local easeT = 1 - (1 - t) ^ 2
        part.Position = Vector3.new(position.X, startY + easeT * 3, position.Z)

        -- Fade out
        label.TextTransparency = t
        label.TextStrokeTransparency = t

        -- Scale pop for crits
        if isCrit and t < 0.2 then
            local scale = 1 + math.sin(t * 5 * math.pi) * 0.3
            label.TextSize = 24 * scale
        end
    end)
end
```

### Cooldown Sweep
```lua
local function createCooldownUI(button, cooldownDuration)
    local overlay = Instance.new("Frame")
    overlay.Name = "CooldownOverlay"
    overlay.Size = UDim2.new(1, 0, 1, 0)
    overlay.BackgroundColor3 = Color3.new(0, 0, 0)
    overlay.BackgroundTransparency = 0.5
    overlay.Parent = button

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = -90
    gradient.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.5, 0),
        NumberSequenceKeypoint.new(0.501, 1),
        NumberSequenceKeypoint.new(1, 1)
    })
    gradient.Parent = overlay

    -- Animate
    local startTime = os.clock()
    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local t = elapsed / cooldownDuration

        if t >= 1 then
            overlay:Destroy()
            conn:Disconnect()
            return
        end

        -- Rotate gradient to create sweep effect
        gradient.Rotation = -90 + (t * 360)
    end)
end
```

## Advanced VFX

### Beam Weapon
```lua
local function createBeam(startAttachment, endPosition, duration)
    local endPart = Instance.new("Part")
    endPart.Anchored = true
    endPart.CanCollide = false
    endPart.Transparency = 1
    endPart.Size = Vector3.new(0.1, 0.1, 0.1)
    endPart.Position = endPosition
    endPart.Parent = workspace.Effects

    local endAttachment = Instance.new("Attachment")
    endAttachment.Parent = endPart

    local beam = Instance.new("Beam")
    beam.Attachment0 = startAttachment
    beam.Attachment1 = endAttachment
    beam.Width0 = 0.5
    beam.Width1 = 0.3
    beam.FaceCamera = true
    beam.Color = ColorSequence.new(Color3.new(1, 0, 0))
    beam.Transparency = NumberSequence.new(0)
    beam.LightEmission = 1
    beam.LightInfluence = 0
    beam.TextureSpeed = 5
    beam.Parent = startAttachment

    -- Fade out
    task.delay(duration * 0.7, function()
        TweenService:Create(beam, TweenInfo.new(duration * 0.3), {
            Transparency = NumberSequence.new(1)
        }):Play()
    end)

    Debris:AddItem(endPart, duration)
    Debris:AddItem(beam, duration)

    return beam
end
```

### Lightning Chain
```lua
local function createLightningChain(startPos, endPos, segments)
    segments = segments or 8

    local parts = {}
    local direction = endPos - startPos
    local segmentLength = direction.Magnitude / segments

    for i = 1, segments do
        local t1 = (i - 1) / segments
        local t2 = i / segments

        local p1 = startPos + direction * t1
        local p2 = startPos + direction * t2

        -- Add random offset (except for endpoints)
        if i > 1 then
            local jitter = segmentLength * 0.5
            p1 = p1 + Vector3.new(
                (math.random() - 0.5) * jitter,
                (math.random() - 0.5) * jitter,
                (math.random() - 0.5) * jitter
            )
        end

        local segment = Instance.new("Part")
        segment.Anchored = true
        segment.CanCollide = false
        segment.Material = Enum.Material.Neon
        segment.Color = Color3.new(0.7, 0.8, 1)

        local dist = (p2 - p1).Magnitude
        segment.Size = Vector3.new(0.1, 0.1, dist)
        segment.CFrame = CFrame.lookAt((p1 + p2) / 2, p2)
        segment.Parent = workspace.Effects

        table.insert(parts, segment)
    end

    -- Quick flash and fade
    task.delay(0.05, function()
        for _, part in ipairs(parts) do
            TweenService:Create(part, TweenInfo.new(0.1), {Transparency = 1}):Play()
        end
    end)

    task.delay(0.15, function()
        for _, part in ipairs(parts) do
            part:Destroy()
        end
    end)
end
```
