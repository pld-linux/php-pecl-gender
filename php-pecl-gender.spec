%define		_modname	gender
%define		_status		stable
Summary:	%{_modname} - determine gender for a given name
Summary(pl.UTF-8):	%{_modname} - określenie płci dla podanego imienia
Name:		php-pecl-%{_modname}
Version:	0.6.1
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	0641eebf38dfe6d4d83a879189230658
URL:		http://pecl.php.net/package/gender/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gender PHP extension is a port of the gender.c program originally
written by Joerg Michael. The main purpose is to find out the gender
of first names. The actual database contains >40000 first names from
54 countries.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie gender to port programu gender.c, autorem którego jest
Joerg Michael. Celem programu jest określenie płci na podstawie
podanych imion. Aktualna baza danych zawiera ponad 40000 imion z ponad
54 krajów.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_pear_dir}/data/gender/data}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

install data/nam_dict.txt.bz2 $RPM_BUILD_ROOT%{php_pear_dir}/data/gender/data

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
%{php_pear_dir}/data/gender
