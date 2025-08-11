-- this is heavily pasted
local Drawings, Last = {}, 0

ui.NewTab("PF", "PF")
ui.NewContainer("PF", "Skeletons", "Skeletons")
ui.NewCheckbox("PF", "Skeletons", "Enable Skeletons")
ui.NewColorpicker("PF", "Skeletons", "Color", { r = 255, g = 255, b = 255, a = 255 }, true)
ui.NewCheckbox("PF", "Skeletons", "Render Outlines")

local players = game.Players
local workspace = game.Workspace
local repStorage = game.GetService('ReplicatedStorage')

local localPlayer = game.LocalPlayer
local playerFolders = workspace:FindFirstChild('Players'):GetChildren()

local otherCache = {
    entityData = {},
    playerData = {},
    }

local function checkCache(cache, addresses)
for address, entry in pairs(cache) do
        if not addresses[address] then
            cache[address] = nil
        end
    end
end

local function Get()
    local enemy = {}

    
    local foundAddresses = {}

    for _, playerFolder in pairs(playerFolders) do
        for _, player in pairs(playerFolder:GetChildren()) do
            local playerAddress = player.Address
            foundAddresses[playerAddress] = true

            if not otherCache.playerData[playerAddress] then
                local playerData = {}
                for _, child in pairs(player:GetChildren()) do
                    if playerData.name then
                        break
                    end

                    local nameTag = child:FindFirstChild('NameTagGui')
                    if nameTag then
                        local playerTag = nameTag:FindFirstChild('PlayerTag')
                        if playerTag then
                            playerData.name = playerTag.Value
                        end
                    end
                end

                if playerData.name then
                    local isPlayer = players:FindFirstChild(playerData.name)
                    if isPlayer and isPlayer.Team ~= localPlayer.Team then
                        if not Drawings[playerAddress] or Drawings[playerAddress].Removing then
                            local P = {}

                            for _, Part in ipairs(player:GetChildren()) do
                                if Part.ClassName == "Part" then
                                    local Type

                                    for _, C in ipairs(Part:GetChildren()) do
                                        if C.ClassName == "SpotLight" then
                                            Type = "Torso"
                                        elseif C.ClassName == "BillboardGui" then
                                            Type = "Head"
                                        end
                                    end

                                    if not Type then
                                        for _, C in ipairs(Part:GetChildren()) do
                                            local ID = C.SpecialMeshTextureId
                                            if ID == "rbxassetid://5614184140" or ID == "rbxassetid://5614184106" then
                                                Type = "Arm"
                                            elseif ID == "rbxassetid://5558971297" or ID == "rbxassetid://5558971356" then
                                                Type = "Leg"
                                            end
                                        end
                                    end

                                    if Type == "Torso" then
                                        P.Torso = Part
                                    elseif Type == "Head" then
                                        P.Head = Part
                                    elseif Type == "Arm" and not P.LArm then
                                        P.LArm = Part
                                    elseif Type == "Arm" then
                                        P.RArm = Part
                                    elseif Type == "Leg" and not P.LLeg then
                                        P.LLeg = Part
                                    elseif Type == "Leg" then
                                        P.RLeg = Part
                                    end
                                end
                            end

                            Drawings[playerAddress] = {
                                Parts = P,
                                SAlpha = 0,
                                EAlpha = 255,
                                Removing = false
                            }
                        else
                            Drawings[playerAddress].EAlpha = 255
                            Drawings[playerAddress].Removing = false
                        end           
                    else
                        otherCache.playerData[playerAddress] = 'ignore'
                    end
                else
                    otherCache.playerData[playerAddress] = 'ignore'
                end
            end
        end
    end
    checkCache(otherCache.playerData, foundAddresses)

    for _, playerFolder in ipairs(game.Workspace.Players:GetChildren()) do
        for _, player in ipairs(playerFolder:GetChildren()) do
            local playerAddress = player.Address
            foundAddresses[playerAddress] = true

           
        end
    end

    for playerAddress, D in pairs(Drawings) do
        if not foundAddresses[playerAddress] and not D.Removing then
            D.EAlpha = 0
            D.Removing = true
        end
    end
end

local function Update()
    local Tick = utility.GetTickCount()
    if Tick - Last < 5 then return end
    Last = Tick

    for _, D in pairs(Drawings) do
        if D.Removing then goto continue end

        local P = D.Parts
        if P.Torso then P.TorsoPos, P.TorsoUp = P.Torso.Position, P.Torso.UpVector end
        if P.Head  then P.HeadPos  = P.Head.Position end
        if P.LArm  then P.LArmPos, P.LArmUp = P.LArm.Position, P.LArm.UpVector end
        if P.RArm  then P.RArmPos, P.RArmUp = P.RArm.Position, P.RArm.UpVector end
        if P.LLeg  then P.LLegPos, P.LLegUp = P.LLeg.Position, P.LLeg.UpVector end
        if P.RLeg  then P.RLegPos, P.RLegUp = P.RLeg.Position, P.RLeg.UpVector end

        ::continue::
    end
end

local function Render()
    if not ui.GetValue("PF", "Skeletons", "Enable Skeletons") then return end

    local Color   = ui.GetValue("PF", "Skeletons", "Color")
    local LColor  = Color3.new(Color.r / 255, Color.g / 255, Color.b / 255, Color.a)
    local OColor  = Color3.new(0, 0, 0)
    local Outline = ui.GetValue("PF", "Skeletons", "Render Outlines")
    local Delta   = utility.GetDeltaTime() * 8

    local function DrawLine(S, E, A)
        local SX, SY, SO = utility.WorldToScreen(S)
        local EX, EY, EO = utility.WorldToScreen(E)
        if SO and EO then
            if Outline then
                draw.Line(SX, SY, EX, EY, OColor, 3, Color.a)
            end
            draw.Line(SX, SY, EX, EY, LColor, 1, Color.a)
        end
    end

    for A, D in pairs(Drawings) do
        D.SAlpha = D.SAlpha + (D.EAlpha - D.SAlpha) * Delta

        if D.Removing and D.SAlpha < 1 then
            Drawings[A] = nil
            goto continue
        end

        local P = D.Parts
        if not P.TorsoPos then goto continue end

        local Mid    = P.TorsoPos + P.TorsoUp * 0.5
        local Pelvis = P.TorsoPos - P.TorsoUp

        DrawLine(Pelvis, Mid, D.SAlpha)

        if P.HeadPos then
            DrawLine(Mid, P.HeadPos, D.SAlpha)
        end

        if P.LArmPos and P.LArmUp then
            local Elbow = Vector3.new(P.LArmPos.X, Mid.Y - 0.79, P.LArmPos.Z - 0.95)
            DrawLine(Mid, Elbow, D.SAlpha)
            DrawLine(Elbow, P.LArmPos - P.LArmUp * 0.89, D.SAlpha)
        end

        if P.RArmPos and P.RArmUp then
            local Elbow = Vector3.new(P.RArmPos.X, Mid.Y - 0.79, P.RArmPos.Z - 0.95)
            DrawLine(Mid, Elbow, D.SAlpha)
            DrawLine(Elbow, P.RArmPos - P.RArmUp * 0.89, D.SAlpha)
        end

        if P.LLegPos and P.LLegUp then
            local Knee = P.LLegPos + P.LLegUp * 0.5
            DrawLine(Pelvis, Knee, D.SAlpha)
            DrawLine(Knee, P.LLegPos - P.LLegUp * 0.89, D.SAlpha)
        end

        if P.RLegPos and P.RLegUp then
            local Knee = P.RLegPos + P.RLegUp * 0.5
            DrawLine(Pelvis, Knee, D.SAlpha)
            DrawLine(Knee, P.RLegPos - P.RLegUp * 0.89, D.SAlpha)
        end

        ::continue::
    end
end

cheat.Register("onUpdate", function()
    Get()
    Update()
end)

cheat.Register("onPaint", Render)

