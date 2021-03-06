%ifarch %{armx}
%bcond_without acpitool
%endif

%define use_ccache 1
%define oname enlightenment

%define efl_version 1.25.1

%define _disable_ld_no_undefined 1

Summary:	Enlightenment DR 19 window manager
Name:		e
Version:	0.24.2
Release:	3
License:	BSD
Group:		Graphical desktop/Enlightenment
Url:		http://www.enlightenment.org/
Source0:	http://download.enlightenment.org/rel/apps/%{oname}/%{oname}-%{version}.tar.xz
# When we have it:
#Source1:	some-theme.edj.bz2
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	bluez
BuildRequires:	doxygen
BuildRequires:	systemd-units
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	rfkill
BuildRequires:	efl >= %{efl_version}
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ecore) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-con) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-evas) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-file) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-input) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-input-evas) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-ipc) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-x) >= %{efl_version}
BuildRequires:	pkgconfig(edje) >= %{efl_version}
BuildRequires:	pkgconfig(eet) >= %{efl_version}
BuildRequires:	pkgconfig(eeze) >= %{efl_version}
BuildRequires:	pkgconfig(efl-canvas-wl) >= %{efl_version}
BuildRequires:	pkgconfig(efreet) >= %{efl_version}
BuildRequires:	pkgconfig(efreet-mime) >= %{efl_version}
BuildRequires:	pkgconfig(efreet-trash) >= %{efl_version}
BuildRequires:	pkgconfig(eina) >= %{efl_version}
BuildRequires:	pkgconfig(eio) >= %{efl_version}
BuildRequires:	pkgconfig(eldbus) >= %{efl_version}
BuildRequires:	pkgconfig(elementary) >= 1.11.0
BuildRequires:	pkgconfig(ethumb) >= %{efl_version}
BuildRequires:	pkgconfig(evas) >= %{efl_version}
BuildRequires:	pkgconfig(exchange)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-shape)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(xorg-server)
BuildRequires:	x11-server-xwayland
%if %{without acpitool}
Requires:	acpitool
%endif
Requires:	efl >= %{efl_version}
Recommends:	econnman

Provides:	%{oname} = %{EVRD}

%description
E21 is a next generation window manager 
based on the Enlightenment Foundation Libraries (EFL)
for composite enabled cards only

%files -f %{oname}.lang
%doc AUTHORS README COPYING doc/*
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf
%{_sysconfdir}/xdg/menus/e-applications.menu
%{_sysconfdir}/enlightenment/system.conf
%{_bindir}/%{oname}
%{_bindir}/%{oname}_*
%{_bindir}/emixer
%{_datadir}/%{oname}
%{_datadir}/applications/emixer.desktop
%{_datadir}/applications/enlightenment_filemanager.desktop
#{_datadir}/pixmaps/emixer.png
%{_iconsdir}/hicolor/128x128/apps/emixer.png
%{_iconsdir}/hicolor/512x512/apps/enlightenment.png
%{_iconsdir}/hicolor/512x512/apps/enlightenment_badge-symbolic.png
%{_iconsdir}/hicolor/512x512/places/enlightenment.png
%{_iconsdir}/hicolor/scalable/apps/enlightenment.svg
%{_iconsdir}/hicolor/512x512/places/enlightenment_badge-symbolic.png
%{_iconsdir}/hicolor/scalable/apps/enlightenment_badge-symbolic.svg
%{_iconsdir}/hicolor/scalable/places/enlightenment.svg
%{_iconsdir}/hicolor/scalable/places/enlightenment_badge-symbolic.svg
%{_datadir}/applications/enlightenment_askpass.desktop
%{_datadir}/wayland-sessions/enlightenment.desktop
%{_datadir}/xsessions/%{oname}.desktop
%{_datadir}/pixmaps/enlightenment-askpass.png
%{_libdir}/%{oname}
%{_unitdir}/enlightenment.service

#----------------------------------------------------------------------------

%package devel
Summary:	Enlightenment library headers and development libraries
Group:		Development/C

%description devel
E21 development headers and development libraries.

%files devel
%{_bindir}/%{oname}-config
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{oname}

#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}
%autopatch -p1

%build

%meson \
       -Dpam=true \
       -Dmount-eeze=true \
       -Dwl=true \
       -Dsystemdunitdir=%{_userunitdir}

%meson_build

%install
%meson_install

%find_lang %{oname}

# Put systemd service to proper path
mkdir -p %{buildroot}%{_unitdir}/
mv %{buildroot}/usr/lib/systemd/user/enlightenment.service %{buildroot}%{_unitdir}/enlightenment.service

#fake e-config
touch %{buildroot}/%{_bindir}/%{oname}-config
#%%multiarch_binaries %%{buildroot}/%%{_bindir}/%%{oname}-config

#fix bad perms
#chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/modules/cpufreq/linux-*/freqset
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_sys
#chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_backlight
