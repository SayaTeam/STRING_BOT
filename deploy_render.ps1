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
        @{ key = "PYTHON_VERSION"; value = "3.11.9" },
        @{ key = "API_ID"; value = "33591348" },
        @{ key = "API_HASH"; value = "d138b2ec1432ef7da497e8e3d451140b" },
        @{ key = "BOT_TOKEN"; value = "8998263670:AAEqBPWcl0yL15IR5oqSvoohlVoUGvxlzt8" },
        @{ key = "OWNER_ID"; value = "5940554521" },
        @{ key = "MONGO_DB_URI"; value = "mongodb+srv://shnwazdeveloperx:shnwazdev@shnwazdev.sqmwbgl.mongodb.net/?appName=shnwazdev" },
        @{ key = "MUST_JOIN"; value = "C4Botz" }
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
