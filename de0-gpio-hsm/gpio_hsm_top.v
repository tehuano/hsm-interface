// top module of the design
// Instantiates the controller and model

// clk and cs
//Plug GPIO1_CLKIN0on the DE0 into GPIO 8 on the Raspberry Pi
//Plug GPIO1_D8 on the DE0 into GPIO 10 on the Raspberry Pi
// data
//Plug GPIO1_D0 on the DE0 into GPIO 24 on the Raspberry Pi
//Plug GPIO1_D1 on the DE0 into GPIO 4 on the Raspberry Pi
//Plug GPIO1_D2 on the DE0 into GPIO 17 on the Raspberry Pi
//Plug GPIO1_D3 on the DE0 into GPIO 22 on the Raspberry Pi
//Plug GPIO1_D4 on the DE0 into GPIO 9 on the Raspberry Pi
//Plug GPIO1_D5 on the DE0 into GPIO 25 on the Raspberry Pi
//Plug GPIO1_D6 on the DE0 into GPIO 18 on the Raspberry Pi
//Plug GPIO1_D7 on the DE0 into GPIO 23 on the Raspberry Pi

module gpio_hsm_top #(
    parameter BURST_SIZE = 8,
    parameter DATA_WIDTH = 8,
    parameter ADDRESS_WIDTH = 7
)(
    input CLK_50,
	 input rst,
    input RP_clock,
    input RP_CS,
    inout [DATA_WIDTH-1:0] RP_data,
    output [ADDRESS_WIDTH-1:0] LED
);

// internal connections
wire [DATA_WIDTH-1:0] interface_to_hsm;
wire [DATA_WIDTH-1:0] hsm_to_interface;
wire ifc_read;
wire ifc_write;
wire ifc_send;
wire rx_full;
wire tx_full;
wire [3:0] hsm_ctrl_out;

// instance of the interface
interface_parallel #(8,7) interface_parallel_0(
    .clk(CLK_50),
	 .xclk(RP_clock),
	 .rst(rst),
    .load(RP_CS),
	 .read(ifc_read),
	 .write(ifc_write),
	 .send(ifc_send),
    .in_external(RP_data),
	 .in_internal(hsm_to_interface),
	 .out(interface_to_hsm),
	 .rx_full(rx_full),
	 .tx_full(tx_full),
    .out_phy(LED)
);

hsm_control hsm_control_0(
    .clk(CLK_50),
    .in1(rx_full),
	 .in2(tx_full), 
    .reset(rst),
	 .ifc_read(ifc_read), // todo
    .out(hsm_ctrl_out)
);
	 
// here is going to be an instance of the controller

endmodule