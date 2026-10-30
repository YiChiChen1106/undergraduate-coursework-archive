`timescale 1 ns /1 ns

`define B15to0H     3'b000
`define AandBH      3'b011
`define AorBH       3'b100
`define AaddBH      3'b001
`define AsubBH      3'b010
`define leftshift   3'b101
`define rightshift  3'b110
`define XOR  3'b111

module alu (
	clk,rst, 
	en_in, alu_a, alu_b, alu_func, en_out, alu_out
);
input [15:0] alu_a, alu_b;
input clk,rst, en_in;
input [2:0] alu_func;
output [15:0] alu_out;
output en_out;
reg [15:0] alu_out;
reg  en_out;

always @(negedge rst or posedge clk) 
begin
    if(rst ==1'b0)
	   begin
	   	alu_out <= 16'b0000000000000000;
	   	en_out  <= 1'b0;
	   end				
    else 
        begin
		if(en_in == 1'b1)
			begin
				en_out  <= 1'b1;
			    case (alu_func)
				`B15to0H:alu_out <= alu_b;
				`AaddBH: alu_out <=alu_a+alu_b;
				`AsubBH: alu_out <=alu_a-alu_b;
				`AandBH: alu_out <=alu_a&alu_b;
				`AorBH: alu_out <=alu_a|alu_b;
				`leftshift:alu_out <=alu_a<<1;
				`rightshift:alu_out <=alu_a>>1;
				`XOR:alu_out<=alu_a^alu_b;
				default: alu_out <= 16'b0000000000000000;
			    endcase
			end
		else 
			begin
				en_out <= 1'b0;
				alu_out <= alu_out;
			end
			
        end
end
endmodule
