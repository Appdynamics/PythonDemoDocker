
#mysql.server restart
#mysql.server start
#mysql -u root

#redis-server /usr/local/etc/redis.conf

#postgres -D /usr/local/var/postgres/

#elasticsearch

#pyagent run -c appdynamics.cfg python app.py
#pyagent run -c appdynamics2.cfg python app2.py










#locust -f locustfile.py --host=http://127.0.0.1:5000
#./startController.sh
#app.config.from_pyfile('config.py')

#cursor.execute("CREATE TABLE Inventory(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Email VARCHAR(20))")
#for x in range(1,5000):
    #inventory = (
        #(x, 'Eric', 'ejoha001'),
        #(x+5000, 'Eric', 'ejoha001')
    #)
    #query = "INSERT INTO Inventory (Id, Name, Email) VALUES (%s, %s, %s)"
    #cursor.executemany(query, inventory)
    #cursor.execute("SELECT * FROM Inventory")

#rows = cursor.fetchall()


#class MissingArgumentException(Exception):
#    status_code = 400
#
#    def __init__(self, message):
#        super(MissingArgumentException, self).__init__()
#        self.message = message
#
#@app.errorhandler(MissingArgumentException)
#def handle_missing_argument_exception(error):
#    return render_template_string(
#        "<!DOCTYPE html><title>Missing Required Argument</title><h1>Missing required argument: {{msg}}",
#        msg=error.message)
