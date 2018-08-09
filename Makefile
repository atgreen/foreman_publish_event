foreman_publish_event: foreman_publish_event.cc
	g++ -O3 -g -o $@ \
		`pkg-config activemq-cpp --cflags` \
		`pkg-config glib-2.0 --cflags` \
		`pkg-config glib-2.0 --libs` \
		`pkg-config activemq-cpp --libs` $<
