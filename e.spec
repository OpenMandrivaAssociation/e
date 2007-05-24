%define name 	e
%define oname	enlightenment
%define version 0.16.999.038
%define release %mkrel 2

%define major 	0
%define libname %mklibname %{name} %{major}

Summary: 	Enlightenment DR 17 window manager
Name: 		%name
Version: 	%version
Release: 	%release
License: 	BSD
Group: 		Graphical desktop/Enlightenment
Source: 	%{oname}-%{version}.tar.bz2
BuildRoot: 	%_tmppath/%name-buildroot
URL: 		http://www.get-e.org/
Buildrequires:  ecore-devel >= 0.9.9, evas-devel >= 0.9.9.038, edje, edje-devel
Buildrequires:  eet-devel >= 0.9.10.038, embryo-devel, embryo
Buildrequires:  efreet-devel >= 0.0.3.002
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

%package -n %{libname}-devel
Summary: Enlightenment library headers and development libraries
Group: System/Libraries
#Requires: %{libname} = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
E17 development headers and development libraries.

%prep
%setup -n %{oname}-%{version} -q 

%build
%configure2_5x --enable-files --disable-valgrind
%make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
%multiarch_binaries %buildroot/%{_bindir}/enlightenment-config

%find_lang enlightenment

# display manager entry
mkdir -p %buildroot/%{_sysconfdir}/X11/wmsession.d
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/23E17
NAME=E17
ICON=
EXEC=/usr/bin/enlightenment_start
SCRIPT:
exec /usr/bin/enlightenment_start
EOF

%post
%make_session
%postun
%make_session

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
%exclude %_libdir/enlightenment/modules/*/*/module.a
%exclude %_libdir/enlightenment/modules/*/*/module.la
%config %_sysconfdir/X11/wmsession.d/23E17
%config(noreplace) %_sysconfdir/enlightenment/sysactions.conf

%files -n %{libname}-devel
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/enlightenment-config
%_libdir/enlightenment/modules/*/*/module.a
%_libdir/enlightenment/modules/*/*/module.la
%_bindir/enlightenment-config
%_includedir/enlightenment

