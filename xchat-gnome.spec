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

%define name	xchat-gnome
%define version	0.16
%define rel	1
%define main_summary	Graphical IRC client for the GNOME desktop 
%define perl_version	%(rpm -q --qf '%%{epoch}:%%{VERSION}' perl)
%define iconname xchat-gnome.png 

%if %build_plf
%define distsuffix plf
%endif 

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	%{main_summary}
Group:		Networking/IRC
License:	GPL
Url:		http://xchat-gnome.navi.cx/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Source:		http://flapjack.navi.cx/releases/xchat-gnome/%{name}-%{version}.tar.bz2 

# do not give away OS with VERSION
Patch0:		xchat-gnome-0.12-ctcp_version.patch

# use mozilla-firefox instead of firefox
# not needed(?)
#Patch4:		xchat-2.4.1-firefox.patch.bz2

BuildRequires:	bison
Buildrequires:	gtk+2-devel
BuildRequires:	openssl-devel
BuildRequires:  ImageMagick
BuildRequires:	GConf2
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libnotify-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  scrollkeeper
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	libnotify-devel
BuildRequires:	libsexy-devel
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
BuildRequires:	libtool
BuildRequires:	automake1.8
BuildRequires:	libxslt-proc
BuildRequires:	desktop-file-utils
Provides:	xchat-gnome-dbus = %version-%release
Obsoletes:	xchat-gnome-dbus < 0.15
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%description
XChat-gnome is a new frontend to the popular X-Chat IRC client which is
designed with the user interface foremost in mind. Historically, the OSS
desktop has been steadily improving in usability, accessibility, and general
slickness, yet the world of IRC clients has not kept up. With IRC being one
of the fundamental methods of communication within the open source community,
it is bizzare that this area has been neglected.

Build Options:
--with plf        Enable SOCKS5 support (need to download from PLF)
--witht perl      Enable Perl plugin
--with python     Enable Python plugin 
--with tcl        Enable TCL plugin 
--with netmon     Enable Net Monitor plugin 

%package devel
Summary:	XChat header for plugin development
Group:          Networking/IRC

%description devel
This package contains xchat-plugin.h needed to build external plugins.

%package perl
Summary:	XChat Perl plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}
Requires:	perl-base = %perl_version

%description perl
Provides Perl scripting capability to XChat.

%package python
Summary:	XChat Python plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description python
Provides Python scripting capability to XChat.

%package tcl
Summary:	XChat TCL plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description tcl
Provides tcl scripting capability to XChat.

%package autoaway
Summary:	XChat Autoaway plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description autoaway
Provides a autoaway function to XChat.

%if %build_netmon
%package netmonitor
Summary:	XChat Netmonitor plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description netmonitor
Net Monitor support for XChat.
%endif

%package notification
Summary:	XChat Notification plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description notification
Provides a notification area icon to XChat.

%package soundnotification
Summary:        XChat Sound Notification plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}

%description soundnotification
Provides a sound notification to XChat.

%package notifyosd
Summary:	XChat On Screen Notification plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description notifyosd
Provides an on screen notification to XChat.

%package urlscraper
Summary:	XChat URLscraper plugin
Group:		Networking/IRC
Requires:	%{name} = %{version}

%description urlscraper
Provides capability to extract URLs from XChat conversations.

%prep
%setup -q
%patch0 -p1 -b .ctcp_version
#%patch4 -p0 -b .firefox

%build

%configure2_5x  --disable-schemas-install \
		--disable-scrollkeeper \
		--with-plugins=autoaway,notification,notify-osd,url_scraper,sound-notification\
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

%find_lang xchat-gnome

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
install -D data/icons/hicolor/48x48/apps/xchat-gnome.png %{buildroot}%{_liconsdir}/%{iconname}
install -D data/icons/hicolor/scalable/apps/xchat-gnome-plugin.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/xchat-gnome.svg
install -D data/icons/hicolor/48x48/apps/xchat-gnome.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/xchat-gnome.png
install -D data/icons/hicolor/128x128/apps/xchat-gnome.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/xchat-gnome.png

convert data/icons/hicolor/128x128/apps/xchat-gnome.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{iconname}
convert data/icons/hicolor/128x128/apps/xchat-gnome.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{iconname}

cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%name): needs="x11" \
	section="Internet/Chat" \
	title="XChat-GNOME IRC Chat" \
	longtitle="%{main_summary}" \
	command="%{_bindir}/%{name}" \
	icon="%{name}.png" \
	xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="IRCClient" \
  --add-category="X-MandrivaLinux-Internet-Chat" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %{buildroot}%{_includedir}
cp plugins/xchat-plugin.h %{buildroot}%{_includedir}/

rm -f %{buildroot}%{_libdir}/xchat-gnome/plugins/*.a
%if !%build_netmon
rm -f %{buildroot}%{_libdir}/xchat-gnome/plugins/netmonitor.*
%endif


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/apps_xchat.schemas > /dev/null
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/xchat_gnome_url_handler.schemas > /dev/null
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q || true ; fi
gtk-update-icon-cache --force --quiet %{_iconsdir}/hicolor

%{update_menus}
%if %mdkversion >= 200700
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%preun
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/apps_xchat.schemas > /dev/null
gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/xchat_gnome_url_handler.schemas > /dev/null
if [ "$1" = "0" -a -x %{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --force --quiet %{_iconsdir}/hicolor
fi

%postun
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q || true ; fi

%{clean_menus}
%if %mdkversion >= 200700
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%post notification
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/notification.schemas > /dev/null

%preun notification
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/notification.schemas > /dev/null


%post urlscraper
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/urlscraper.schemas > /dev/null

%preun urlscraper
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/urlscraper.schemas > /dev/null


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f xchat-gnome.lang
%defattr(-,root,root)
%doc README ChangeLog COPYING
%{_sysconfdir}/gconf/schemas/apps_xchat.schemas
%{_sysconfdir}/gconf/schemas/xchat_gnome_url_handler.schemas
%{_bindir}/xchat-gnome
%{_datadir}/applications/xchat-gnome.desktop
%{_datadir}/xchat-gnome
%{_datadir}/gnome/help/xchat-gnome
%{_datadir}/dbus-1/services/org.gnome.Xchat.service
%{_datadir}/omf/xchat-gnome
%{_menudir}/*
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/%{iconname}
%{_liconsdir}/%{iconname}
%{_miconsdir}/%{iconname}
%dir %{_libdir}/xchat-gnome
%dir %{_libdir}/xchat-gnome/plugins
%{_mandir}/man1/xchat-gnome.1.bz2

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


