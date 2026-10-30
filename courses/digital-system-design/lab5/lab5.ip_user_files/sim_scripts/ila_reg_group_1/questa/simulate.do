onbreak {quit -f}
onerror {quit -f}

vsim -t 1ps -lib xil_defaultlib ila_reg_group_opt

do {wave.do}

view wave
view structure
view signals

do {ila_reg_group.udo}

run -all

quit -force
