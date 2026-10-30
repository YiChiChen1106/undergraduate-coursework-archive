# Lab5

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

## Slide 1

Digital Logic Design and Application

Lab Course 5

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

   e-file name:  report no. + student code + name  (eg: 1_20xxxxxx_Alex)

   send to email: same as the homework

   cut-off time: report1 : before lab3 （before 14, May）

                       report2 : 1 week after lab5（before 10, May ）

## Slide 3

Grading

Assessment

 Lab1 10% + Lab2 20% + Lab3 20% + Lab4 20% + Lab5 10% + Report1 5% + Repor2 15%

And for each lab:

Pre-Lab preparation and Performance in laboratory (65%)

Laboratory experimental reports (35%)

## Slide 4

Note

Please save the screenshots of the code, simulation result, etc.

You will need them to write the Lab_report.

## Slide 5

Content

EDA tools

Datapath Design 

Controller Design

CPU Integration

CPU Verification and Improvement

Enlarge your own instruction set (for example: add several instructions) and modify the datapath & controller modules based on the new instruction set

Compose a  better testbench and do verification again

Describe your work as clearly as possible in your lab report2

## Slide 6

Instruction Set

Opcode

Rd

Rs

Imme

assembly

function

4bit

2bit

2bit

8bit

0000

0001

01

10

xx

01

00000010

xxxxxxxx

Mov R1 #02

Mov R2 R1

R1<= 2

R2<=(R1)

0010

0011

01

01

xx

10

 00001000 

xxxxxxxx

Add R1 #08

Add R1 R2

R1<=(R1)+8

R1<=(R1)+(R2)

0101

01

10

xxxxxxxx

Sub R1 R2

R1<=(R1)-(R2)

0110

0111

11

01

xx

10

00000011

xxxxxxxx

And R1 #03

And R1 R2

R3<= (R3) bit_and (3)

R1<= (R1) bit_and (R2)

1001

01

10

xxxxxxxx

Or R1 R2

R1<=(R1) bit_or (R2)

1010

xx

xx

00000001

       Jump #01

                PC<= 1

Opcode supports 16 instructions. So you can add other instructions, like shift, multiplication.

Rd and Rs can be expressed in 2 bits that means you can operate 4 registers.

Immediate data is expressed in 8 bits.

## Slide 7

1. Create New Hardware Project

Follow the steps of lab1.ppt to create New Hardware Project. 

## Slide 8

2. Create New Source File-step1

Follow the steps of lab4.ppt to create files  in the code folder like this 

## Slide 9

2. Create New Source File-step2

Refer to the next page to combine cpu and rom in top_cpu.v

## Slide 10

2. Create New Source File-step3

CPU

ROM

clk

rst

16

ins

en_ram_out

addr

16

en_ram_in

system_top

## Slide 11

2. Create New Source File-step4

A ROM (Read-only memory), with instructions editable in design phase.

Design your program according to the equation below. 

Be aware that data exceeding the defined address is unknown.

[8-(2+1) ]|(2+1)+1

## Slide 12

3. Create the ILA IP core (Integrated  Logic Analyser)

## Slide 13

3. Create the ILA IP core 

Step-1

1. Left-click

## Slide 14

3. Create the ILA IP core 

Step-2

1. Left-click

1. Input name to search IP cores

2. Double click

## Slide 15

3. ADD 

IP CORE

-step2-2

1. Module’s name

2. Input parameter

## Slide 16

3. ADD 

IP CORE

-step2-3

1. Input parameter

## Slide 17

3. ADD 

IP CORE

-step2-4

1. Left click

## Slide 18

3. ADD 

IP CORE

-step2-5

Ensure these signals are connected to probes.

We need to pay attention to the signals q0, q1, q2, and q3.

reg_group

## Slide 19

3. Do Synthesis and get the circuit 

Follow the steps of lab1.ppt to do Synthesis and get the circuit 

## Slide 20

Add tb_top_cpu.v  to the project as simulation source

4. Create Simulation Source

File

Define clk

Define rst

## Slide 21

5.  Create the constraint

Copy contents in PINS_SET.txt to this window

## Slide 22

6.Connect  FPGA Target Board With Computer

1. Put all  switch(17 ) to ON

2.Connect J3(2) and USB port of computer with USB cable 

3.Power on with switch (7)

4.system reset  L18(13)

## Slide 23

7. program device

Follow the steps of lab1.ppt

## Slide 24

8. Run ila to see the data in the registers

-step1

2. Add signals

1. Select the ila

3. Select all

4. Click ok

## Slide 25

8. Run ila to see the data in the registers

-step2

2

1

3

Add Trigger Signal 

## Slide 26

9. Run ila to see the data in the registers

-step3

1. Set Trigger Condition 

3.Start Trigger

2.Press and hold the reset button on the board !!!!!!

4.Release the reset button!!!!!!

## Slide 27

Some other ideas for Instruction Set

Memory access instructions

                 Ldr, Str

Conditional branch instructions

                 Jz, Jnc, …

Other data operation instructions

 Xor, Cmp…..

 Acc (add 1 to N)

## Slide 28

Digital Logic Design and Application

Lab Course 5

~~End~~