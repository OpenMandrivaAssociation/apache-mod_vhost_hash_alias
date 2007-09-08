#Module-Specific definitions
%define mod_name mod_vhost_hash_alias
%define mod_conf 42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache HTTPD module for mass virtual hosting
Name:		apache-%{mod_name}
Version:	1.0
Release:	%mkrel 6
Group:		System/Servers
License:	LGPL
URL:		http://weuh.org/projects/mod_vhost_hash_alias/
Source0: 	mod-vhost-hash-alias-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libmhash-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%configure2_5x \
    --with-apxs2=%{_sbindir}/apxs

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL NEWS TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


