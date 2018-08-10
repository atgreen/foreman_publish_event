Name:		foreman_publish_event
Version:	0.1.0
Release:	1
Summary:	Publish foreman hook events over ActiveMQ

Group:		Development/Tools
License:	GPLv3
URL:		https://github.com/atgreen/foreman_hook_event
Source0:	foreman_publish_event-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  activemq-cpp-devel glib2-devel
Requires:       tfm-rubygem-foreman_hooks

%description
foreman_publish_event sends all foreman hook events over OpenWire +
SSL to ActiveMQ.  Interested parties can subscribe to their topic of
interest to trigger automation.

%prep
%setup -q -n foreman_publish_event-%{version}

%build
CXXFLAGS="%optflags -Wno-error=format-security -Wno-deprecated-declarations" ./configure --prefix=%_prefix
%__make all 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/etc
cp foreman_publish_event.conf $RPM_BUILD_ROOT/etc

%post
TMPDIR=`mktemp -d /tmp/foreman_publish_event_XXXXXXX`
mkdir -p $TMPDIR
foreman-rake hooks:objects 2>/dev/null | sort | uniq > $TMPDIR/objects 
cat $TMPDIR/objects | xargs -n1 -iXXXX  mkdir -p /usr/share/foreman/config/hooks/XXXX/after_destroy
cat $TMPDIR/objects | xargs -n1 -iXXXX  mkdir -p /usr/share/foreman/config/hooks/XXXX/after_create
cat $TMPDIR/objects | xargs -n1 -iXXXX  ln -s %{_bindir}/foreman_publish_event /usr/share/foreman/config/hooks/XXXX/after_create/99_foreman_publish_event
cat $TMPDIR/objects | xargs -n1 -iXXXX  ln -s %{_bindir}/foreman_publish_event /usr/share/foreman/config/hooks/XXXX/after_destroy/99_foreman_publish_event
rm -rf $TMPDIR

mkdir -p /usr/share/foreman/config/hooks/katello/repository/after_sync
ln -s %{_bindir}/foreman_publish_event /usr/share/foreman/config/hooks/katello/repository/after_sync

# Work around foreman_hooks bug: https://github.com/theforeman/foreman_hooks/issues/45
find /usr/share/foreman/config/hooks/aix -name 99_foreman_publish_event	| xargs	rm
find /usr/share/foreman/config/hooks/foreman/model/ec2 -name 99_foreman_publish_event | xargs rm
find /usr/share/foreman/config/hooks/foreman/model/gce -name 99_foreman_publish_event | xargs rm
find /usr/share/foreman/config/hooks/katello/kt_environment -name 99_foreman_publish_event | xargs rm
find /usr/share/foreman/config/hooks/nic/bmc -name 99_foreman_publish_event | xargs rm
find /usr/share/foreman/config/hooks/nxos -name 99_foreman_publish_event | xargs rm

%preun
find /usr/share/foreman/config/hooks -name 99_foreman_publish_event | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) /etc/foreman_publish_event.conf
%doc README.md
%license COPYING

%changelog
* Wed Aug 8 2018 Anthony Green <green@redhat.com> 0.1.0-1
- Created.
