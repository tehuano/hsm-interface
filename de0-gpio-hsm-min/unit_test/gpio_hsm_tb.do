# create the default "work" library
vlib work

# compile files
vlog ../gpio_hsm.v
vlog ../tranceiver.v
vlog ../gpio_hsm_tb.v

vsim work.gpio_hsm_tb

# waveforms to be analyzed
add wave /gpio_hsm_tb/rp_clk
add wave /gpio_hsm_tb/load_key
add wave /gpio_hsm_tb/bus_dir
add wave /gpio_hsm_tb/bidir_signal 
add wave /gpio_hsm_tb/data_out 
add wave /gpio_hsm_tb/external_data_value
add wave /gpio_hsm_tb/UUT/result_int
add wave /gpio_hsm_tb/UUT/key_int
add wave /gpio_hsm_tb/UUT/data_in
add wave /gpio_hsm_tb/UUT/rx_tx/data_to_hsm

# reset the simulation
restart -force

# run the full simulation
run 2000 ns

#list signals
#add list -radix hexadecimal signal

#write list -window .main_pane.list gpio_hsm_tb.lst

# open the wave window
#view wave