#Module-Specific definitions
%define mod_name mod_vhost_hash_alias
%define mod_conf 42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache HTTPD module for mass virtual hosting
Name:		apache-%{mod_name}
Version:	1.0
Release:	14
Group:		System/Servers
License:	LGPL
URL:		https://weuh.org/projects/mod_vhost_hash_alias/
Source0: 	mod-vhost-hash-alias-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	mhash-devel
Epoch:		1

%description
mod_vhost_hash_alias is an Apache HTTPD module that allows mass hosting with
good distribution across a unified directory namespace. Administrators no
longer have to use complex regexps with mod_rewrite, since they can use
mod_vhost_hash_alias to do a better job and use fewer resources.
mod_vhost_hash_alias is a component of the VHFFS hosting platform which is
used by the Web hosting provider Tuxfamily.org.

%prep

%setup -q -n mod-vhost-hash-alias-%{version}
sed -i s/HashDigest/HashType/ README

%build
export APR_CONFIG="%{_bindir}/apr-1-config"

%configure2_5x --localstatedir=/var/lib \
    --with-apxs2=%{_bindir}/apxs

%make

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS ChangeLog README INSTALL NEWS TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-14mdv2011.0
+ Revision: 678436
- mass rebuild

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 1:1.0-13mdv2011.0
+ Revision: 605254
- Rebuild with apr with workaround to issue with gcc type based

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-12mdv2011.0
+ Revision: 588081
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-11mdv2010.1
+ Revision: 516231
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-10mdv2010.0
+ Revision: 406678
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-9mdv2009.1
+ Revision: 326271
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-8mdv2009.0
+ Revision: 235122
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-7mdv2009.0
+ Revision: 215666
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 1:1.0-6mdv2008.1
+ Revision: 135823
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-6mdv2008.0
+ Revision: 83413
- fix deps
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2007.1
+ Revision: 140772
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-4mdv2007.1
+ Revision: 79545
- Import apache-mod_vhost_hash_alias

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-4mdv2007.0
- rebuild

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-3mdk
- really rebuilt against apache-2.2.0

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-2mdk
- rebuilt against apache-2.2.0
- fix the config

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-1mdk
- fix versioning

* Thu Sep 22 2005 Pascal Terjan <pterjan@mandriva.org> 2.0.54_1.0-2mdk
- fix URL

* Thu Sep 22 2005 Pascal Terjan <pterjan@mandriva.org> 2.0.54_1.0-1mdk
- first Mandriva package

