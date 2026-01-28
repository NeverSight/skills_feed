---
name: data-persistence
description: Implements data persistence systems including DataStore patterns, session locking, data migration, error handling, and backup systems. Use when saving player progress, inventory, settings, or any persistent data.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Data Persistence

When implementing data persistence, follow these patterns for reliable and secure data storage.

## DataStore Basics

### Data Manager Module
```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local DataManager = {}
DataManager.cache = {}
DataManager.dataStore = DataStoreService:GetDataStore("PlayerData_v1")

local DEFAULT_DATA = {
    version = 1,
    coins = 0,
    gems = 0,
    level = 1,
    experience = 0,
    inventory = {},
    settings = {
        musicVolume = 0.5,
        sfxVolume = 0.5
    },
    stats = {
        totalPlayTime = 0,
        totalKills = 0,
        totalDeaths = 0
    }
}

function DataManager.getKey(player)
    return "Player_" .. player.UserId
end

function DataManager.deepCopy(original)
    local copy = {}
    for k, v in pairs(original) do
        if type(v) == "table" then
            copy[k] = DataManager.deepCopy(v)
        else
            copy[k] = v
        end
    end
    return copy
end

function DataManager.reconcile(data, template)
    for key, value in pairs(template) do
        if data[key] == nil then
            if type(value) == "table" then
                data[key] = DataManager.deepCopy(value)
            else
                data[key] = value
            end
        elseif type(value) == "table" and type(data[key]) == "table" then
            DataManager.reconcile(data[key], value)
        end
    end
end
```

### Loading Data with Retry
```lua
local MAX_RETRIES = 3
local RETRY_DELAY = 1

function DataManager.load(player)
    local key = DataManager.getKey(player)
    local data = nil
    local success = false

    for attempt = 1, MAX_RETRIES do
        local ok, result = pcall(function()
            return DataManager.dataStore:GetAsync(key)
        end)

        if ok then
            data = result
            success = true
            break
        else
            warn("DataStore load failed (attempt " .. attempt .. "):", result)
            if attempt < MAX_RETRIES then
                task.wait(RETRY_DELAY * attempt)  -- Exponential backoff
            end
        end
    end

    if not success then
        -- Use default data but mark as failed
        data = DataManager.deepCopy(DEFAULT_DATA)
        data._loadFailed = true
        warn("Using default data for", player.Name, "- load failed")
    elseif data == nil then
        -- New player
        data = DataManager.deepCopy(DEFAULT_DATA)
    else
        -- Reconcile with defaults (add missing fields)
        DataManager.reconcile(data, DEFAULT_DATA)
    end

    -- Migrate if needed
    data = DataManager.migrate(data)

    DataManager.cache[player.UserId] = data
    return data
end
```

### Saving Data
```lua
function DataManager.save(player, async)
    local key = DataManager.getKey(player)
    local data = DataManager.cache[player.UserId]

    if not data then
        warn("No data to save for", player.Name)
        return false
    end

    -- Don't save if load failed (prevent data loss)
    if data._loadFailed then
        warn("Skipping save for", player.Name, "- original load failed")
        return false
    end

    -- Remove internal flags before saving
    local saveData = DataManager.deepCopy(data)
    saveData._loadFailed = nil

    local saveFunc = function()
        local success, err = pcall(function()
            DataManager.dataStore:SetAsync(key, saveData)
        end)

        if not success then
            warn("DataStore save failed for", player.Name, ":", err)
        end

        return success
    end

    if async then
        task.spawn(saveFunc)
        return true
    else
        return saveFunc()
    end
end
```

### Auto-Save System
```lua
local AUTO_SAVE_INTERVAL = 300  -- 5 minutes

function DataManager.startAutoSave(player)
    task.spawn(function()
        while player.Parent do
            task.wait(AUTO_SAVE_INTERVAL)
            if player.Parent then
                DataManager.save(player, true)
            end
        end
    end)
end

-- Save on player leaving
Players.PlayerRemoving:Connect(function(player)
    DataManager.save(player, false)  -- Synchronous save
    DataManager.cache[player.UserId] = nil
end)

-- Save all on server shutdown
game:BindToClose(function()
    local saveThreads = {}

    for _, player in ipairs(Players:GetPlayers()) do
        table.insert(saveThreads, task.spawn(function()
            DataManager.save(player, false)
        end))
    end

    -- Wait for all saves (max 30 seconds)
    task.wait(30)
end)
```

## Session Locking

### Prevent Double-Loading
```lua
local MemoryStoreService = game:GetService("MemoryStoreService")
local sessionMap = MemoryStoreService:GetSortedMap("SessionLocks")

local LOCK_DURATION = 3600  -- 1 hour
local SESSION_ID = game.JobId

function DataManager.acquireLock(player)
    local key = "Lock_" .. player.UserId

    local success, currentLock = pcall(function()
        return sessionMap:GetAsync(key)
    end)

    if success and currentLock and currentLock ~= SESSION_ID then
        -- Another session has the lock
        return false, "Data is being used in another server"
    end

    -- Try to acquire lock
    local acquired, err = pcall(function()
        sessionMap:SetAsync(key, SESSION_ID, LOCK_DURATION)
    end)

    return acquired, err
end

function DataManager.releaseLock(player)
    local key = "Lock_" .. player.UserId

    pcall(function()
        sessionMap:RemoveAsync(key)
    end)
end

function DataManager.refreshLock(player)
    local key = "Lock_" .. player.UserId

    pcall(function()
        sessionMap:SetAsync(key, SESSION_ID, LOCK_DURATION)
    end)
end

-- Modified load with session locking
function DataManager.loadWithLock(player)
    local locked, lockErr = DataManager.acquireLock(player)

    if not locked then
        player:Kick("Your data is being used in another server. Please wait a moment.")
        return nil
    end

    local data = DataManager.load(player)

    -- Refresh lock periodically
    task.spawn(function()
        while player.Parent and DataManager.cache[player.UserId] do
            task.wait(300)  -- Refresh every 5 minutes
            DataManager.refreshLock(player)
        end
    end)

    return data
end
```

## Data Migration

### Version-Based Migration
```lua
local CURRENT_VERSION = 3

local migrations = {
    [2] = function(data)
        -- v1 -> v2: Convert inventory from array to dictionary
        if data.inventory and type(data.inventory[1]) == "string" then
            local newInventory = {}
            for _, itemId in ipairs(data.inventory) do
                newInventory[itemId] = (newInventory[itemId] or 0) + 1
            end
            data.inventory = newInventory
        end
        return data
    end,

    [3] = function(data)
        -- v2 -> v3: Add new stats field
        data.stats = data.stats or {}
        data.stats.achievementsUnlocked = data.stats.achievementsUnlocked or {}
        return data
    end
}

function DataManager.migrate(data)
    local version = data.version or 1

    while version < CURRENT_VERSION do
        local nextVersion = version + 1
        local migrationFunc = migrations[nextVersion]

        if migrationFunc then
            print("Migrating data from v" .. version .. " to v" .. nextVersion)
            data = migrationFunc(data)
            data.version = nextVersion
        end

        version = nextVersion
    end

    return data
end
```

## UpdateAsync for Atomic Operations

### Safe Currency Operations
```lua
function DataManager.addCurrency(player, currencyType, amount)
    local key = DataManager.getKey(player)

    local success, newValue = pcall(function()
        return DataManager.dataStore:UpdateAsync(key, function(oldData)
            if not oldData then
                oldData = DataManager.deepCopy(DEFAULT_DATA)
            end

            oldData[currencyType] = (oldData[currencyType] or 0) + amount

            -- Update cache
            if DataManager.cache[player.UserId] then
                DataManager.cache[player.UserId][currencyType] = oldData[currencyType]
            end

            return oldData
        end)
    end)

    return success, newValue and newValue[currencyType]
end

function DataManager.removeCurrency(player, currencyType, amount)
    local key = DataManager.getKey(player)

    local success, newValue, sufficient = false, nil, false

    success = pcall(function()
        newValue = DataManager.dataStore:UpdateAsync(key, function(oldData)
            if not oldData then
                return nil  -- Abort
            end

            local current = oldData[currencyType] or 0

            if current < amount then
                sufficient = false
                return nil  -- Abort, not enough currency
            end

            sufficient = true
            oldData[currencyType] = current - amount

            if DataManager.cache[player.UserId] then
                DataManager.cache[player.UserId][currencyType] = oldData[currencyType]
            end

            return oldData
        end)
    end)

    return success and sufficient, newValue and newValue[currencyType]
end
```

## OrderedDataStore for Leaderboards

### Global Leaderboard
```lua
local LeaderboardService = {}
local leaderboardStore = DataStoreService:GetOrderedDataStore("GlobalLeaderboard_v1")

function LeaderboardService.submitScore(player, score)
    local key = tostring(player.UserId)

    local success, err = pcall(function()
        leaderboardStore:SetAsync(key, score)
    end)

    return success
end

function LeaderboardService.getTopScores(limit)
    limit = limit or 100

    local success, pages = pcall(function()
        return leaderboardStore:GetSortedAsync(false, limit)  -- false = descending
    end)

    if not success then
        return nil
    end

    local scores = {}
    local page = pages:GetCurrentPage()

    for rank, entry in ipairs(page) do
        table.insert(scores, {
            rank = rank,
            userId = tonumber(entry.key),
            score = entry.value
        })
    end

    return scores
end

function LeaderboardService.getPlayerRank(player)
    local key = tostring(player.UserId)

    -- Get player's score
    local success, score = pcall(function()
        return leaderboardStore:GetAsync(key)
    end)

    if not success or not score then
        return nil
    end

    -- Count how many scores are higher
    local rank = 1
    local pages = leaderboardStore:GetSortedAsync(false, 100)

    while true do
        local page = pages:GetCurrentPage()

        for _, entry in ipairs(page) do
            if entry.value > score then
                rank = rank + 1
            elseif entry.key == key then
                return rank
            end
        end

        if pages.IsFinished then
            break
        end

        pages:AdvanceToNextPageAsync()
    end

    return rank
end
```

## MemoryStore for Temporary Data

### Cross-Server Communication
```lua
local MemoryStoreService = game:GetService("MemoryStoreService")
local globalQueue = MemoryStoreService:GetQueue("GlobalAnnouncements")
local serverStatus = MemoryStoreService:GetSortedMap("ServerStatus")

-- Publish announcement to all servers
function publishAnnouncement(message)
    pcall(function()
        globalQueue:AddAsync(message, 300)  -- 5 minute expiration
    end)
end

-- Process announcements
task.spawn(function()
    while true do
        local success, items = pcall(function()
            return globalQueue:ReadAsync(10, false, 5)
        end)

        if success and items then
            for _, item in ipairs(items) do
                -- Show announcement to all players
                showAnnouncement(item)
            end

            -- Remove processed items
            pcall(function()
                globalQueue:RemoveAsync(items[#items].id)
            end)
        end

        task.wait(5)
    end
end)

-- Register server status
function updateServerStatus()
    pcall(function()
        serverStatus:SetAsync(game.JobId, {
            playerCount = #Players:GetPlayers(),
            maxPlayers = Players.MaxPlayers,
            mapName = getCurrentMap(),
            lastUpdate = os.time()
        }, 120)  -- 2 minute expiration
    end)
end

task.spawn(function()
    while true do
        updateServerStatus()
        task.wait(60)
    end
end)
```

## Backup & Recovery

### Periodic Backups
```lua
local BackupService = {}
local backupStore = DataStoreService:GetDataStore("PlayerBackups")
local MAX_BACKUPS = 5

function BackupService.createBackup(player)
    local data = DataManager.cache[player.UserId]
    if not data then return false end

    local backupKey = "Backup_" .. player.UserId
    local timestamp = os.time()

    local success = pcall(function()
        backupStore:UpdateAsync(backupKey, function(backups)
            backups = backups or {}

            -- Add new backup
            table.insert(backups, {
                timestamp = timestamp,
                data = DataManager.deepCopy(data)
            })

            -- Keep only recent backups
            while #backups > MAX_BACKUPS do
                table.remove(backups, 1)
            end

            return backups
        end)
    end)

    return success
end

function BackupService.listBackups(userId)
    local backupKey = "Backup_" .. userId

    local success, backups = pcall(function()
        return backupStore:GetAsync(backupKey)
    end)

    if success and backups then
        local list = {}
        for i, backup in ipairs(backups) do
            table.insert(list, {
                index = i,
                timestamp = backup.timestamp,
                date = os.date("%Y-%m-%d %H:%M:%S", backup.timestamp)
            })
        end
        return list
    end

    return {}
end

function BackupService.restoreBackup(userId, backupIndex)
    local backupKey = "Backup_" .. userId

    local success, backup = pcall(function()
        local backups = backupStore:GetAsync(backupKey)
        return backups and backups[backupIndex]
    end)

    if success and backup then
        local mainKey = "Player_" .. userId
        return pcall(function()
            DataManager.dataStore:SetAsync(mainKey, backup.data)
        end)
    end

    return false
end
```

## Error Handling Best Practices

### Comprehensive Error Handling
```lua
local function safeDataOperation(operation, ...)
    local args = {...}
    local attempts = 0
    local maxAttempts = 3

    while attempts < maxAttempts do
        attempts = attempts + 1

        local success, result = pcall(operation, unpack(args))

        if success then
            return true, result
        end

        -- Check error type
        local errorMsg = tostring(result)

        if errorMsg:find("502") or errorMsg:find("503") then
            -- Service unavailable, retry with backoff
            task.wait(2 ^ attempts)
        elseif errorMsg:find("Request was throttled") then
            -- Rate limited, wait longer
            task.wait(6)
        elseif errorMsg:find("Key not found") then
            -- Key doesn't exist (not an error for GetAsync)
            return true, nil
        else
            -- Unknown error, log and retry
            warn("DataStore error:", errorMsg)
            task.wait(1)
        end
    end

    return false, "Max retries exceeded"
end
```
