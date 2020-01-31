module interface_rx_tx #(parameter DATA_WIDTH = 8) (
    input clock,
    input chip_select,
    inout [DATA_WIDTH-1:0] data_pins,
	 input [DATA_WIDTH-1:0] data_from_interface,
    output [DATA_WIDTH-1:0] data_to_interface
);

reg [DATA_WIDTH-1:0] data_out_int;
reg [DATA_WIDTH-1:0] data_to_interface_int;

assign data_pins = chip_select ? 8'bZ : data_out_int;
assign data_to_interface = data_to_interface_int;

always @(posedge clock) begin
    // if chip select is high, the fpga is reading in data
    if(chip_select) begin
        data_to_interface_int <= data_pins;
    end else begin
        data_out_int <= data_from_interface;
    end
end 

endmodule