module hsm_control(
    input clk,
	 input reset,
    input in1,
	 input in2, 
	 input ifc_read,
    output [3:0] out
);

parameter zero=0, one=1, two=2, three=3;

reg [3:0] out_int;
reg [1:0] state;

assign out = out_int;

always @(state) begin
     begin
          case (state)
               zero:
                    out_int = 4'b0000;
               one:
                    out_int = 4'b0001;
               two:
                    out_int = 4'b0010;
               three:
                    out_int = 4'b0100;
               default:
                    out_int = 4'b1111;
          endcase
     end
end

always @(posedge clk or posedge reset) begin
     begin
          if (reset)
               state = zero;
          else
               case (state)
                    zero:
                         state = one;
                    one:
                         if (in1)
                              state = two;
                         else
                              state = one;
                    two:
                         if (in2)
                              state = three;
                         else
                              state = two;
                    three:
                         state = zero;
               endcase
     end
end

endmodule 