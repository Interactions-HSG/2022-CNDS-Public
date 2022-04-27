# --- GLOBAL VARIABLES --------------------------

VER  = "FS-2022"

# --- TTN VARIABLES --------------------------
User = "myopia-sensor-testing@ttn"
Password = "NNSXS.J63AMJ5UHGLUQBXO5UC7EN7ZO6CWNTOYWWMG77A.LOKF6OJEBC6YGFM77BOWC52PJVKSDLK3N7QKFLKAE67AOREJ55AA"
theRegion = "EU1"
TTN_URL = theRegion.lower() + ".cloud.thethings.network"
MQTT_TOPIC = "#"

# --- LORA CLOUD VARIABLES --------------------------
DMS_APITOKEN = "AQEAfRVPAahZ4jHx81hZC7keEOzcabw6gZpfYlFbyMJFwf9TdSWF"
DMS_HOST     = "https://mgs.loracloud.com"
DMS_PORT     = 199
DMSAPI_UPLINK_SEND = {
    'method' : 'POST',
    'url'    : f"{DMS_HOST}/api/v1/uplink/send"
}

# APP Constants
WIFI_PACKET_TYPE = "08"
ACC_PACKET_TYPE = "09"

