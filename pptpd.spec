Summary:	Serves out PPTP connections
Name:		pptpd
Version:	0.9.2
Release:	1
Copyright:	GPL
Group:		Utilities/System
Vendor:		Matthew Ramsay http://www.moretonbay.com/vpn/pptp.html
Source:		http://www.moretonbay.com/vpn/pptpd-0.8.4.tgz
BuildRoot:	/tmp/%{version}-%{name}-root

%description
PPTPd, Point-to-Point Tunnelling Protocol Daemon, offers out connections to
pptp clients to become virtual members of the IP pool owned by the pptp
server. In effect, these clients become virtual members of the local
subnet, regardless of what their real IP address is.  A tunnel is built
between the pptp server and client, and packets from the subnet are wrapped
and passed between server and client similar to other C/S protocols.

%prep
%setup -q

%build
./configure
make 

%install
rm -rf $RPM_BUILD_ROOT

make install
install samples/pptpd.conf /etc/pptpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING INSTALL README TODO html samples
/usr/bin/pptpd
/usr/bin/pptpctrl
/etc/pptpd.conf
