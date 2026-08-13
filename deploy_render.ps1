$apiKey = "rnd_8NiTBeAtgFGI5G4KFlSH40f76Zar"
$ownerId = "tea-d9rm72142hec738qu7pg"

$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Accept"        = "application/json"
    "Content-Type"  = "application/json"
}

$body = @{
    type = "web_service"
    name = "string-bot-session"
    ownerId = $ownerId
    repo = "https://github.com/SayaTeam/STRING_BOT"
    autoDeploy = "yes"
    branch = "main"
    serviceDetails = @{
        env = "python"
        envSpecificDetails = @{
            buildCommand = "pip install -r requirements.txt"
            startCommand = "python main.py"
        }
        region = "singapore"
        plan = "free"
    }
    envVars = @(
        @{ key = "API_ID"; value = "30422005" },
        @{ key = "API_HASH"; value = "5170ded206641d73215baf40175a6924" },
        @{ key = "BOT_TOKEN"; value = "8662603507:AAGdeAAT9xf7pMiITT6H_vENAsnyM95vyVg" },
        @{ key = "OWNER_ID"; value = "5940554521" },
        @{ key = "MONGO_DB_URI"; value = "mongodb+srv://shnwazdeveloperx:shnwazdev@shnwazdev.sqmwbgl.mongodb.net/?appName=shnwazdev" },
        @{ key = "MUST_JOIN"; value = "-1004460771158" }
    )
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "https://api.render.com/v1/services" -Method Post -Headers $headers -Body $body
    Write-Output "Successfully created Render service:"
    Write-Output ($response | ConvertTo-Json -Depth 5)
} catch {
    Write-Output "Render API error:"
    Write-Output $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $errBody = $reader.ReadToEnd()
        Write-Output "Error details: $errBody"
    }
}
