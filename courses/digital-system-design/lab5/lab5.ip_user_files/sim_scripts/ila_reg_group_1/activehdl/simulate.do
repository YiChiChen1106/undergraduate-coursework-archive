onbreak {quit -force}
onerror {quit -force}

asim -t 1ps +access +r +m+ila_reg_group -L xil_defaultlib -L xpm -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.ila_reg_group xil_defaultlib.glbl

do {wave.do}

view wave
view structure

do {ila_reg_group.udo}

run -all

endsim

quit -force
