#ifndef ACCELERATIONMODULE_H
#define ACCELERATIONMODULE_H

#include "mbed.h"

class AccelerationModule {
public:
    AccelerationModule(PinName mosi, PinName miso, PinName sclk, PinName cs);
    void initialise();
    void readAcceleration(float& x, float& y, float& z);

private:
    SPI ADXL345;
    DigitalOut ADXL345_cs;
    char buffer[6];
    int16_t data[3];
};

#endif // ACCELERATIONMODULE_H