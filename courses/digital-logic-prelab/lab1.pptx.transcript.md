# lab1

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

Digital Logic Design and Application

Lab Course 1

Lecturer:

TA:

Lab Room:                         

## Slide 2

Fundamental

Digital Logic + Computer Architecture

Verilog Language

Tools 

 EDA software:  Vivado 2017.1

 Evaluation board:  EES331

Lab report submitted

 请大家注意，实验报告提交给数电理论课程的助教，各自教学班级收相应的报告即可，提交格式如 lab1-学号-姓名

## Slide 3

Grading

Assessment

 Lab1 10% + Lab2 20% + Lab3 20% + Lab4 20% + Lab5 10% + Report1 5% + Repor2 15%

And for each lab:

Pre-Lab preparation and Performance in laboratory (65%)

Laboratory experimental reports (35%)

## Slide 4

Reference

IEEE Standard Verilog Language Reference Manual

Vivado Introduction Using Verilog Design

EES331 User manual  （Zynq Book）

Codes for Students

## Slide 5

Content

EDA tools

Familiar the development environment

Coding, Synthesis and simulation

Compose testbench and do verification

Datapath Design 

Controller Design

CPU Integration

CPU Verification and Improvement

## Slide 6

Traditional method  VS  Programmable logic device

Implement for a 3-8 Decoder 

## Slide 7

Note

Please save the screenshots of the code, simulation result, etc.

You will need them to write the Lab_report.

## Slide 8

FPGA Design Flow

## Slide 9

2024/3/26

module decoder(A,B,C,Y); 

input A,B,C;

output reg [7:0] Y;

always@(*)

begin

	case({A,B,C})

	3'b000:Y=8'b0000_0001;

	3'b001:Y=8'b0000_0010;

	3'b010:Y=8'b0000_0100;

	3'b011:Y=8'b0000_1000;

	3'b100:Y=8'b0001_0000;

	3'b101:Y=8'b0010_0000;

	3'b110:Y=8'b0100_0000;

	3'b111:Y=8'b1000_0000;

	default: Y=8'd0000_0000;

	endcase

end

endmodule

module decoder(A,B,C,D,Y); 

input A,B,C,D;

output reg [15:0] Y;

always@(*)

begin

   case({A,B,C,D})

   4'b0000:Y=16'b0000000000000001;

   4'b0001:Y=16'b0000000000000010;

	......

   4'b1111:Y=16'b1000000000000000;

   default: Y=16'b0000000000000000;

   endcase

end

endmodule

Coding

## Slide 10

2024/3/26

Test Bench

A

B

C

Waveform

Simulation

begin

A=0;B=0;C=0;

#10 A=0;B=0;C=1;

#10 A=0;B=1;C=0;

#10 A=0;B=1;C=1;

#10 A=1;B=0;C=0;

#10 A=1;B=0;C=1;

#10 A=1;B=1;C=0;

#10 A=1;B=1;C=1;

#30 $stop;

end

## Slide 11

Hardware verify

## Slide 12

FPGA Design Flow

## Slide 13

1. Create New Hardware Project-step1

2. Click here

1. Open VIVADO 2017.1

→

## Slide 14

Click here

1. Create New Hardware Project-step2

## Slide 15

1. Rename new project，select the save path for project

2. Click here

1. Create New Hardware Project-step3

## Slide 16

1. Select RTL Project

1. Create New Hardware Project-step4

2. Click here

## Slide 17

 Directly Click here. 

Don’t add any other files.

1. Create New Hardware Project-step5

## Slide 18

 Directly Click here. 

Don’t add any other files.

1. Create New Hardware Project-step6

## Slide 19

1.  Select xc7z020clg484-1 as the following part

2. Click here

1. Create New Hardware Project-step7

## Slide 20

Check  the project  information，then click here

1. Create New Hardware Project-step8

## Slide 21

After finished,  you can see this window 

1. Create New Hardware Project-step9

Source Menu

Simulation Menu

Synthesis Menu

Hardware Program Menu

## Slide 22

FPGA Design Flow

## Slide 23

1. Right-click

2. Click here

2. Create New Source File-step1

## Slide 24

2. Create New Source File-step2

 2. Click here

1.Choose it

## Slide 25

Click here

2. Create New Source File-step3

## Slide 26

1. Add file name

2. Create New Source File-step4

 2. Click here

## Slide 27

2. Create New Source File-step5

Click here

## Slide 28

2. Create New Source File-step6

 2. Click here

1. Add module name

## Slide 29

2. Create New Source File-step7

Click here

## Slide 30

Double click

Add your Verilog here.

The input and output can refer to the next page.

2. Create New Source File-step8

## Slide 31

3-8 decoder

module decoder(A,B,C,Y); 

input A,B,C;

output reg [7:0] Y;

always@(*)

begin

       xxxxxx

       xxxxxx

end

endmodule

2. Create New Source File-step9

## Slide 32

FPGA Design Flow

## Slide 33

3. Do Synthesis and get the circuit -step1

Click here

## Slide 34

3. Do Synthesis and get the circuit -step1

Click here

## Slide 35

3. Do Synthesis and get the circuit –step2

After finishing, you can see 

this window 

2.Click here

1.Choose it

## Slide 36

3. Do Synthesis and get the circuit –step3

2.Click here

1.Click here

## Slide 37

3. Do Synthesis and get the circuit –step4

your circuit based the Verilog code

## Slide 38

FPGA Design Flow

## Slide 39

4. Create Simulation Source

File-step1

1. Right-click

2. Click here

## Slide 40

4. Create Simulation Source

File-step2

2. Click here

1.Choose it

## Slide 41

Click here

4. Create Simulation Source

File-step3

## Slide 42

1. Add file name

4. Create Simulation Source

File-step4

 2. Click here

## Slide 43

Click here

4. Create Simulation Source

File-step5

## Slide 44

 2. Click here

1. Add module name

4. Create Simulation Source

File-step6

## Slide 45

Click here

4. Create Simulation Source

File-step7

## Slide 46

2. Copy  the  content in tb_decoder.txt  to this window, and complete the code

4. Create Simulation Source

File-step8

1. Double click

## Slide 47

4. Create Simulation Source

File-step9

1.Right- click

2.Click

## Slide 48

1. Click here

2. Click here

4. Create Simulation Source

File-step10

## Slide 49

Observe the variation of signals. Make sure all of these are  right.

5.  Do the simulation and debug. 

Click here to zoom the window

Click here to see bit 0~7

## Slide 50

FPGA Design Flow

## Slide 51

51

1. Right-click

2. Click here

6. Create Constraint Source

File-step1

## Slide 52

52

6. Create Constraint Source

File-step2

2. Click here

1.Choose it

## Slide 53

53

6. Create Constraint Source

File-step3

Click here

## Slide 54

54

1. Add file name

 2. Click here

6. Create Constraint Source

File-step4

## Slide 55

55

6. Create Constraint Source

File-step5

Click here

## Slide 56

1. Double click

2. Copy  the  content in PINS_SET.txt  to this window

6. Create Constraint Source

File-step6

## Slide 57

Click here

7. Generate Bitstream

File for FPGA

-step1

## Slide 58

7. Generate Bitstream

File for FPGA

-step2

Click here

## Slide 59

You can see

 on the top right corner. 

After finishing, you can see this window 

7. Generate Bitstream

File for FPGA

-step3

2.Click here

1.Choose this

## Slide 60

8.Connect  FPGA Target Board With Computer

1. Put all  switch(17 ) to ON

2.Connect J3(2) and USB port of computer with USB cable 

3.  Power on with switch (7)

## Slide 61

2. Right-click

3. Click here

1. Click here

9. Program device

-step1

## Slide 62

8. Program device

-step2

Click here

## Slide 63

Find you bit file

8. Program device

-step3

Click here

## Slide 64

1. Switch(0,1,2) are the inputs (A,B,C), led(0~7) are the  outputs (Y0~Y7)

2. Use the switch to control the led light 

9. Observe phenomena

## Slide 65

Appendix:        implement and verify a ledwater

## Slide 66

Digital Logic Design and Application

Lab Course 1

~~End~~