Summary: Serves out PPTP connections
Name: pptpd
Version: 0.8.13
Release: 1
Copyright: GPL
Group: Utilities/System
Source: http://www.moretonbay.com/vpn/pptpd-0.8.4.tgz
vendor: Matthew Ramsay http://www.moretonbay.com/vpn/pptp.html
packager: Allan's Package-O-Matic Blenderfier
%description
PPTPd, Point-to-Point Tunnelling Protocol Daemon, offers out connections
to pptp clients to become virtual members of the IP pool owned by the pptp
server.  In effect, these clients become virtual members of the local
subnet, regardless of what their real IP address is.  A tunnel is built
between the pptp server and client, and packets from the subnet are
wrapped and passed between server and client similar to other C/S
protocols.

%prep
%setup -c pptpd-%{PACKAGE_VERSION} -T
TAG=`echo %{PACKAGE_VERSION} | sed -e 's/\./_/g'`
cd .. && cvs -d :pserver:anoncvs@cvs.pptpd.wonderland.org:/cvs/pptpd export -r PPTPD_$TAG -d pptpd-%{PACKAGE_VERSION} -f pptpd

%build
./configure
make 

%install
make install
install -m 0644 samples/pptpd.conf /etc/pptpd.conf

%files
%doc AUTHORS COPYING INSTALL README TODO html samples
/usr/local/bin/pptpd
/usr/local/bin/pptpctrl
/etc/pptpd.conf
