/*
  Blink at random interval

  Turns an LED on for 100 ms, then off for random period, repeatedly.
  This example code is in the public domain.
*/

int count = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(20000);
}

// the loop function runs over and over again forever
void loop() {
  if (count < 1000) {
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off (LOW is the voltage level)
    delay(100);                        // wait for a bit
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on by making the voltage HIGH
    delay(random(250,500));            // wait for a random bit
    count += 1;
  }
}
