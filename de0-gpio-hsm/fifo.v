module fifo #(parameter DATA_WIDTH = 8, parameter ADDRESS_WIDTH = 7)(
    input clk,
    input reset,
    input read,
    input write,
	 input [DATA_WIDTH-1:0] in,
    output reg [DATA_WIDTH-1:0] out,
    output empty, 
    output full,
	 output [ADDRESS_WIDTH-1:0] counter_out
); 

reg [DATA_WIDTH-1:0] FIFO [0:(2**ADDRESS_WIDTH)-1];
reg [ADDRESS_WIDTH-1:0] counter = 0; 
reg [ADDRESS_WIDTH-1:0] read_ptr = 0;
reg [ADDRESS_WIDTH-1:0] write_ptr = 0; 

assign empty = (counter == 0)? 1'b1:1'b0; 
assign full = (counter == (2**ADDRESS_WIDTH)) ? 1'b1:1'b0;

assign counter_out = counter;

always @(posedge clk) begin
    if (reset) begin 
        read_ptr <= 0; 
        write_ptr <= 0;
    end else if (read == 1'b1 && counter != 0) begin 
        out  = FIFO[read_ptr]; 
		if (read_ptr == ((2**ADDRESS_WIDTH))-1) begin
            read_ptr <= 0; 
        end else begin
            read_ptr <= read_ptr + {{(ADDRESS_WIDTH-1){1'b0}},1'b1};
		end
    end else if (write == 1'b1 && counter < (2**ADDRESS_WIDTH)) begin
        FIFO[write_ptr] = in; 
		if (write_ptr == ((2**ADDRESS_WIDTH)-1)) begin
            write_ptr <= 0;
		end else begin
		    write_ptr <= write_ptr + {{(ADDRESS_WIDTH-1){1'b0}},1'b1};
		end 
    end
    if (read_ptr > write_ptr) begin 
        counter <= read_ptr-write_ptr; 
    end else if (write_ptr > read_ptr) 
        counter <= write_ptr-read_ptr; 
    end

endmodule