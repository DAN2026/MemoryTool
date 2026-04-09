from blinker import signal

set_ini = signal('set-ini')
set_mipbias = signal('set-mipbias')
set_testing_ini = signal('set-testing-ini')

set_fov = signal('set-fov')
set_view_distance = signal('set-view-distance')

set_environment = signal('set-environment')
set_beer = signal('set-beer')
set_fullbright = signal('set-fullbright')

set_damage_numbers = signal('set-damage-numbers')
set_stalker_vision = signal('set-stalker-vision')
set_gamma = signal('set-gamma')

get_fov = signal('get-fov')
get_gamma = signal('get-gamma')
get_view_distance = signal('get-view-distance')

on_connection_change = signal('on-connection-change')
request_reconnect = signal('request-reconnect')
request_shutdown = signal('request-shutdown')

