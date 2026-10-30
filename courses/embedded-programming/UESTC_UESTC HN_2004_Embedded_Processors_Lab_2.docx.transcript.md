# UESTC_UESTC HN_2004_Embedded_Processors_Lab_2

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

1

Lab 2 – Peripherals Programming on mbed Part 1: Interfacing Using GPIO and SPI Pins

Embedded Processors UESTC2004 & UESTCHN2004 School of Engineering, University of Glasgow

Student Name:

Student Number:

UESTC 2004 Lab Assessment Criteria

Each individual lab will be evaluated using the below criteria:

Demonstrating a functional embedded system – 50%

This means each student will need to demonstrate a functional system for each task in the lab manual to the GTA and member of staff to get the full mark.

Lab Questions – 10%

Reflection and significance – 25%

After the completion of programming and testing each of the “Tasks”, you will be required to reflect, in a few lines, on your understanding of the tasks and its significance. This is a chance for you to ask yourselves “What you did?”, “What it means?”, and “What next?”, meaning what is the significance of the undertaken task in the context of embedded systems and what you are learning in the lecture. Try to be innovative and think outside the box. Please, do not provide a summary of what you did as it will not be accepted.

Adherence to coding good practice – 15%

Meaningful variable names – please avoid names like “x”, “y”, or personal names

Using block comments to explain what your code does at the beginning and using line comments to clarify what this line of code does.

Consistent indentation – Indentation helps in making the code readable and easy to interpret. See an example of what to do and what to avoid, below:

Good practice 

#include “mbed.h” char switch_word ;//the word we will send//the word we will send

//the word we will send

//the word we will send

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

2

char recd_val; int main() {//the received value//the received value//set baud rate to 9600//set baud rate to 9600

//the received value

//the received value

//set baud rate to 9600

//set baud rate to 9600

async_port.baud(9600); recd_val = 0; while (1) {

switch_word=0xa0;

} }

Avoid this ✘

#include “mbed.h” char switch_word ; char recd_val;//the word we will send //the received value//set baud rate to 9600//the word we will send //the received value//set baud rate to 9600

//the word we will send //the received value

//set baud rate to 9600

//the word we will send //the received value

//set baud rate to 9600

int main() { async_port.baud(9600); recd_val = 0; while (1) { switch_word=0xa0; } }

All the best of luck.

The Embedded Processors Team,

Lab Objective

The objective of this lab is to implement the fundamental concepts of interfacing different input/output devices with an embedded processor and to get you think about software and hardware design aspects that can make your system more efficient. Specifically, the lab aims to achieve the following objectives:

Develop a push button (non-locking switch) controlled up/down counter and a 7- segment display, and learn how to display numeric data on one.

Perform loopback communication using the Serial Peripheral Interface (SPI) protocol and understand the basic concept of synchronous serial communication.

Requirements

Software:

Keil arm online compiler (https://studio.keil.arm.com/auth/login/) – You will need to create an account to use the online compiler.

Hardware:

For this lab, the following components will be needed:

One breadboard

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

3

One Nucleo L432KC mbed board and USB programming cable

Resistors (As appropriate for current limiting resistors and pull-up/down resistor)

1 x 7-segment display

2 x push-button (non-locking switches)

One LED

Wires

Task 1: 7-Segment Display Counter with Push Button Control

Objective:

Design and implement an embedded system using the Nucleo L432KC board and Mbed that allows users to increment and decrement a counter displayed on a 7-segment display using two push buttons.

Task 1.1: Produce a table in your lab book like that below which shows the hexadecimal number you will write to the MCU pins to generate the display values 0-9.

Display

Value

0

1

2

3

4

5

6

7

8

9

Segment drive in binary

00111111

00000110

01011011

01001111

01100110

01101101

01111101

00000111

01111111

01101111

Segment drive in hexadecimal

0xBF

0x06

0x5B

0x4F

0x66

0x6D

0x7D

0x67

0x7F

0x6F

[Use the below space to show how you workout the hexadecimal values corresponding to each digit]

Task 1.2: Is your 7-segment display common-anode or common-cathode? And What difference does this make to your design?

[Answer in the below space]

Common cathode

When using common cathode. I use high level as input. Otherwise, the low level is input. 

Task 1.3: Write your C program on the online compiler and download it to the Nucleo board to test it. More information on how to compile your code online and download it to

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

4

the board can be found here: https://os.mbed.com/docs/mbed-os/v6.15/quick-start/build-with-the-online-compiler.html

#include "mbed.h"

#define Blinking_time 500ms

BusOut display(D12, D3, D4, D5, D6, D9, D10, D11);

// main() runs in its own thread in the OS

DigitalIn jia(D2, PullUp);

DigitalIn jian(D13, PullUp);

int main()

{

    static int i = 0;

    while (true) {

        if (jia.read() == 1) {

    i++;

        }

    if (jian.read() == 1) {

    i--;

    }

        if (i > 9) {

            i = 9;

        }

        if (i < 0) {

            i = 0;

        }

        switch (i) {

            case 0: display = 0x3F; break;

            case 1: display = 0x06; break;

            case 2: display = 0x5B; break;

            case 3: display = 0x4F; break;

            case 4: display = 0x66; break;

            case 5: display = 0x6D; break;

            case 6: display = 0x7D; break;

            case 7: display = 0x07; break;

            case 8: display = 0x7F; break;

            case 9: display = 0x6F; break;

                    }

    ThisThread::sleep_for(Blinking_time);

    }

}

Task 2: Serial peripheral interface master with loopback

The objective of this task is to write an SPI loopback code using mbed Nucleo L432KC board. The code should send a message "Hello World!" over SPI and then receive it back using the same SPI interface. The received message should be printed on the serial monitor.

Task 2.1: For the SPI protocol, draw a brief diagram to show the communication structure.

[Answer in the below space]

CSSCLKMOSIMISO                SLAVECSSCLKMOSIMISO                SLAVECSSCLKMOSIMISO     MASTERCSSCLKMOSIMISO     MASTER

CS

SCLK

MOSI

MISO

                SLAVE

CS

SCLK

MOSI

MISO

                SLAVE

CS

SCLK

MOSI

MISO

     MASTER

CS

SCLK

MOSI

MISO

     MASTER

Task 2.2: For SPI protocol, indicate which device can initialise and control the communication.

[Answer in the below space]

Master

Task 2.3: For SPI protocol, indicate how to choose a slave to communicate with. [Answer in the below space]

Use CS to confirm which slave is chosen

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

5

Task 2.4: Implementation

Please set the SPI object to the following pins:

SCLK

A4

MISO

A5

MOSI

A6

Connect/hardwire the MOSI pin to the MISO pin of your mbed, on the breadboard. This feeds the output of the SPI back into its input. Do not connect SCK to anything.

Configure the SPI for 8 bits of data and mode 0. This is the default but we may change it, as required.

Configure the SPI for a frequency of 1 MHz.

Display an introductory message “SPI Loopback Code Started!” once, on the serial terminal.

Send “Hello world!” through the SPI MOSI and receive it through the MISO to then be

displayed on the serial terminal as follows “Received Message is: Hello World!”.

Repeat the process every one second.

Test your code and debug any errors.

Show your code to the GTAs.

#include "mbed.h"

SPI spi(A6,A5,A4); // mosi, miso, sclk

DigitalOut cs(D10);

int main()

{

    printf("SPI Loopback Code Started!\n");

    while(1){

    const char tx[] = "Hello,World!";

    char rx[sizeof(tx)];

    spi.format(8, 0);

    spi.frequency(1000000);

    spi.write(tx,sizeof(tx),rx,sizeof(rx));

    printf("Receive Message is: %s\n", rx);

    thread_sleep_for(1000);

    }

}

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

6

Task 3: Reflection

After the completion of programming and testing of Tasks 1 and 2 please reflect, in a few lines, on your understanding of the tasks and its significance. This is a chance for you to ask yourselves “What you did?”, “What it means?”, “What next?”, and/or How else, more efficiently, can this be done?, meaning what is the significance of the undertaken task in the context of embedded systems and what you are learning in the lecture. Try to be innovative and think outside the box. Please, do not provide a summary of what you did as it will not be accepted.

[Answer in the below space]

Task1:I use seven-segment LED to demonstrate ten numbers .When press the adding button , the number displayed on the LED increase, When pressing another button, the number displayed on the LED decrease.

Task2:I use SPI technology to transport messsge between slave and master.

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

7

Lab Score

Marking Criteria

Student’s Score

Demonstration (60%) Task 1 (45%)

Task 2 (15%)

Lab Questions (20%) Task 2 (10%)

Task 3 (10%)

Reflection (5%)

Adherence to coding good practice (15%)

UESTC 2004: Embedded ProcessorsLab 2: GPIO/SPI InterfacingLab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing

Lab 2: GPIO/SPI Interfacing