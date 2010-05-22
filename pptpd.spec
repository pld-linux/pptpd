Summary:	Serves out PPTP connections
Summary(pl.UTF-8):	Serwer połączeń PPTP
Name:		pptpd
Version:	1.3.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Vendor:		Matthew Ramsay http://www.moretonbay.com/vpn/pptp.html
Source0:	http://dl.sourceforge.net/poptop/%{name}-%{version}.tar.gz
# Source0-md5:	b38df9c431041922c997c1148bedf591
Source1:	%{name}.init
Patch0:		%{name}-install.patch
Patch1:		%{name}-lib64.patch
URL:		http://www.poptop.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	ppp >= 2.4.3
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPTPd, Point-to-Point Tunnelling Protocol Daemon, offers out
connections to pptp clients to become virtual members of the IP pool
owned by the pptp server. In effect, these clients become virtual
members of the local subnet, regardless of what their real IP address
is. A tunnel is built between the pptp server and client, and packets
from the subnet are wrapped and passed between server and client
similar to other C/S protocols.

%description -l pl.UTF-8
PPTPd (Point-to-Point Tunnelling Protocol Daemon, czyli demon
obsługujący protokół tunelowania Point-to-Point) udostępnia połączenia
klientom pptp, aby stały się wirtualnymi członkami puli IP
obsługiwanej przez serwer pptp. W efekcie ci klienci stają się
wirtualnymi członkami podsieci lokalnej, niezależnie od ich
prawdziwego adresu IP. Tunel jest tworzony między serwerem a klientem
pptp, a pakiety z podsieci są wyłapywane i puszczane pomiędzy serwerem
a klientem podobnie do innych protokołów klient-serwer.

%prep
%setup -q
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

sed -i -e "s#/lib#/%{_lib}#g#" plugins/Makefile

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d}

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

install samples/pptpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pptpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

rm -rf html/CVS samples/CVS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pptpd
if [ -f /var/lock/subsys/pptpd ]; then
	/etc/rc.d/init.d/pptpd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/pptpd start\" to start pptpd." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pptpd ]; then
		/etc/rc.d/init.d/pptpd stop 1>&2
	fi
	/sbin/chkconfig --del pptpd
fi


%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO samples/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pptpd.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%{_libdir}/%{name}
