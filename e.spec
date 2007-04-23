%define name 	e
%define version 0.16.999.023
%define release 0.%{cvsrel}.3mdk

%define cvsrel 20060323

%define major 	0
%define libname %mklibname %{name} %{major}

Summary: 	Enlightenment DR 17 window manager
Name: 		%name
Version: 	%version
Release: 	%release
License: 	BSD
Group: 		Graphical desktop/Enlightenment
Source: 	%{name}-%{cvsrel}.tar.bz2
Source1:	e17-menu-method.bz2
BuildRoot: 	%_tmppath/%name-buildroot
URL: 		http://www.get-e.org/
Buildrequires: 	ecore-devel evas-devel edje edje-devel
Buildrequires: 	eet-devel embryo-devel
Buildrequires:	multiarch-utils
BuildRequires:	gettext-devel
Requires:	ewl edb
Requires:	edje evas

%description
E17 is a next generation window manager for UNIX operating systems. Based on
the Enlightenment Foundation Libraries (EFL), E17 is much more than just
another window manager - it's an ambitious and innovative project that aims
to drive the development of graphical applications industry-wide for several
years to come.

%package -n %{libname}
Summary: Enlightement libraries
Group: System/Libraries

%description -n %{libname}
Dynamic libraries for Enlightenment window manager

%package -n %{libname}-devel
Summary: Enlightenment library headers and development libraries
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
E17 development headers and development libraries.

%prep
%setup -n e -q

%build
./autogen.sh
%configure2_5x --disable-valgrind
%make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
mkdir -p %buildroot/%{_sysconfdir}/menu-methods
bzcat %{SOURCE1} > %buildroot/%{_sysconfdir}/menu-methods/e17
chmod 755 %buildroot/%{_sysconfdir}/menu-methods/e17
%multiarch_binaries %buildroot/%{_bindir}/enlightenment-config

%find_lang enlightenment

# display manager entry
mkdir -p %buildroot/%{_sysconfdir}/X11/wmsession.d
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/23E17
NAME=E17
ICON=
EXEC=/usr/bin/enlightenment
SCRIPT:
exec /usr/bin/enlightenment
EOF

%post
%make_session
%postun
%make_session

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f enlightenment.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING
%_bindir/enlightenment
%_bindir/enlightenment_*
%_datadir/enlightenment
%_datadir/xsessions/*
%_libdir/enlightenment
%config %_sysconfdir/X11/wmsession.d/23E17
%_sysconfdir/menu-methods/e17

%files -n %{libname}
%defattr(-,root,root)
%_libdir/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/enlightenment-config
%_bindir/enlightenment-config
%_libdir/*.a
%_libdir/*.la
%_libdir/*.so
%_includedir/enlightenment
%_includedir/*.h
