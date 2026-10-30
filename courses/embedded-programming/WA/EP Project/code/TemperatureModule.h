#ifndef TemperatureModule_H
#define TemperatureModule_H

#include "mbed.h"

class TemperatureModule {
public:
    TemperatureModule(PinName sda, PinName scl);
    void configure();
    float readTemperature();
    I2C i2c;
    
private:
    
    char tmp102Address;
    char configRegister[3];
    char tempRegister[2];
};

#endif