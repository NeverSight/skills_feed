---
name: procedural-generation
description: Implements procedural generation systems including noise functions, terrain generation, dungeon generation, city generation, and object placement. Use when building roguelikes, open worlds, or any content that needs to be generated algorithmically.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Procedural Generation

When implementing procedural generation, use these patterns for performant and interesting content.

## Noise Functions

### Multi-Octave Perlin Noise
```lua
local function octaveNoise(x, y, octaves, persistence, scale, lacunarity)
    octaves = octaves or 4
    persistence = persistence or 0.5
    scale = scale or 1
    lacunarity = lacunarity or 2

    local total = 0
    local frequency = scale
    local amplitude = 1
    local maxValue = 0

    for i = 1, octaves do
        total = total + math.noise(x * frequency, y * frequency) * amplitude
        maxValue = maxValue + amplitude
        amplitude = amplitude * persistence
        frequency = frequency * lacunarity
    end

    return total / maxValue  -- Normalize to [-1, 1]
end

-- Usage for terrain
local function getTerrainHeight(x, z)
    local baseHeight = octaveNoise(x, z, 4, 0.5, 0.01) * 50  -- Large features
    local detail = octaveNoise(x, z, 2, 0.5, 0.1) * 5        -- Small details
    return baseHeight + detail + 10  -- Base height offset
end
```

### Domain Warping
```lua
-- Use noise to distort noise coordinates for more organic shapes
local function warpedNoise(x, y, scale, warpStrength)
    local warpX = math.noise(x * scale, y * scale, 0) * warpStrength
    local warpY = math.noise(x * scale, y * scale, 100) * warpStrength

    return math.noise((x + warpX) * scale, (y + warpY) * scale)
end

-- Creates more interesting, swirly patterns
local function getWarpedTerrainHeight(x, z)
    local warp1 = warpedNoise(x, z, 0.005, 50)
    local warp2 = warpedNoise(x, z, 0.02, 10)
    return (warp1 * 40 + warp2 * 10) + 20
end
```

### Ridged Noise (Mountains)
```lua
local function ridgedNoise(x, y, octaves, scale)
    local total = 0
    local frequency = scale
    local amplitude = 1
    local weight = 1

    for i = 1, octaves do
        local noise = math.noise(x * frequency, y * frequency)
        noise = 1 - math.abs(noise)  -- Create ridges
        noise = noise * noise        -- Sharpen ridges
        noise = noise * weight
        weight = math.clamp(noise * 2, 0, 1)

        total = total + noise * amplitude
        amplitude = amplitude * 0.5
        frequency = frequency * 2
    end

    return total
end
```

## Terrain Generation

### Heightmap-Based Terrain
```lua
local TerrainGenerator = {}

function TerrainGenerator.generateChunk(chunkX, chunkZ, chunkSize, resolution)
    local terrain = workspace.Terrain
    local heightMap = {}

    -- Generate height map
    for x = 0, resolution do
        heightMap[x] = {}
        for z = 0, resolution do
            local worldX = chunkX * chunkSize + (x / resolution) * chunkSize
            local worldZ = chunkZ * chunkSize + (z / resolution) * chunkSize

            local height = getTerrainHeight(worldX, worldZ)
            heightMap[x][z] = height
        end
    end

    -- Fill terrain
    local cellSize = chunkSize / resolution
    for x = 0, resolution - 1 do
        for z = 0, resolution - 1 do
            local worldX = chunkX * chunkSize + x * cellSize
            local worldZ = chunkZ * chunkSize + z * cellSize

            local h1 = heightMap[x][z]
            local h2 = heightMap[x + 1][z]
            local h3 = heightMap[x][z + 1]
            local h4 = heightMap[x + 1][z + 1]

            local minH = math.min(h1, h2, h3, h4)
            local maxH = math.max(h1, h2, h3, h4)

            local material = TerrainGenerator.getMaterial(maxH, maxH - minH)

            terrain:FillBlock(
                CFrame.new(worldX + cellSize/2, (minH + maxH)/2, worldZ + cellSize/2),
                Vector3.new(cellSize, maxH - minH + 1, cellSize),
                material
            )
        end
    end
end

function TerrainGenerator.getMaterial(height, slope)
    if slope > 2 then
        return Enum.Material.Rock  -- Steep = rock
    elseif height > 80 then
        return Enum.Material.Snow  -- High = snow
    elseif height > 40 then
        return Enum.Material.Rock
    elseif height > 5 then
        return Enum.Material.Grass
    else
        return Enum.Material.Sand  -- Low = sand/beach
    end
end
```

### Biome System
```lua
local function getBiome(x, z)
    local temperature = octaveNoise(x, z, 2, 0.5, 0.001) -- -1 to 1
    local moisture = octaveNoise(x + 1000, z + 1000, 2, 0.5, 0.001)

    temperature = (temperature + 1) / 2  -- 0 to 1
    moisture = (moisture + 1) / 2

    if temperature < 0.3 then
        return moisture > 0.5 and "snow_forest" or "tundra"
    elseif temperature < 0.6 then
        if moisture < 0.3 then
            return "plains"
        elseif moisture < 0.7 then
            return "forest"
        else
            return "swamp"
        end
    else
        return moisture < 0.4 and "desert" or "jungle"
    end
end

local BiomeSettings = {
    desert = {
        heightScale = 20,
        material = Enum.Material.Sand,
        treeDensity = 0,
        grassDensity = 0
    },
    forest = {
        heightScale = 40,
        material = Enum.Material.Grass,
        treeDensity = 0.3,
        grassDensity = 0.8
    },
    -- etc.
}
```

## Dungeon Generation

### BSP (Binary Space Partitioning)
```lua
local DungeonGenerator = {}

local function splitRoom(room, minSize)
    local rooms = {}

    local canSplitH = room.width >= minSize * 2
    local canSplitV = room.height >= minSize * 2

    if not canSplitH and not canSplitV then
        return {room}
    end

    local splitHorizontal
    if canSplitH and canSplitV then
        splitHorizontal = math.random() > 0.5
    else
        splitHorizontal = canSplitH
    end

    if splitHorizontal then
        local splitX = room.x + math.random(minSize, room.width - minSize)
        local room1 = {x = room.x, y = room.y, width = splitX - room.x, height = room.height}
        local room2 = {x = splitX, y = room.y, width = room.x + room.width - splitX, height = room.height}

        for _, r in ipairs(splitRoom(room1, minSize)) do
            table.insert(rooms, r)
        end
        for _, r in ipairs(splitRoom(room2, minSize)) do
            table.insert(rooms, r)
        end
    else
        local splitY = room.y + math.random(minSize, room.height - minSize)
        local room1 = {x = room.x, y = room.y, width = room.width, height = splitY - room.y}
        local room2 = {x = room.x, y = splitY, width = room.width, height = room.y + room.height - splitY}

        for _, r in ipairs(splitRoom(room1, minSize)) do
            table.insert(rooms, r)
        end
        for _, r in ipairs(splitRoom(room2, minSize)) do
            table.insert(rooms, r)
        end
    end

    return rooms
end

function DungeonGenerator.generate(width, height, minRoomSize)
    local initialRoom = {x = 0, y = 0, width = width, height = height}
    local partitions = splitRoom(initialRoom, minRoomSize)

    -- Shrink partitions to create rooms with walls between
    local rooms = {}
    for _, partition in ipairs(partitions) do
        local padding = 2
        local room = {
            x = partition.x + padding,
            y = partition.y + padding,
            width = partition.width - padding * 2,
            height = partition.height - padding * 2
        }
        if room.width > 0 and room.height > 0 then
            table.insert(rooms, room)
        end
    end

    -- Connect rooms with corridors
    local corridors = {}
    for i = 1, #rooms - 1 do
        local r1 = rooms[i]
        local r2 = rooms[i + 1]

        local x1 = r1.x + r1.width / 2
        local y1 = r1.y + r1.height / 2
        local x2 = r2.x + r2.width / 2
        local y2 = r2.y + r2.height / 2

        -- L-shaped corridor
        if math.random() > 0.5 then
            table.insert(corridors, {x1 = x1, y1 = y1, x2 = x2, y2 = y1})
            table.insert(corridors, {x1 = x2, y1 = y1, x2 = x2, y2 = y2})
        else
            table.insert(corridors, {x1 = x1, y1 = y1, x2 = x1, y2 = y2})
            table.insert(corridors, {x1 = x1, y1 = y2, x2 = x2, y2 = y2})
        end
    end

    return rooms, corridors
end

function DungeonGenerator.buildInWorld(rooms, corridors, floorHeight)
    local dungeonModel = Instance.new("Model")
    dungeonModel.Name = "Dungeon"

    -- Build rooms
    for _, room in ipairs(rooms) do
        local floor = Instance.new("Part")
        floor.Size = Vector3.new(room.width, 1, room.height)
        floor.Position = Vector3.new(room.x + room.width/2, floorHeight, room.y + room.height/2)
        floor.Anchored = true
        floor.Material = Enum.Material.Cobblestone
        floor.Parent = dungeonModel

        -- Walls
        -- ... add wall parts
    end

    -- Build corridors
    for _, corridor in ipairs(corridors) do
        local dx = corridor.x2 - corridor.x1
        local dy = corridor.y2 - corridor.y1
        local length = math.sqrt(dx*dx + dy*dy)

        local floor = Instance.new("Part")
        floor.Size = Vector3.new(3, 1, length)
        floor.CFrame = CFrame.lookAt(
            Vector3.new((corridor.x1 + corridor.x2)/2, floorHeight, (corridor.y1 + corridor.y2)/2),
            Vector3.new(corridor.x2, floorHeight, corridor.y2)
        )
        floor.Anchored = true
        floor.Material = Enum.Material.Cobblestone
        floor.Parent = dungeonModel
    end

    dungeonModel.Parent = workspace
    return dungeonModel
end
```

### Cellular Automata (Caves)
```lua
local function generateCave(width, height, fillChance, iterations)
    -- Initialize with random fill
    local grid = {}
    for x = 1, width do
        grid[x] = {}
        for y = 1, height do
            if x == 1 or x == width or y == 1 or y == height then
                grid[x][y] = 1  -- Walls at edges
            else
                grid[x][y] = math.random() < fillChance and 1 or 0
            end
        end
    end

    -- Apply cellular automata rules
    for _ = 1, iterations do
        local newGrid = {}
        for x = 1, width do
            newGrid[x] = {}
            for y = 1, height do
                local neighbors = 0
                for dx = -1, 1 do
                    for dy = -1, 1 do
                        if dx ~= 0 or dy ~= 0 then
                            local nx, ny = x + dx, y + dy
                            if nx >= 1 and nx <= width and ny >= 1 and ny <= height then
                                neighbors = neighbors + grid[nx][ny]
                            else
                                neighbors = neighbors + 1  -- Out of bounds = wall
                            end
                        end
                    end
                end

                -- Rule: become wall if 5+ neighbors are walls
                if neighbors >= 5 then
                    newGrid[x][y] = 1
                elseif neighbors <= 3 then
                    newGrid[x][y] = 0
                else
                    newGrid[x][y] = grid[x][y]
                end
            end
        end
        grid = newGrid
    end

    return grid
end
```

## Object Placement

### Poisson Disc Sampling
```lua
local function poissonDiscSampling(width, height, minDistance, maxAttempts)
    maxAttempts = maxAttempts or 30
    local cellSize = minDistance / math.sqrt(2)
    local gridWidth = math.ceil(width / cellSize)
    local gridHeight = math.ceil(height / cellSize)

    local grid = {}
    for i = 1, gridWidth do
        grid[i] = {}
    end

    local points = {}
    local activeList = {}

    -- Start with random point
    local startX = math.random() * width
    local startY = math.random() * height
    table.insert(points, {x = startX, y = startY})
    table.insert(activeList, 1)

    local gx = math.floor(startX / cellSize) + 1
    local gy = math.floor(startY / cellSize) + 1
    grid[gx][gy] = 1

    while #activeList > 0 do
        local activeIndex = math.random(#activeList)
        local currentPoint = points[activeList[activeIndex]]
        local found = false

        for _ = 1, maxAttempts do
            local angle = math.random() * math.pi * 2
            local distance = minDistance + math.random() * minDistance

            local newX = currentPoint.x + math.cos(angle) * distance
            local newY = currentPoint.y + math.sin(angle) * distance

            if newX >= 0 and newX < width and newY >= 0 and newY < height then
                local gx = math.floor(newX / cellSize) + 1
                local gy = math.floor(newY / cellSize) + 1

                local valid = true

                -- Check neighbors
                for dx = -2, 2 do
                    for dy = -2, 2 do
                        local checkX = gx + dx
                        local checkY = gy + dy

                        if checkX >= 1 and checkX <= gridWidth and
                           checkY >= 1 and checkY <= gridHeight and
                           grid[checkX][checkY] then

                            local otherPoint = points[grid[checkX][checkY]]
                            local dist = math.sqrt((newX - otherPoint.x)^2 + (newY - otherPoint.y)^2)

                            if dist < minDistance then
                                valid = false
                                break
                            end
                        end
                    end
                    if not valid then break end
                end

                if valid then
                    local newIndex = #points + 1
                    table.insert(points, {x = newX, y = newY})
                    table.insert(activeList, newIndex)
                    grid[gx][gy] = newIndex
                    found = true
                    break
                end
            end
        end

        if not found then
            table.remove(activeList, activeIndex)
        end
    end

    return points
end

-- Place trees using Poisson disc
local function placeVegetation(area, density)
    local minDistance = 5 / density  -- Higher density = closer spacing
    local points = poissonDiscSampling(area.width, area.height, minDistance)

    for _, point in ipairs(points) do
        local worldX = area.x + point.x
        local worldZ = area.y + point.y

        -- Raycast down to find ground
        local ray = workspace:Raycast(
            Vector3.new(worldX, 1000, worldZ),
            Vector3.new(0, -2000, 0)
        )

        if ray then
            local tree = ReplicatedStorage.Trees:GetChildren()[math.random(#ReplicatedStorage.Trees:GetChildren())]:Clone()
            tree:PivotTo(CFrame.new(ray.Position))
            tree.Parent = workspace.Vegetation
        end
    end
end
```

## Seeded Generation

### Deterministic Random
```lua
local SeededRandom = {}

function SeededRandom.new(seed)
    local rng = Random.new(seed)
    return {
        next = function(self, min, max)
            if max then
                return rng:NextInteger(min, max)
            elseif min then
                return rng:NextInteger(1, min)
            else
                return rng:NextNumber()
            end
        end,
        shuffle = function(self, array)
            local n = #array
            for i = n, 2, -1 do
                local j = rng:NextInteger(1, i)
                array[i], array[j] = array[j], array[i]
            end
            return array
        end
    }
end

-- Reproducible world generation
local function generateWorld(seed)
    local rng = SeededRandom.new(seed)

    -- Same seed always produces same world
    local numRooms = rng:next(5, 10)
    local rooms = {}

    for i = 1, numRooms do
        table.insert(rooms, {
            x = rng:next(0, 100),
            y = rng:next(0, 100),
            width = rng:next(5, 15),
            height = rng:next(5, 15)
        })
    end

    return rooms
end
```
