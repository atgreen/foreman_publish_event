AUTOMAKE_OPTIONS = foreign

EXTRA_DIST = COPYING foreman_publish_event.spec

bin_PROGRAMS = foreman_publish_event

foreman_publish_event_CXXFLAGS = $(DEPS_CFLAGS)
foreman_publish_event_SOURCES = foreman_publish_event.cc
foreman_publish_event_LDADD = $(DEPS_LIBS)

