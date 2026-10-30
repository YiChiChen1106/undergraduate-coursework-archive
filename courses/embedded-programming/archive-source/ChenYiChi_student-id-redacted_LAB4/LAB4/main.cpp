#include "mbed.h"


#define I2CSDA D0
#define I2CSDL D1

DigitalIn switch_ip1(D5, PullDown);

I2C TMP102(I2CSDA,I2CSDL);

const int TMP102Address = 0x90;// TMP102 address
char ConfigRegisterTMP102[3];//config register
char TemperatureRegister[2];//Temperanture Register
float Temperature;

void ConfigureTMP102()
{
    ConfigRegisterTMP102[0] = 0x01;
    ConfigRegisterTMP102[1] = 0x60;
    ConfigRegisterTMP102[2] = 0xA0;
    TMP102.write(TMP102Address, ConfigRegisterTMP102,3);//write 3 bytes
}

// main() runs in its own thread in the OS
int main(){

    unsigned short M;
    char L;
    ConfigureTMP102();
    ConfigRegisterTMP102[0] = 0x00;
    TMP102.write(TMP102Address, ConfigRegisterTMP102,1);
    printf("Initiating temperature..\n\r");

    while(1){
        float sum=0;
        
        if (switch_ip1 == 1)
        {
            ThisThread::sleep_for(20ms);   //按键防抖
            if (switch_ip1 == 1)           
            {
                TMP102.read(TMP102Address, TemperatureRegister,2);//read 2 bytes
                M = TemperatureRegister[0]<<4;
                L = TemperatureRegister[1]>>4;
                M = M + L;
                Temperature = 0.0625*M;
                printf("Temperature = %.3f\n\r",Temperature);
            }
            ThisThread::sleep_for(2000ms);   //按键防抖
        }
        
     
    }
}