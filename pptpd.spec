Summary:	Serves out PPTP connections
Summary(pl):	Serwer po³±czeñ PPTP
Name:		pptpd
Version:	1.1.2
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Vendor:		Matthew Ramsay http://www.moretonbay.com/vpn/pptp.html
Source0:	http://poptop.lineo.com/releases/%{name}-%{version}.tar.gz
URL:		http://poptop.lineo.com/	
BuildRequires:	automake
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
PPTPd, Point-to-Point Tunnelling Protocol Daemon, offers out
connections to pptp clients to become virtual members of the IP pool
owned by the pptp server. In effect, these clients become virtual
members of the local subnet, regardless of what their real IP address
is. A tunnel is built between the pptp server and client, and packets
from the subnet are wrapped and passed between server and client
similar to other C/S protocols.

%prep
%setup -q

%build
aclocal
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install samples/pptpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pptpd.conf

gzip -9nf AUTHORS README TODO COPYING INSTALL html/* samples/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,COPYING,INSTALL,README,TODO,html/*,samples/*}.gz
%config(noreplace) %{_sysconfdir}/pptpd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
