const int sensorPin = A0; // Pin analógico para el movimiento lateral
const int buttonPin = 2;  // Pin digital para el botón

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP); // Configura el botón con resistencia pull-up interna
}

void loop() {
  int sensorValue = analogRead(sensorPin); // Lee el valor del sensor
  int buttonState = digitalRead(buttonPin); // Lee el estado del botón

  // Mapea el valor del sensor a un rango adecuado para el juego
  int movement = map(sensorValue, 0, 1023, -10, 10);

  // Envía los datos al juego por el puerto serial
  Serial.print(movement);
  Serial.print(",");
  Serial.println(buttonState);

  delay(10); // Espera un poco antes de la siguiente lectura
}