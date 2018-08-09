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

## Building

### Red Hat Enterprise Linux 7

foreman_publish_event uses ActiveMQ 6, which means you'll need the
`activemq-cpp-devel` package from EPEL.  Also be sure to install
`rpmbuild`, `autoconf`, `automake` and `gcc-c++`.

* Run the provided `autogen.sh` and the newly created `configure` script to create build machinery.
* Run `make dist` to create a tarball.
* Run `rpmbuild -ta foreman_publish_event-VERSION.tar.gz` to build the RPM.

## Configuring

The config file is `/etc/foreman_publish_event`.  You'll need to set
the ActiveMQ broker `uri` as well as login credentials `username` and
`password`.

## Troubleshooting

Errors are sent to syslog, which you can review with `journalctl`.

## Author

foreman_publish_event is an experiment by Anthony Green.




