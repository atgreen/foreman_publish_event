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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%license COPYING

%changelog
* Wed Aug 8 2018 Anthony Green <green@redhat.com> 0.1.0-1
- Created.
