// --------------------------------------------------------------------------
// foreman_publish_event.cc
//
// Copyright (C) 2018  Anthony Green <green@redhat.com>
// Distrubuted under the terms of the GPL v3 or later.
//
// This program is responsible for publishing foreman hook events
// through an ActiveMQ message broker.
// --------------------------------------------------------------------------

#include <cstdlib>
#include <memory>

#include <stdio.h>
#include <stdlib.h>
#include <glib.h>
#include <string.h>
#include <syslog.h>
#include <unistd.h>
#include <sys/types.h>

// On Fedora/EL, these headers are provided by the package activemq-cpp-devel.
#include <activemq/library/ActiveMQCPP.h>
#include <activemq/core/ActiveMQConnectionFactory.h>
#include <decaf/lang/System.h>

#define CONFIG_FILE "/etc/foreman_publish_event.conf"

using namespace activemq;
using namespace cms;
using namespace std;
 
static Session *session;
static MessageProducer *producer;

static void fatal (const char *msg)
{
  syslog (LOG_ERR, msg);
  exit (EXIT_SUCCESS);
}

static bool replace(std::string& str, const std::string& from, const std::string& to) {
  size_t start_pos = str.find(from);
  if(start_pos == std::string::npos)
    return false;
  str.replace(start_pos, from.length(), to);
  return true;
}

int main(int argc, const char *argv[])
{
  GKeyFile* gkf;
  gkf = g_key_file_new();

  if (!g_key_file_load_from_file(gkf, CONFIG_FILE, G_KEY_FILE_NONE, NULL))
    fatal ("Could not read config file " CONFIG_FILE);

  gchar *broker_uri = g_key_file_get_string (gkf, "broker", "uri", NULL);
  if (! broker_uri)
    fatal ("config file missing broker uri");
  
  gchar *broker_username = g_key_file_get_string (gkf, "broker", "username", NULL);
  if (! broker_username)
    fatal ("config file missing broker username");
  
  gchar *broker_password = g_key_file_get_string (gkf, "broker", "password", NULL);
  if (! broker_password)
    fatal ("config file missing broker password");
  
  string brokerURI = broker_uri;
  Connection *connection;
  Destination *destination;

  openlog ("foreman_publish_event", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);

  activemq::library::ActiveMQCPP::initializeLibrary();

  try {

    decaf::lang::System::setProperty("decaf.net.ssl.disablePeerVerification", "true");
    
    // Create a ConnectionFactory
    std::auto_ptr<ConnectionFactory> 
      connectionFactory(ConnectionFactory::createCMSConnectionFactory(brokerURI));

    // Create a Connection
    connection = connectionFactory->createConnection(broker_username,
						     broker_password);
    connection->start();

    session = connection->createSession(Session::AUTO_ACKNOWLEDGE);

    string topic("FOREMAN" + string(argv[0]));
    replace(topic, string("/usr/share/foreman/config/hooks"), string(""));
    replace(topic, string("/99_foreman_publish_event"), string(""));

    destination = session->createTopic(topic);

    producer = session->createProducer(destination);
    producer->setDeliveryMode(DeliveryMode::NON_PERSISTENT);

  } catch (CMSException& e) {

    fatal (e.getStackTraceString().c_str());

  }

  string msg;
  getline(cin, msg, (char) 0);
  
  std::auto_ptr<TextMessage> message(session->createTextMessage(msg));
  producer->send(message.get());

  return EXIT_SUCCESS;
}
