#include "include/BuzzerModule.h"
#include "mbed.h"


BuzzerModule::BuzzerModule(PinName pwm) : buzzer(pwm) {}

void BuzzerModule::alarm(const float frequency[], const float beat[], int size) {
      for(int i=0;i<=27;i++){
        //Change PWM's period to change the frequency of the music
        buzzer.period(1/(2*frequency[i]));
        //duty cycle
        buzzer=0.5;
        //time interruption for beat
        wait_us(1000000*0.4*beat[i]);
    }
}