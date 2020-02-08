// top module of the design
// Instantiates the controller and model

//ep3c16f484c6n

// clk and cs
//Plug GPIO1_CLKIN0on the DE0 into GPIO 8 on the Raspberry Pi
//Plug GPIO1_D8 on the DE0 into GPIO 10 on the Raspberry Pi
//Plug GPIO1_D9 on the DE0 into GPIO 20 on the Raspberry Pi

// data
//Plug GPIO1_D0 on the DE0 into GPIO 24 on the Raspberry Pi
//Plug GPIO1_D1 on the DE0 into GPIO 4 on the Raspberry Pi
//Plug GPIO1_D2 on the DE0 into GPIO 17 on the Raspberry Pi
//Plug GPIO1_D3 on the DE0 into GPIO 22 on the Raspberry Pi
//Plug GPIO1_D4 on the DE0 into GPIO 9 on the Raspberry Pi
//Plug GPIO1_D5 on the DE0 into GPIO 25 on the Raspberry Pi
//Plug GPIO1_D6 on the DE0 into GPIO 18 on the Raspberry Pi
//Plug GPIO1_D7 on the DE0 into GPIO 23 on the Raspberry Pi

module gpio_hsm #(parameter DATA_WIDTH = 8)(
    input RP_clock,
    input RP_is_key,
	 input RP_dir,
    inout [DATA_WIDTH-1:0] RP_data,
    output [DATA_WIDTH-1:0] FPGA_data
);

wire [DATA_WIDTH-1:0] result_int;
reg [DATA_WIDTH-1:0] key_int;
wire [DATA_WIDTH-1:0] data_in;
reg [DATA_WIDTH-1:0] data_in_int;

assign FPGA_data = result_int;
assign result_int = key_int ^ data_in_int;

always @(posedge RP_clock) begin
    if (RP_is_key == 1) begin
	     key_int <= data_in;
    end else if (RP_dir == 1) begin
	     data_in_int <= data_in;
    end
end

 tranceiver #(8) rx_tx (
    .clk(RP_clock),
    .chip_select(RP_dir),
    .data_pins(RP_data),
	 .data_from_hsm(result_int),
	 .data_to_hsm(data_in)
);

endmodule