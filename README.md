# foreman_publish_event

This is a very experimental project.

The foreman_publish_event project sends foreman_hook create/destroy
events to ActiveMQ, allowing users to subscribe to topics of interest
for automation purposes without tasking the foreman/Satellite
administrator with hook script development, installation and
maintenance.

Example use cases include:

* Trigger gold image VM template or base container image creation
  based on ContentView promotions.

* Update CMDB records based on host create/destroy messages.

* Send notification messages based on new errata availability.

* etc

# Author

foreman_publish_event is an experiment by Anthony Green.




