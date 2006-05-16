#
# Conditional build:
%bcond_without	gnome	# don't build gnome applet
%bcond_without	gtk	# don't build GTK+ GUI
#
%define dbversion 20060308
%define ddcdb	%{name}-db-%{dbversion}

Summary:	DDCcontrol - control the monitor parameters
Summary(pl):	DDCcontrol - narzędzie do regulacji parametrów monitora
Name:		ddccontrol
Version:	0.4.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/ddccontrol/%{name}-%{version}.tar.bz2
# Source0-md5:	bef6825f7dfffbb4fd40eb4a848cd438
Source1:	http://dl.sourceforge.net/ddccontrol/%{ddcdb}.tar.bz2
# Source1-md5:	973a5db6081054bbb336254331820b0c
Patch0:		%{name}-SAM0197.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-gnome.patch
URL:		http://ddccontrol.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_gnome:BuildRequires:	gnome-panel-devel >= 2.10}
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.4}
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DDCcontrol is a program used to control monitor parameters, like
brightness and contrast, by software, i.e. without using the OSD and
the buttons in front of the monitor.

%description -l pl
DDCcontrol jest programem służącym do regulacji parametrów monitora
takich jak jaskrawość i kontrast, bez używania OSD i przycisków na
obudowie monitora.

%package gtk
Summary:	GTK+ GUI for ddccontrol
Summary(pl):	Graficzny interfejs GTK+ dla ddccontrol
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
GTK+ GUI for ddccontrol.

%description gtk -l pl
Graficzny interfejs GTK+ dla ddccontrol.

%package applet
Summary:	GNOME applet for ddccontrol
Summary(pl):	Aplet GNOME dla ddccontrol
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description applet
GNOME applet for ddccontrol.

%description applet -l pl
Aplet GNOME dla ddccontrol.

%package libs
Summary:	ddccontrol library
Summary(pl):	Biblioteka ddccontrol
Group:		Libraries

%description libs
DDCcontrol library.

%description libs -l pl
Biblioteka DDCcontrol.

%package devel
Summary:	Development files for ddccontrol library
Summary(pl):	Pliki niezbędne programistom używającym biblioteki ddccontrol
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libxml2-devel
Requires:	pciutils-devel

%description devel
Development files for ddccontrol library.

%description devel -l pl
Pliki niezbędne programistom używającym biblioteki ddccontrol.

%package static
Summary:	Static ddccontrol library
Summary(pl):	Biblioteka statyczna ddccontrol
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ddccontrol library.

%description static -l pl
Biblioteka statyczna ddccontrol.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gtk:--disable-gnome} \
	%{!?with_gnome:--disable-gnome-applet}
%{__make}
cd %{ddcdb}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C %{ddcdb} install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/html
%attr(755,root,root) %{_bindir}/ddccontrol
%attr(755,root,root) %{_bindir}/ddcpci
%{_datadir}/ddccontrol-db

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gddccontrol
%{_desktopdir}/gddccontrol.desktop
%{_pixmapsdir}/gddccontrol.png
%endif

%if %{with gnome}
%files applet
%defattr(644,root,root,755)
%dir %{_libdir}/ddccontrol
%attr(755,root,root) %{_libdir}/ddccontrol/ddcc-applet
%{_datadir}/ddccontrol
%{_libdir}/bonobo/servers/*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so
%{_libdir}/libddccontrol.la
%{_includedir}/ddccontrol

%files static
%defattr(644,root,root,755)
%{_libdir}/libddccontrol.a
