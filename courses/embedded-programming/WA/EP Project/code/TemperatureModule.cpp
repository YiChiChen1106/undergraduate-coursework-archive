#include "include/TemperatureModule.h"

TemperatureModule::TemperatureModule(PinName sda, PinName scl) : i2c(sda, scl), tmp102Address(0x48) {}

void TemperatureModule::configure() {
    configRegister[0] = 0x01;
    configRegister[1] = 0x60;
    configRegister[2] = 0xA0;
    i2c.write(tmp102Address << 1, configRegister, 3);
}

float TemperatureModule::readTemperature() {
    char tempRegAddr = 0x00;
    i2c.write(tmp102Address << 1, &tempRegAddr, 1);
    i2c.read(tmp102Address << 1, tempRegister, 2);
    
    unsigned short M = tempRegister[0] << 4;
    char L = tempRegister[1] >> 4;
    float temperature = (M + L) * 0.0625;
    printf("temperature%2f\n",temperature);
    return temperature;
}