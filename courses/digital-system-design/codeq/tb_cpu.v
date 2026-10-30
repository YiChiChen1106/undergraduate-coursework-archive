`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/04/01 17:09:45
// Design Name: 
// Module Name: tb_cpu
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module tb_cpu();
reg         clk,rst,en_ram_out;
reg  [15:0] ins;
wire        en_ram_in;
wire [15:0] addr;

cpu test_cpu(
    .clk (clk),
    .rst (rst),
    .addr (addr),
    .ins (ins),
    .en_ram_in (en_ram_in), 
    .en_ram_out (en_ram_out)     	
);
parameter Tclk = 10;

initial begin
         clk=0;
          forever #(Tclk/2) clk=~clk;
end                      
initial begin
                                     rst=0;
#(Tclk*4)        rst=1; 
end	
initial begin
       en_ram_out=1;
end

initial begin
	                    ins = 16'b0000_0000_0000_0000;//before 50ns, give an empty instruction, wating for "rst"// addr = 0
        #(Tclk*5)       ins = 16'b0000_0000_0000_1000;//MOV  R0 #08 
        #(Tclk*5)       ins = 16'b0000_0100_0000_0010;//MOV  R1 #02
        #(Tclk*5)       ins = 16'b0010_0100_0000_0001;//ADD  R1 #01
        #(Tclk*5)       ins = 16'b0101_0001_0000_0000;//SUB   R0 R1
        #(Tclk*5)       ins = 16'b1001_0001_0000_0000;//OR    R0 R1
        #(Tclk*5)       ins = 16'b0010_0000_0000_0001;//ADD  R0 #01
        #(Tclk*5)       ins = 16'b1010_0000_0000_0111;//Jump addr = 8'd7
        
        #(Tclk*10)      $stop;
        end    
endmodule
