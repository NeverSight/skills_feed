---
name: ui-ux
description: Implements UI/UX systems including responsive design, animations, input handling, HUD elements, and menu systems. Use when building game interfaces, menus, HUDs, or any user-facing UI.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox UI/UX Systems

When implementing UI systems, follow these patterns for responsive and polished interfaces.

## Responsive Design

### UIAspectRatioConstraint
```lua
-- Maintain aspect ratio regardless of screen size
local frame = Instance.new("Frame")
frame.Size = UDim2.new(0.5, 0, 0.5, 0)  -- Will be adjusted

local aspectRatio = Instance.new("UIAspectRatioConstraint")
aspectRatio.AspectRatio = 16/9
aspectRatio.AspectType = Enum.AspectType.FitWithinMaxSize
aspectRatio.DominantAxis = Enum.DominantAxis.Width
aspectRatio.Parent = frame
```

### UISizeConstraint
```lua
-- Limit min/max size
local sizeConstraint = Instance.new("UISizeConstraint")
sizeConstraint.MinSize = Vector2.new(100, 50)
sizeConstraint.MaxSize = Vector2.new(500, 300)
sizeConstraint.Parent = frame
```

### Screen Size Detection
```lua
local camera = workspace.CurrentCamera

local function getScreenCategory()
    local viewportSize = camera.ViewportSize

    if viewportSize.X < 600 then
        return "mobile"
    elseif viewportSize.X < 1200 then
        return "tablet"
    else
        return "desktop"
    end
end

local function updateLayout()
    local category = getScreenCategory()

    if category == "mobile" then
        mainFrame.Size = UDim2.new(0.95, 0, 0.9, 0)
        fontSize = 14
    elseif category == "tablet" then
        mainFrame.Size = UDim2.new(0.8, 0, 0.8, 0)
        fontSize = 16
    else
        mainFrame.Size = UDim2.new(0.6, 0, 0.7, 0)
        fontSize = 18
    end
end

camera:GetPropertyChangedSignal("ViewportSize"):Connect(updateLayout)
```

### Safe Area (Notch/Button Handling)
```lua
local GuiService = game:GetService("GuiService")

local function getSafeInsets()
    local insets = GuiService:GetGuiInset()
    return insets
end

-- Apply safe area padding
local topInset = getSafeInsets()
mainFrame.Position = UDim2.new(0.5, 0, 0, topInset.Y + 10)
```

## UI Animation

### TweenService for UI
```lua
local TweenService = game:GetService("TweenService")

local function animateIn(frame)
    frame.Position = UDim2.new(0.5, 0, 1.5, 0)  -- Start below screen
    frame.Visible = true

    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        {Position = UDim2.new(0.5, 0, 0.5, 0)}
    )
    tween:Play()
    return tween
end

local function animateOut(frame)
    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.In),
        {Position = UDim2.new(0.5, 0, 1.5, 0)}
    )
    tween:Play()
    tween.Completed:Connect(function()
        frame.Visible = false
    end)
    return tween
end
```

### Spring Animation
```lua
local function springAnimation(frame, targetSize, stiffness, damping)
    stiffness = stiffness or 200
    damping = damping or 20

    local currentSize = {frame.Size.X.Scale, frame.Size.Y.Scale}
    local velocity = {0, 0}
    local target = {targetSize.X.Scale, targetSize.Y.Scale}

    local conn
    conn = RunService.RenderStepped:Connect(function(dt)
        for i = 1, 2 do
            local displacement = target[i] - currentSize[i]
            local springForce = displacement * stiffness
            local dampingForce = velocity[i] * damping
            local acceleration = springForce - dampingForce

            velocity[i] = velocity[i] + acceleration * dt
            currentSize[i] = currentSize[i] + velocity[i] * dt
        end

        frame.Size = UDim2.new(currentSize[1], 0, currentSize[2], 0)

        -- Check if settled
        local totalVelocity = math.abs(velocity[1]) + math.abs(velocity[2])
        local totalDisplacement = math.abs(target[1] - currentSize[1]) + math.abs(target[2] - currentSize[2])

        if totalVelocity < 0.001 and totalDisplacement < 0.001 then
            frame.Size = targetSize
            conn:Disconnect()
        end
    end)
end
```

### Stagger Animation
```lua
local function staggerChildren(parent, delay, animateFunc)
    delay = delay or 0.1

    local children = parent:GetChildren()
    for i, child in ipairs(children) do
        task.delay((i - 1) * delay, function()
            animateFunc(child)
        end)
    end
end

-- Usage
staggerChildren(menuFrame, 0.05, function(button)
    button.Position = button.Position + UDim2.new(0.1, 0, 0, 0)
    button.BackgroundTransparency = 1

    TweenService:Create(button, TweenInfo.new(0.3), {
        Position = button.Position - UDim2.new(0.1, 0, 0, 0),
        BackgroundTransparency = 0
    }):Play()
end)
```

## Input Handling

### Button Interactions
```lua
local function setupButton(button)
    local originalSize = button.Size
    local originalColor = button.BackgroundColor3

    -- Hover
    button.MouseEnter:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize + UDim2.new(0.02, 0, 0.02, 0),
            BackgroundColor3 = originalColor:Lerp(Color3.new(1, 1, 1), 0.1)
        }):Play()
    end)

    button.MouseLeave:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize,
            BackgroundColor3 = originalColor
        }):Play()
    end)

    -- Click
    button.MouseButton1Down:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.05), {
            Size = originalSize - UDim2.new(0.01, 0, 0.01, 0)
        }):Play()
    end)

    button.MouseButton1Up:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize
        }):Play()
    end)
end
```

### Drag and Drop
```lua
local function makeDraggable(frame)
    local dragging = false
    local dragStart
    local startPos

    frame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or
           input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = frame.Position

            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)

    frame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or
           input.UserInputType == Enum.UserInputType.Touch then
            if dragging then
                local delta = input.Position - dragStart
                frame.Position = UDim2.new(
                    startPos.X.Scale,
                    startPos.X.Offset + delta.X,
                    startPos.Y.Scale,
                    startPos.Y.Offset + delta.Y
                )
            end
        end
    end)
end
```

### Scroll Handling
```lua
local scrollingFrame = Instance.new("ScrollingFrame")
scrollingFrame.Size = UDim2.new(0.5, 0, 0.5, 0)
scrollingFrame.CanvasSize = UDim2.new(0, 0, 0, 0)  -- Will be auto-sized
scrollingFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y
scrollingFrame.ScrollBarThickness = 8
scrollingFrame.ScrollBarImageColor3 = Color3.fromRGB(100, 100, 100)

-- List layout for automatic sizing
local listLayout = Instance.new("UIListLayout")
listLayout.SortOrder = Enum.SortOrder.LayoutOrder
listLayout.Padding = UDim.new(0, 5)
listLayout.Parent = scrollingFrame

-- Smooth scrolling
local function smoothScrollTo(targetPosition)
    local tween = TweenService:Create(
        scrollingFrame,
        TweenInfo.new(0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
        {CanvasPosition = Vector2.new(0, targetPosition)}
    )
    tween:Play()
end
```

## HUD Systems

### Health Bar
```lua
local function createHealthBar(parent)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(0.3, 0, 0, 30)
    container.Position = UDim2.new(0.02, 0, 0.05, 0)
    container.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    container.Parent = parent

    local fill = Instance.new("Frame")
    fill.Size = UDim2.new(1, 0, 1, 0)
    fill.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
    fill.Parent = container

    -- Delayed damage indicator
    local delayedFill = Instance.new("Frame")
    delayedFill.Size = UDim2.new(1, 0, 1, 0)
    delayedFill.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
    delayedFill.ZIndex = fill.ZIndex - 1
    delayedFill.Parent = container

    local function updateHealth(current, max)
        local ratio = current / max
        local targetSize = UDim2.new(ratio, 0, 1, 0)

        -- Instant fill update
        fill.Size = targetSize

        -- Delayed red bar
        TweenService:Create(delayedFill, TweenInfo.new(0.5), {
            Size = targetSize
        }):Play()

        -- Color based on health
        if ratio > 0.5 then
            fill.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
        elseif ratio > 0.25 then
            fill.BackgroundColor3 = Color3.fromRGB(200, 200, 0)
        else
            fill.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
        end
    end

    return {container = container, update = updateHealth}
end
```

### Minimap
```lua
local function createMinimap(parent, worldSize, minimapSize)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(0, minimapSize, 0, minimapSize)
    container.Position = UDim2.new(1, -minimapSize - 10, 0, 10)
    container.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    container.ClipsDescendants = true
    container.Parent = parent

    -- Player marker
    local playerMarker = Instance.new("Frame")
    playerMarker.Size = UDim2.new(0, 10, 0, 10)
    playerMarker.AnchorPoint = Vector2.new(0.5, 0.5)
    playerMarker.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
    playerMarker.Parent = container

    Instance.new("UICorner", playerMarker).CornerRadius = UDim.new(1, 0)

    local function worldToMinimap(worldPos)
        local x = (worldPos.X / worldSize + 0.5) * minimapSize
        local y = (worldPos.Z / worldSize + 0.5) * minimapSize
        return UDim2.new(0, x, 0, y)
    end

    local function update()
        local character = Players.LocalPlayer.Character
        if not character then return end

        local pos = character.PrimaryPart.Position
        playerMarker.Position = worldToMinimap(pos)

        -- Rotate marker based on facing
        local lookVector = character.PrimaryPart.CFrame.LookVector
        local angle = math.atan2(lookVector.X, lookVector.Z)
        playerMarker.Rotation = math.deg(angle)
    end

    RunService.RenderStepped:Connect(update)

    return container
end
```

### Cooldown Indicator
```lua
local function createCooldownIndicator(button, duration)
    local overlay = Instance.new("Frame")
    overlay.Size = UDim2.new(1, 0, 1, 0)
    overlay.BackgroundColor3 = Color3.new(0, 0, 0)
    overlay.BackgroundTransparency = 0.5
    overlay.ZIndex = button.ZIndex + 1
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

    local cooldownText = Instance.new("TextLabel")
    cooldownText.Size = UDim2.new(1, 0, 1, 0)
    cooldownText.BackgroundTransparency = 1
    cooldownText.TextColor3 = Color3.new(1, 1, 1)
    cooldownText.TextScaled = true
    cooldownText.ZIndex = overlay.ZIndex + 1
    cooldownText.Parent = overlay

    local startTime = os.clock()

    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local remaining = duration - elapsed

        if remaining <= 0 then
            overlay:Destroy()
            conn:Disconnect()
            return
        end

        -- Update sweep
        local progress = elapsed / duration
        gradient.Offset = Vector2.new(0, progress * 2 - 1)

        -- Update text
        cooldownText.Text = string.format("%.1f", remaining)
    end)
end
```

## Menu Systems

### Page Navigation
```lua
local MenuController = {}
MenuController.pageStack = {}

function MenuController.pushPage(pageName)
    local currentPage = MenuController.pageStack[#MenuController.pageStack]
    if currentPage then
        currentPage.Visible = false
    end

    local newPage = Pages[pageName]
    newPage.Visible = true
    table.insert(MenuController.pageStack, newPage)
end

function MenuController.popPage()
    if #MenuController.pageStack <= 1 then return end

    local currentPage = table.remove(MenuController.pageStack)
    currentPage.Visible = false

    local previousPage = MenuController.pageStack[#MenuController.pageStack]
    previousPage.Visible = true
end

function MenuController.goToPage(pageName)
    -- Clear stack and go to specific page
    for _, page in ipairs(MenuController.pageStack) do
        page.Visible = false
    end
    MenuController.pageStack = {}
    MenuController.pushPage(pageName)
end

-- Back button
backButton.MouseButton1Click:Connect(function()
    MenuController.popPage()
end)
```

### Modal Dialog
```lua
local function showModal(title, message, buttons)
    -- Darken background
    local backdrop = Instance.new("Frame")
    backdrop.Size = UDim2.new(1, 0, 1, 0)
    backdrop.BackgroundColor3 = Color3.new(0, 0, 0)
    backdrop.BackgroundTransparency = 0.5
    backdrop.ZIndex = 100
    backdrop.Parent = ScreenGui

    local modal = Instance.new("Frame")
    modal.Size = UDim2.new(0.4, 0, 0.3, 0)
    modal.Position = UDim2.new(0.5, 0, 0.5, 0)
    modal.AnchorPoint = Vector2.new(0.5, 0.5)
    modal.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    modal.ZIndex = 101
    modal.Parent = backdrop

    local titleLabel = Instance.new("TextLabel")
    titleLabel.Text = title
    titleLabel.Size = UDim2.new(1, 0, 0.2, 0)
    titleLabel.BackgroundTransparency = 1
    titleLabel.TextColor3 = Color3.new(1, 1, 1)
    titleLabel.TextScaled = true
    titleLabel.Parent = modal

    local messageLabel = Instance.new("TextLabel")
    messageLabel.Text = message
    messageLabel.Size = UDim2.new(0.9, 0, 0.4, 0)
    messageLabel.Position = UDim2.new(0.05, 0, 0.25, 0)
    messageLabel.BackgroundTransparency = 1
    messageLabel.TextColor3 = Color3.new(0.8, 0.8, 0.8)
    messageLabel.TextWrapped = true
    messageLabel.Parent = modal

    local buttonContainer = Instance.new("Frame")
    buttonContainer.Size = UDim2.new(0.9, 0, 0.25, 0)
    buttonContainer.Position = UDim2.new(0.05, 0, 0.7, 0)
    buttonContainer.BackgroundTransparency = 1
    buttonContainer.Parent = modal

    local listLayout = Instance.new("UIListLayout")
    listLayout.FillDirection = Enum.FillDirection.Horizontal
    listLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
    listLayout.Padding = UDim.new(0, 10)
    listLayout.Parent = buttonContainer

    local result = nil

    for _, buttonData in ipairs(buttons) do
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(0, 100, 1, 0)
        btn.Text = buttonData.text
        btn.BackgroundColor3 = buttonData.color or Color3.fromRGB(60, 60, 60)
        btn.TextColor3 = Color3.new(1, 1, 1)
        btn.Parent = buttonContainer

        btn.MouseButton1Click:Connect(function()
            result = buttonData.value
            backdrop:Destroy()
        end)
    end

    -- Wait for result
    while not result and backdrop.Parent do
        task.wait()
    end

    return result
end

-- Usage
local choice = showModal("Confirm", "Are you sure?", {
    {text = "Yes", value = true, color = Color3.fromRGB(0, 150, 0)},
    {text = "No", value = false, color = Color3.fromRGB(150, 0, 0)}
})
```
