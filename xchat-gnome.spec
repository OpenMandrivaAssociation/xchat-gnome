%define build_plf 0
%define build_perl 1
%define build_python 1
%define build_tcl 1
%define build_netmon 0

%{?_with_plf: %{expand: %%global build_plf 1}}

%{?_without_perl: %{expand: %%global build_perl 0}} 
%{?_with_perl: %{expand: %%global build_perl 1}} 

%{?_without_python: %{expand: %%global build_python 0}} 
%{?_with_python: %{expand: %%global build_python 1}} 

%{?_without_tcl: %{expand: %%global build_tcl 0}} 
%{?_with_tcl: %{expand: %%global build_tcl 1}} 

%{?_without_netmon: %{expand: %%global build_netmon 0}} 
%{?_with_netmon: %{expand: %%global build_netmon 1}} 

%define perl_version	%(rpm -q --qf '%%{epoch}:%%{VERSION}' perl)
%define iconname xchat-gnome.png 

%if %build_plf
%define distsuffix plf
%endif 

Summary:	Graphical IRC client for the GNOME desktop 
Name:		xchat-gnome
Version:	0.24.0
Release:	%mkrel 1
Group:		Networking/IRC
License:	GPLv2+
Url:		http://xchat-gnome.navi.cx
Source:		http://ftp.gnome.org/pub/GNOME/sources/xchat-gnome/0.24/%{name}-%{version}.tar.bz2 
# do not give away OS with VERSION
Patch0:		%{name}-0.18-ctcp_version.patch
# (tpg) no more crash on startup
Patch1:		%{name}-0.18-config.patch
BuildRequires:	bison
Buildrequires:	gtk+2-devel
BuildRequires:	openssl-devel
BuildRequires:	GConf2
BuildRequires:	intltool gettext-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libnotify-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	scrollkeeper
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	libnotify-devel
BuildRequires:	libsexy-devel
BuildRequires:	libcanberra-devel >= 0.3
%if %build_perl
BuildRequires:	perl-devel
%endif
%if %build_python
BuildRequires:	python-devel
%endif
%if %build_tcl
BuildRequires:	tcl tcl-devel
%endif
BuildRequires:	dbus-devel >= 0.50
%if %build_plf
BuildRequires:	socks5-devel
%endif
BuildRequires:	libxslt-proc
BuildRequires:	chrpath
Provides:	xchat-gnome-dbus = %{version}-%{release}
Obsoletes:	xchat-gnome-dbus < 0.15
Requires(post):	scrollkeeper
Requires(postun): scrollkeeper
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
XChat-gnome is a new frontend to the popular X-Chat IRC client which is
designed with the user interface foremost in mind. Historically, the OSS
desktop has been steadily improving in usability, accessibility, and general
slickness, yet the world of IRC clients has not kept up. With IRC being one
of the fundamental methods of communication within the open source community,
it is bizzare that this area has been neglected.

%package devel
Summary:	XChat header for plugin development
Group:		Networking/IRC

%description devel
This package contains xchat-plugin.h needed to build external plugins.

%package perl
Summary:	XChat Perl plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}
Requires:	perl-base = %{perl_version}

%description perl
Provides Perl scripting capability to XChat.

%package python
Summary:	XChat Python plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description python
Provides Python scripting capability to XChat.

%package tcl
Summary:	XChat TCL plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description tcl
Provides tcl scripting capability to XChat.

%package autoaway
Summary:	XChat Autoaway plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description autoaway
Provides a autoaway function to XChat.

%if %build_netmon
%package netmonitor
Summary:	XChat Netmonitor plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description netmonitor
Net Monitor support for XChat.
%endif

%package notification
Summary:	XChat Notification plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description notification
Provides a notification area icon to XChat.

%package soundnotification
Summary:	XChat Sound Notification plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description soundnotification
Provides a sound notification to XChat.

%package notifyosd
Summary:	XChat On Screen Notification plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description notifyosd
Provides an on screen notification to XChat.

%package urlscraper
Summary:	XChat URLscraper plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}-%{release}

%description urlscraper
Provides capability to extract URLs from XChat conversations.

%prep
%setup -q
%patch0 -p1 -b .ctcp_version
%patch1 -p1 -b .config

%build
autoreconf
%configure2_5x  --disable-schemas-install \
		--enable-scrollkeeper \
		--disable-static \
		--with-plugins=autoaway,dbus,notification,notify-osd,url_scraper,sound-notification\
%if %build_perl
,perl\
%endif
%if %build_python
,python\
%endif
%if %build_tcl
,tcl\
%endif
%if %build_netmon
,net-monitor\
%endif
%if %build_plf
		--enable-socks
%endif

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

mv %{buildroot}%{_sysconfdir}/gconf/schemas/url_handler.schemas %{buildroot}%{_sysconfdir}/gconf/schemas/xchat_gnome_url_handler.schemas

mkdir -p %{buildroot}%{_includedir}
cp plugins/xchat-plugin.h %{buildroot}%{_includedir}/

%if !%build_netmon
rm -f %{buildroot}%{_libdir}/xchat-gnome/plugins/netmonitor.*
%endif

#nuke rpath
chrpath -d %{buildroot}%{_bindir}/*
chrpath -d %{buildroot}%{_libdir}/%{name}/plugins/notifyosd.so
chrpath -d %{buildroot}%{_libdir}/%{name}/plugins/autoaway.so

%find_lang xchat-gnome

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%post_install_gconf_schemas apps_xchat
%post_install_gconf_schemas xchat_gnome_url_handler
%update_scrollkeeper
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas apps_xchat
%preun_uninstall_gconf_schemas xchat_gnome_url_handler

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_scrollkeeper
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post notification
%post_install_gconf_schemas notification
%endif

%preun notification
%preun_uninstall_gconf_schemas notification

%if %mdkversion < 200900
%post urlscraper
%post_install_gconf_schemas urlscraper
%endif

%preun urlscraper
%preun_uninstall_gconf_schemas urlscraper

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS AUTHORS ChangeLog
%{_sysconfdir}/gconf/schemas/apps_xchat.schemas
%{_sysconfdir}/gconf/schemas/xchat_gnome_url_handler.schemas
%attr(755,root,root) %{_bindir}/xchat-gnome
%{_datadir}/applications/xchat-gnome.desktop
%{_datadir}/xchat-gnome
%{_datadir}/gnome/help/xchat-gnome
%{_datadir}/dbus-1/services/org.gnome.Xchat.service
%{_datadir}/omf/xchat-gnome
%{_iconsdir}/hicolor/*/apps/*
%dir %{_libdir}/xchat-gnome
%dir %{_libdir}/xchat-gnome/plugins
%{_mandir}/man1/xchat-gnome.*

%files devel
%defattr(-,root,root)
%{_includedir}/xchat-plugin.h

%if %build_perl
%files perl
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/perl.so
%{_libdir}/xchat-gnome/plugins/perl.la
%endif

%if %build_python
%files python
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/python.so
%{_libdir}/xchat-gnome/plugins/python.la
%endif

%if %build_tcl
%files tcl
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/tcl.so
%{_libdir}/xchat-gnome/plugins/tcl.la
%endif

%files autoaway
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/autoaway.so
%{_libdir}/xchat-gnome/plugins/autoaway.la

%if %build_netmon
%files netmonitor
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/netmonitor.so
%{_libdir}/xchat-gnome/plugins/netmonitor.la
%endif

%files notification
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/notification.so
%{_libdir}/xchat-gnome/plugins/notification.la
%{_sysconfdir}/gconf/schemas/notification.schemas

%files soundnotification
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/soundnotification.so
%{_libdir}/xchat-gnome/plugins/soundnotification.la

%files notifyosd
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/notifyosd.so
%{_libdir}/xchat-gnome/plugins/notifyosd.la

%files urlscraper
%defattr(-,root,root)
%{_libdir}/xchat-gnome/plugins/urlscraper.so
%{_libdir}/xchat-gnome/plugins/urlscraper.la
%{_sysconfdir}/gconf/schemas/urlscraper.schemas
