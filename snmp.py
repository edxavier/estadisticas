from easysnmp import Session


# Create an SNMP session to be used for all our requests
session = Session(hostname='10.160.80.22', community='public', version=2)


# And of course, you may use the numeric OID too
description = session.get('.1.3.6.1.4.1.2021.4.11.0')

location = session.get('.1.3.6.1.4.1.2021.11.9.0')
services = session.get('.1.3.6.1.4.1.2021.10.1.3.1')

print("Location "+location.value)
print("Desc> "+description.value)
print("Serv "+services.value)

# Perform an SNMP w
