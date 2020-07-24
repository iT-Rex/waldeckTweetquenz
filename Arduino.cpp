#include <Arduino.h>

#define PIN_LEDSTRIP 5
#define DIM_INTERVAL 1500
#define DIM_STEP 1
#define MAX_INTENSITY 255
#define MIN_INTENSITY 2

/*
 * Connect the Gate of a MOSFET through around 200 Ohm to PIN_LEDSTRIP (make sure that this pin is PWM-capable!)
 * Connect the Source of the MOSFET to GND
 * Put around 10k Ohm between the Gate and the Source
 * Connect your LED-strip to the Drain of the MOSFET and a sufficiently powerful powersupply
 * Connect the powersupply GND to one of the Arduino's GND pins
 * Connect the Arduino (via USB) to a computer running the TwitterPrinter script
 */

String millisToTimeString(unsigned long p_nMillis)
{
  String sResult = "";

  unsigned long nRemainingSeconds = p_nMillis / 1000;
  byte nSeconds = nRemainingSeconds % 60;
  nRemainingSeconds /= 60;
  byte nMinutes = nRemainingSeconds % 60;
  nRemainingSeconds /= 60;
  byte nHours = nRemainingSeconds % 24;

  if (nHours > 0) sResult += String(nHours) +":";
  if (nMinutes < 10 && nHours > 0) sResult += "0";
  if (nMinutes > 0) sResult += String(nMinutes) +":";
  if (nSeconds < 10 && nMinutes > 0) sResult += "0";
  sResult += String(nSeconds);
  return sResult;
} // String millisToTimeString


void setup() {
  Serial.begin(38400);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PIN_LEDSTRIP, OUTPUT);
  analogWrite(PIN_LEDSTRIP, 255);

  Serial.println("TwitterPrinterGlitterSquinter v1.0 - Analphabetic Anteater");
  Serial.print("Dimming by ");
  Serial.print(DIM_STEP);
  Serial.print(" every ");
  Serial.print(DIM_INTERVAL);
  Serial.print(" milliseconds, until brightness ");
  Serial.print(MIN_INTENSITY);
  Serial.println(" is reached.");
  Serial.print("Dimming fully will take approx. ");
  float fArduinoCHasStupidOverflows;
  fArduinoCHasStupidOverflows = DIM_INTERVAL;
  fArduinoCHasStupidOverflows *= (255 - MIN_INTENSITY);
  fArduinoCHasStupidOverflows /= DIM_STEP;
  Serial.println(millisToTimeString(fArduinoCHasStupidOverflows));
} // void setup

void loop() {
  static int s_nIntensity = MAX_INTENSITY;
  static unsigned long s_fLastTime = millis();

  digitalWrite(LED_BUILTIN, LOW);

  if (Serial.available() > 0) {
    s_nIntensity = MAX_INTENSITY;
    s_fLastTime = millis();
    while (Serial.available()) Serial.read(); // flush the serial buffer
    Serial.println("Twat!");
  } // if

  if (millis() - s_fLastTime > DIM_INTERVAL) {
    if (s_nIntensity > MIN_INTENSITY) {
      s_nIntensity -= DIM_STEP;
      if (s_nIntensity < MIN_INTENSITY) s_nIntensity = MIN_INTENSITY;
      s_fLastTime = millis();
      digitalWrite(LED_BUILTIN, HIGH);
    } // if
  } // if

  analogWrite(PIN_LEDSTRIP, s_nIntensity);

  delay(50);
} // void loop
