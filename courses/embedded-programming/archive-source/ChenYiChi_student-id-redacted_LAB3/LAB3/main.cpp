#include <mbed.h>
#include "BufferedSerial.h"
#include <cstdio>  // 输入输出头文件

#define WATING_TIME 500ms


#define SCLK A4  
#define MISO A5  
#define MOSI A6  
#define CS D12  
#define LXG1 D11 
#define LXG2 D9 
#define LXR1 D0  
#define LXR2 D1  
#define LYG1 D6  
#define LYG2 A3  
#define LYR1 A2  
#define LYR2 A0  

// 初始化SPI和其他外设对象
SPI ADXL(MOSI, MISO, SCLK);           
//Serial pc(USBTX, USBRX);
DigitalOut chip_sel(CS);           // 创建数字输出对象用于控制SPI通信的片选信号

DigitalOut lxg1(LXG1);
DigitalOut lxg2(LXG2);
DigitalOut lxr1(LXR1);
DigitalOut lxr2(LXR2);
DigitalOut lyg1(LYG1);
DigitalOut lyg2(LYG2);
DigitalOut lyr1(LYR1);
DigitalOut lyr2(LYR2);

// 加速度计初始化函数
void initialise() { 
    chip_sel = 1; 
    ADXL.format(8, 3); // 设置SPI通信格式，8位数据长度，模式3
    ADXL.frequency(2000000); // 设置SPI频率为2MHz
    chip_sel = 0; 
    ADXL.write(0x31); // 选择DATA_FORMAT寄存器
    ADXL.write(0x03); // 配置寄存器：4线SPI, 10位模式, 数据右对齐, 量程±16g
    chip_sel = 1; 
    chip_sel = 0; 
    ADXL.write(0x2D); // 选择POWER_CTRL寄存器
    ADXL.write(0x08); // 配置寄存器：进入测量模式
    chip_sel = 1; 
}

// 主函数
int main() { 
    char buffer[6]; // 存储加速度计数据的缓冲区
    int16_t combine_data[3]; // 存储合成的加速度数据
    float x_axis, y_axis, z_axis; // 存储转换为g单位的加速度数据
    initialise(); // 初始化加速度计
    while(1) { 
        ThisThread::sleep_for (WATING_TIME); // 等待0.5秒
        chip_sel = 0; 
        ADXL.write(0xF2); // 发送读取命令，从第一个数据寄存器开始
        for(int i = 0; i < 5; i++) { 
            buffer[i] = ADXL.write(0x00); // 读取数据并存储在缓冲区
        }
        chip_sel = 1; 

        // 合成16位的加速度数据
        combine_data[0] = buffer[1] << 8 | buffer[0];
        combine_data[1] = buffer[3] << 8 | buffer[2];
        combine_data[2] = buffer[5] << 8 | buffer[4];

        // 转换为g单位的加速度
        x_axis = 0.016 * combine_data[0];
        y_axis = 0.016 * combine_data[1];
        z_axis = 0.016 * combine_data[2];
printf("x = %+1.2fg\t y = %+1.2fg\t z = %+1.2fg\n\r", x_axis, y_axis, z_axis);
        // 根据x轴的加速度控制LED
         if(x_axis > 0.5 && y_axis > 0.5) {
            // 例如: 同时向右和向上倾斜
            lxg1 = 1; lyr1 = 1;
            lxr1 = lxr2 = lxg2 = lyr2 = lyg1 = lyg2 = 0;
        } else if(x_axis < -0.5 && y_axis < -0.5) {
            // 例如: 同时向左和向下倾斜
            lxr2 = 1; lyr2 = 1;
            lxr1 = lxg1 = lxg2 = lyr1 = lyg1 = lyg2 = 0;
        } else if(x_axis > 0.5 && y_axis < -0.5) {
            // 例如: 向右倾斜且向下倾斜
            lxg1 = 1; lyr2 = 1;
            lxr1 = lxr2 = lxg2 = lyr1 = lyg1 = lyg2 = 0;
        } else if(x_axis < -0.5 && y_axis > 0.5) {
            // 例如: 向左倾斜且向上倾斜
            lxr2 = 1; lyr1 = 1;
            lxr1 = lxg1 = lxg2 = lyr2 = lyg1 = lyg2 = 0;
        } else {
            // 默认情况下关闭所有LED
            lxr1 = lxr2 = lxg1 = lxg2 = lyr1 = lyr2 = lyg1 = lyg2 = 0;
        }
        
    }
}