%define name 	e
%define oname	enlightenment
%define version 0.16.999.038
%define release %mkrel 1

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


%changelog
* Wed May 16 2007 Antoine Ginies <aginies@mandriva.com> 0.16.999.038-1mdv2008.0
- CVS snapshot 20070516
- fix wmsessions.d file

* Tue Apr 24 2007 Pascal Terjan <pterjan@mandriva.org> 0.16.999.037-2mdv2008.0
+ Revision: 17859
- Drop the menu-method, e17 now supports .desktop

* Tue Apr 24 2007 Pascal Terjan <pterjan@mandriva.org> 0.16.999.037-1mdv2008.0
+ Revision: 17734
- BuildRequires embryo
- 0.16.999.037
- remove the lib package
- update file list
- Import e



* Tue Mar 28 2006 Austin Acton <austin@mandriva.org> 0.16.999.023-0.20060323.3mdk
- typo

* Mon Mar 27 2006 Austin Acton <austin@mandriva.org> 0.16.999.023-0.20060323.2mdk
- requires evas and edje

* Sat Mar 25 2006 Austin Acton <austin@mandriva.org> 0.16.999.023-0.20060323.1mdk
- new cvs checkout

* Tue Jan 17 2006 Austin Acton <austin@mandriva.org> 0.16.999.23-0.20060117.1mdk
- new cvs checkout

* Thu Nov 24 2005 AUstin Acton <austin@mandriva.org> 0.16.999.13-0.20051124.1mdk
- new cvs checkout
- disable valgrind

* Mon Nov 14 2005 Austin Acton <austin@mandriva.org> 0.16.999.13-0.20051109.2mdk
- buildrequires

* Thu Nov 10 2005 Austin Acton <austin@mandriva.org> 0.16.999.13-0.20051109.1mdk
- new cvs checkout

* Sun Sep 4 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050904.1mdk
- new cvs checkout

* Mon Aug 29 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050813.5mdk
- update menu method from Guillaume Bedot

* Mon Aug 15 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050813.4mdk
- oops, make menu method exectuable

* Sun Aug 14 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050813.3mdk
- first test of menu method from Guillaume Bedot

* Sun Aug 14 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050813.2mdk
- multiarch binaries

* Sun Aug 14 2005 Austin Acton <austin@mandriva.org> 0.16.999.013-0.20050813.1mdk
- new cvs checkout

* Mon Jun 27 2005 Austin Acton <austin@mandriva.org> 0.16.999.010-0.20050627.1mdk
- new cvs checkout

* Thu Jun 9 2005 Austin Acton <austin@mandriva.org> 0.16.999.008-0.20050608.2mdk
- requires ewl, edb

* Wed Jun 8 2005 Austin Acton <austin@mandriva.org> 0.16.999.008-0.20050608.1mdk
- new cvs checkout

* Mon May 16 2005 Austin Acton <austin@mandriva.org> 0.16.999.007-0.20050511.3mdk
- fix wmsession file

* Mon May 16 2005 Austin Acton <austin@mandriva.org> 0.16.999.007-0.20050511.2mdk
- move config binary to devel package
- use wmsession.d

* Fri May 13 2005 Austin Acton <austin@mandriva.org> 0.16.999.007-0.20050511.1mdk
- revamp e17 spec file
- add dm entry
- make parallel installable with enlightenment 16
