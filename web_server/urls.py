from controllers import *

app.add_api_route('/login', login)
app.add_api_route('/servers', server_state)
app.add_api_route('/api/servers', api_servers)
app.add_api_route('/api/procs', api_procs)

