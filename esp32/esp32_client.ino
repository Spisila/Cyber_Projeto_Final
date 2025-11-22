#include <WiFi.h>

const char* WIFI_SSID = "nome_wifi";
const char* WIFI_PASS = "senha_wifi";

const char* SERVER_IP = "192.168.15.4";
const uint16_t SERVER_PORT = 5000;

WiFiClient client;
unsigned long lastSend = 0;
const int LED_PIN = 2;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  Serial.print("Conectando ao WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nWiFi conectado!");

  conectarServidor();
}

void conectarServidor() {
  Serial.println("Conectando ao servidor...");
  while (!client.connect(SERVER_IP, SERVER_PORT)) {
    Serial.println("Falha, tentando de novo...");
    delay(1000);
  }
  Serial.println("Conectado ao servidor!");
}

void enviarJSON() {
  float temp = random(200, 300) / 10.0;
  float hum  = random(400, 800) / 10.0;

  String json = "{\"type\":\"data\",\"from\":\"esp32\",\"payload\":{\"temp\":";
  json += temp;
  json += ",\"hum\":";
  json += hum;
  json += "}}";

  client.println(json);
  Serial.println("Enviado: " + json);
}

void tratarComando(String cmd) {
  cmd.trim();

  int pos = cmd.indexOf(':');
  if (pos != -1) {
    cmd = cmd.substring(pos + 1);
    cmd.trim();
  }

  Serial.println("Comando limpo: " + cmd);

  if (cmd == "led_on") {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED ligado");
  }
  else if (cmd == "led_off") {
    digitalWrite(LED_PIN, LOW);
    Serial.println("LED desligado");
  }
}

void loop() {
  if (!client.connected()) {
    Serial.println("Reconectando...");
    conectarServidor();
  }

  if (client.available()) {
    String cmd = client.readStringUntil('\n');
    tratarComando(cmd);
  }

  if (millis() - lastSend > 2000) {
    enviarJSON();
    lastSend = millis();
  }
}
