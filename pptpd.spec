Summary:	Serves out PPTP connections
Name:		pptpd
Version:	1.0.0
Release:	1
Copyright:	GPL
Group:		Utilities/System
Vendor:		Matthew Ramsay http://www.moretonbay.com/vpn/pptp.html
Source:		http://www.moretonbay.com/vpn/releases/%{name}-%{version}.tgz
URL:		http://www.moretonbay.com/vpn/pptp.html
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

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
LDFLAGS="-s"; export LDFLAGS
%configure
make 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}

make install DESTDIR=$RPM_BUILD_ROOT

install samples/pptpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pptpd.conf

gzip -9nf AUTHORS README TODO html/* samples/* \
	$RPM_BUILD_ROOT%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,COPYING,INSTALL,README,TODO,html/*,samples/*}.gz
%config(noreplace) %{_sysconfdir}/pptpd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
