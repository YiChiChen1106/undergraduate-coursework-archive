`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/04/01 15:33:22
// Design Name: 
// Module Name: tb_state_transition
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


`timescale 1ns / 1ps
module tb_state_transition();

reg clk,rst;
reg alu_end;
reg [1:0] rd;
reg [3:0] opcode;
wire en_fetch;
wire en_group;
wire en_pc;
wire [1:0] pc_ctrl;
wire [3:0] reg_en;
wire alu_in_sel;
wire [2:0] alu_func;

state_transition state_transition1(
					.clk(clk) ,
					.rst(rst) ,
					.alu_end(alu_end) ,
					.rd(rd) ,
					.opcode(opcode)  ,
					.en_fetch(en_fetch),	
					.en_group_pulse(en_group),
					.en_pc(en_pc)  ,
					.pc_ctrl(pc_ctrl) ,
					.reg_en(reg_en) ,
					.alu_in_sel(alu_in_sel)	,
					.alu_func(alu_func)			
				);


parameter Tclk = 10;

initial begin
			clk=1;
			forever #(Tclk/2) clk=~clk;
		end
        
initial begin
				    rst=0;
		  #(Tclk*3)	rst=1; 
		end

reg [2:0]cnt1;
always @ (posedge clk) begin
	if(!rst) 
		cnt1 <= 3'd1;          // When being reset, the cnt1 is initialized as 1 to align alu_end to posedge of first execution state
	else 
	    cnt1 <= cnt1+1;		   // cnt1 means that alu_end should be pulled up periodically
end	

always @ (posedge clk) begin
	    if(!rst)                   // Pull up alu_end every 5 clocks, this block should involve cnt1
    alu_end <= 1'b0;
else if (cnt1 == 4) begin
    alu_end <= 1'b1;
    cnt1 <= 0;
    #15 alu_end = 1'b0;
end
end

initial begin
                    	rd = 2'b00;
          #(Tclk*3)     rd = 2'b00;    // 3 clocks for aligning rd at Fetch state
		  #(Tclk*5)     rd = 2'b01;
		  #(Tclk*5)     rd = 2'b10;
		  #(Tclk*5)     rd = 2'b11;
        end

initial begin
                opcode=4'b0000;
  #(Tclk*3)     opcode=4'b0000;    // 3 clocks for aligning opcode at Fetch state
  #(Tclk*5)     opcode=4'b0010;
  #(Tclk*5)     opcode=4'b0101;
  #(Tclk*5)     opcode=4'b0111;
  #(Tclk*5)     opcode=4'b1001;
  #(Tclk*5)     opcode=4'b1010;
          // add your code here
        end
        
initial begin
          #(Tclk*70)  $stop;
end
				
endmodule

