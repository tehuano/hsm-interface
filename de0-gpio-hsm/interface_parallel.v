module interface_parallel #(parameter DATA_WIDTH = 8, parameter ADDRESS_WIDTH = 6)(
    input clk,
	 input xclk,
	 input rst,
    input load,
	 input read,
	 input write,
	 input send,
    inout [DATA_WIDTH-1:0] in_external,
	 input [DATA_WIDTH-1:0] in_internal,
	 output rx_empty,
	 output rx_full,
	 output tx_empty,
	 output tx_full,
    output [DATA_WIDTH-1:0] out,
    output [ADDRESS_WIDTH-1:0] out_phy
);

// rx signals
reg rx_read;
reg rx_write;
reg [DATA_WIDTH-1:0] rx_data_in;
reg [DATA_WIDTH-1:0] out_int;
wire [DATA_WIDTH-1:0] rx_out;

// tx signals
reg tx_read;
reg tx_write;
reg [DATA_WIDTH-1:0] tx_data_in;
wire [DATA_WIDTH-1:0] tx_out;

wire [DATA_WIDTH-1:0] data_in;
reg [DATA_WIDTH-1:0] data_out;

// output assignments 
assign out = out_int;

always @(posedge clk) begin
    if (load) begin
        rx_write <= 1;
		  rx_data_in <= data_in;
	 end else begin
        rx_write <= 0;
	 end
end

always @(posedge clk) begin
    if (read) begin
	     rx_read <= 1;
        out_int <= rx_out;
	 end else begin
	     rx_read <= 0;
	 end
end

always @(posedge clk) begin
    if (write) begin
        tx_write <= 1;
        tx_data_in <= in_internal;
     end else begin
        tx_write <= 0;
     end
end

always @(posedge clk) begin
    if (send) begin
        tx_read <= 1;
        data_out <= tx_out;
     end else begin
        tx_read <= 0;
     end
end

fifo #(DATA_WIDTH,ADDRESS_WIDTH) rx_fifo(
    .clk(clk),
    .reset(rst),
    .read(rx_read),
    .write(rx_write),
    .in(rx_data_in),
    .out(rx_out),
    .counter_out(out_phy)
);

fifo #(DATA_WIDTH,ADDRESS_WIDTH) tx_fifo(
    .clk(clk),
	 .reset(rst),
    .read(tx_read),
	 .write(tx_write),
    .in(tx_data_in),
    .out(tx_out)
);

interface_rx_tx interface_rx_tx_0(
    .clock(clk),
    .chip_select(load),
    .data_pins(in_external),
    .data_to_interface(data_in),
    .data_from_interface(data_out)
);
    
endmodule