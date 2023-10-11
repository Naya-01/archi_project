math.randomseed(os.time())

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

-- Fonction pour générer un corps de requête aléatoire
function generateRandomBody()
    local keySizeOptions = {8, 16, 32}
    local fileSizeOptions = {100, 1000, 10000}

    local keySize = keySizeOptions[math.random(1, #keySizeOptions)]
    local fileSize = fileSizeOptions[math.random(1, #fileSizeOptions)]
    local numRounds = math.random(1, 10)
    local key = randomString(keySize)
    local file = randomString(fileSize)
    local body = string.format("%d,%d,%d,%s%s", keySize, fileSize, numRounds, key, file)
    print("Generated request body:", body)

    return body
end

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"

-- Appel à la fonction pour générer le corps de requête
wrk.body = generateRandomBody()