
const int relay = 2;

int duracion = 0;


void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(relay, OUTPUT);
    digitalWrite(relay, LOW);
    Serial.begin(9600);
}

void loop() {
    comunicate();
    if (duracion > 0) {
        digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(relay, HIGH);
        duracion -= 1;
        }
    else { digitalWrite(LED_BUILTIN, LOW); digitalWrite(relay, LOW); }
    delay(1000);
}

void comunicate(){
    if(Serial.available() > 0){
        String str = Serial.readStringUntil(char('\0'));
        int i = str.toInt();
        if (i != duracion) { duracion = i; }
    }
}
