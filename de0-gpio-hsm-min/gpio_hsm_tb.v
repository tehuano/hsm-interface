// gpio_hsm_tb.v

`timescale 1 ns/10 ps // time-unit = 1 ns, precision = 10 ps
module gpio_hsm_tb;

// duration for each bit = 20 * timescale = 20 * 1 ns = 20ns
localparam period = 15;
localparam REG_SIZE = 8;
localparam ADDRESS_WIDTH = 7;

wire [REG_SIZE-1:0] bidir_signal;
wire [ADDRESS_WIDTH-1:0] data_out;

reg [REG_SIZE-1:0] external_data_value;
reg bus_dir = 1'b0;
reg dir = 1'b0;
wire rp_irq;
reg rp_clk = 1'b0;
reg load_key;

gpio_hsm #(
    .DATA_WIDTH(8)
) UUT (
	 .RP_clock(rp_clk),
	 .RP_is_key(load_key),
	 .RP_dir(bus_dir),
	 .RP_data(bidir_signal),
	 .FPGA_data(data_out)
);

assign bidir_signal = (bus_dir == 1'b1) ? external_data_value : 8'hZZ;

always begin
   #5;
	rp_clk = !rp_clk;
   #5;
	rp_clk = !rp_clk;
	#5;
end

always begin
   #4;
	bus_dir = !bus_dir;
   #7;
	bus_dir = !bus_dir;
	#19;
end	

// initial block executes only once
initial begin
    #1;
    // now we switch to output signal
	 load_key = 1'b0;
	 external_data_value = 'haa;
	 #1;
	 dir = 1'b1;
	 #2;
	 load_key = 1'b1;
	 #(period/5);
	 load_key = 1'b0;
    #(period/5); // wait for period
    external_data_value = 'h01;
    #period; // wait for period
    external_data_value = 'h02;
    #period; // wait for period
	 external_data_value = 'h03;
    #period; // wait for period
	 external_data_value = 'h04;
    #period; // wait for period
	 external_data_value = 'h05;
    #period; // wait for period
	 external_data_value = 'h06;
    #period; // wait for period
	 external_data_value = 'h07;
    #period; // wait for period
	 external_data_value = 'h08;
    #period; // wait for period
	 external_data_value = 'h09;
    #period; // wait for period
	 external_data_value = 'h0a;
    #period; // wait for period
	 dir = 1'b0;
	 #(20*period);
    bus_dir = 1'b1;
    #(40*period);
	 bus_dir = 1'b0;
end
endmodule