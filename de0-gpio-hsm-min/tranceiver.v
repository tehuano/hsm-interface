module tranceiver #(parameter DATA_WIDTH = 8) (
    input clk,
    input chip_select,
    inout [DATA_WIDTH-1:0] data_pins,
	 input [DATA_WIDTH-1:0] data_from_hsm,
    output [DATA_WIDTH-1:0] data_to_hsm
);

reg [DATA_WIDTH-1:0] data_out_int;
reg [DATA_WIDTH-1:0] data_to_hsm_int;

assign data_pins = chip_select ? 8'bZ : data_out_int;
assign data_to_hsm = data_to_hsm_int;

always @(*) begin
    // if chip select is high, the fpga is reading in data
    if(chip_select) begin
        data_to_hsm_int <= data_pins;
    end else begin
        data_out_int <= data_from_hsm;
    end
end 

endmodule