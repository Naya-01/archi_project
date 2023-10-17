math.randomseed(os.time())

-- Liste des paramètres à tester
keySizeOptions = {8,16,32,64}
fileSizeOptions = {8,16,32,64}
numRoundsOptions = {5}

-- ...

function writeScriptToFile(keySize, fileSize, numRounds, body)
    local scriptContent = string.format([[
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
wrk.body = "%s"
]], body)

    local scriptFileName = string.format("./wrk_scripts/script_%d_%d_%d.lua", keySize, fileSize, numRounds)
    local file = io.open(scriptFileName, "w")
    if file then
        file:write(scriptContent)
        file:close()
        print("Script written to:", scriptFileName)
    else
        print("Error writing script to file:", scriptFileName)
    end
end


-- Fonction pour générer une chaîne aléatoire de longueur 'length'
function randomString(length)
    local characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    local str = ""

    for i = 1, length do
        local randIndex = math.random(1, #characters)
        str = str .. string.sub(characters, randIndex, randIndex)
    end

    return str
end

-- Fonction pour générer un corps de requête avec différentes combinaisons de paramètres
function generateRandomBody(keySize, fileSize, numRounds)
    local key = randomString(keySize)
    local file = randomString(fileSize)
    local body = string.format("%d,%d,%d,%s%s", keySize, fileSize, numRounds, key, file)
    return body
end

-- Test de toutes les combinaisons possibles
for _, keySize in ipairs(keySizeOptions) do
    for _, fileSize in ipairs(fileSizeOptions) do
        for _, numRounds in ipairs(numRoundsOptions) do
            -- Appel à la fonction pour générer le corps de requête avec la combinaison actuelle
            local body = generateRandomBody(keySize, fileSize, numRounds)

            -- Écrire le script dans un fichier
            writeScriptToFile(keySize, fileSize, numRounds, body)
        end
    end
end