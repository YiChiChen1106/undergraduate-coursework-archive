#ifndef BUZZERMODULE_H
#define BUZZERMODULE_H

#include "mbed.h"

class BuzzerModule {
public:
    BuzzerModule(PinName pwm);
    void alarm(const float frequency[], const float beat[], int size);

private:
    PwmOut buzzer;
};

#endif // BUZZERMODULE_H