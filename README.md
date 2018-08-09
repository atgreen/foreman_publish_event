# foreman_publish_event

This is a very experimental project.

`foreman_publish_event` sends `foreman_hook` create/destroy events to
ActiveMQ, allowing users to subscribe to topics of interest in order
to trigger automation.

## Why?

Developing `foreman_hook` based automation requires admin access to
the Satellite server.  This is not always convenient or even possible.
By publishing hook events over an ActiveMQ message bus, developers are
free to experiment with system automation tasks without interfering
with day-to-day Satellite operations.

An example use case would be for a development team wanting to trigger
Linux container image rebuilds based on new Satellite content
availability.  `foreman_publish_event` removes a dependency on
Satellite operations, allowing for faster development and freedom to
innovate.

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




