%ifarch %{armx}
%bcond_without acpitool
%endif

%define use_ccache 1
%define oname enlightenment

%define efl_version 1.28.0

%define _disable_ld_no_undefined 1

Summary:	Enlightenment DR 19 window manager
Name:		e
Version:	0.27.0
Release:	1
License:	BSD
Group:		Graphical desktop/Enlightenment
Url:		https://www.enlightenment.org/
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
BuildRequires:       pkgconfig(efl) >= %{efl_version}
BuildRequires:	pkgconfig(exchange)
BuildRequires:       pkgconfig(libexif)
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

# In future, let's create task-e package and pull as hard dependency all listed below packages.
Recommends:	econnman
Recommends:   terminology
Recommends:   rage
Recommends:   evisum
Recommends:   espionage
Recommends:   epour
Recommends:   ephoto
Recommends:   enventor
Recommends:   empc
Recommends:   eflete
Recommends:   edi
Recommends:   ecrire

Provides:	%{oname} = %{EVRD}
Provides:     task-%{oname}= %{EVRD}
Provides:     task-e = %{EVRD}

%description
E21 is a next generation window manager 
based on the Enlightenment Foundation Libraries (EFL)
for composite enabled cards only

%files -f %{oname}.lang
%doc AUTHORS COPYING doc/*
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf
%{_sysconfdir}/xdg/menus/e-applications.menu
%{_sysconfdir}/enlightenment/system.conf
%{_bindir}/%{oname}
%{_bindir}/%{oname}_*
%{_bindir}/emixer
%{_datadir}/%{oname}
%{_datadir}/applications/emixer.desktop
%{_datadir}/applications/enlightenment_filemanager.desktop
%{_datadir}/applications/enlightenment_fprint.desktop
%{_datadir}/applications/enlightenment_paledit.desktop
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
%{_iconsdir}/hicolor/*x*/apps/enlightenment_fprint.png
%{_iconsdir}/hicolor/*x*/apps/enlightenment_paledit.png
%{_datadir}/applications/enlightenment_askpass.desktop
#{_datadir}/wayland-sessions/enlightenment.desktop
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
# As of e 0.25.1 and Clang 13.0.0 build error appears:
#../src/bin/e_color.c:14:9: error: type '_Float32' (aka 'float') in generic association compatible with previously specified type 'float' if (!EINA_FLT_NONZERO(ec->v))
# As workaround switch to GCC for now.
export CC=gcc
export CXX=g++
%meson \
       -Dpam=true \
       -Dmount-eeze=true \
       -Dwl=false \
       -Dconnman=false \
       -Dsystemdunitdir=%{_userunitdir}
### FIXME ### wl=true enable wayland session but it is more unstable than Plasma6 on Wayland. So I can't recommend it even to my worst enemy. Lets disable it for now.
### FIXME ### if wayland session is enabled then X11 session is gone. Need to find way to enable both at same time.
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
