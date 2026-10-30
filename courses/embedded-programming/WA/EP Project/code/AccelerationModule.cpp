
#include "include/AccelerationModule.h"

AccelerationModule::AccelerationModule(PinName mosi, PinName miso, PinName sclk, PinName cs)
    : ADXL345(mosi, miso, sclk), ADXL345_cs(cs) {}

void AccelerationModule::initialise() {
  ADXL345_cs=1;
    ADXL345.format(8,3);
    ADXL345.frequency(2000000);
    ADXL345_cs=0;
    ADXL345.write(0x31);
    ADXL345.write(0x0B);
    ADXL345_cs=1;
    ADXL345_cs=0;
    ADXL345.write(0x2D);
    ADXL345.write(0x08);
    ADXL345_cs=1; 

}

void AccelerationModule::readAcceleration(float& x, float& y, float& z) {
        ADXL345_cs=0;
    ADXL345.write(0x80|0x40|0x32);
    for(int i=0; i<5; i++){
        buffer[i] = ADXL345.write(0x00);
    } 
    ADXL345_cs = 1;
    data[0] = buffer[1]<<8 | buffer[0];
    data[1] = buffer[3]<<8 | buffer[2];
    data[2] = buffer[5]<<8 | buffer[4];
    x=0.004*data[0];
    y=0.004*data[1];
    z=0.004*data[2];
    printf("x=%f\n",x);
     printf("y=%f\n",y);
      printf("z=%f\n",z);
}