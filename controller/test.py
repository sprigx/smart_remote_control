from remote_controller import RemoteController

con = RemoteController(17)
res = con.transmit('dac', 'voldown')
print(res)
con.transmit('dac', 'voldown')
con.cleanup()
