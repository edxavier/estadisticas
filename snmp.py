from easysnmp import Session

# Create an SNMP session to be used for all our requests
session = Session(hostname='localhost', community='public', version=2)


# And of course, you may use the numeric OID too
description = session.get('.1.3.6.1.2.1.1.7.0')
location = session.get('HOST-RESOURCES-MIB::hrSystemUptime.0')
print(location.value)
print(description)

# Perform an SNMP w
