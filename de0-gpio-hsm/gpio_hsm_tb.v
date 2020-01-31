// gpio_hsm_tb.v

`timescale 1 ns/10 ps // time-unit = 1 ns, precision = 10 ps
module gpio_hsm_tb;

// duration for each bit = 20 * timescale = 20 * 1 ns = 20ns
localparam period = 20;
localparam REG_SIZE = 8;

wire bidir_signal;
reg clk = 1'b0;
reg [REG_SIZE-1:0] output_value;
wire [REG_SIZE-1:0] data_out, input_value;
reg output_value_valid;

gpio_hsm_top #(
    .BURST_SIZE(8)
) UUT (
    .CLK_50(clk), 
    .rst(1'b0),
	 .RP_CS(output_value_valid),
	 .RP_data(bidir_signal),
	 .LED(data_out)
);

assign input_value = bidir_signal;
assign bidir_signal = (output_value_valid == 1'b1) ? output_value : 8'hZZ;

always begin 
    clk = !clk;
    #(period/2);
end 

// initial block executes only once
initial begin
    #100;
    // now we switch to output signal
    output_value_valid = 1;
    output_value = 'h88;
    #period; // wait for period
	 output_value = 'h99;
    #period; // wait for period
    output_value = 'haa;
    #period; // wait for period
    output_value = 'hbb;
    #period; // wait for period
	 output_value = 'hcc;
    #period; // wait for period
	 output_value = 'hdd;
    #period; // wait for period
	 output_value = 'hee;
    #period; // wait for period
	 output_value = 'hff;
    #period; // wait for period
	 #200;
end
endmodule