%define		php_name	php%{?php_suffix}
%define		modname	gender
%define		status		stable
Summary:	%{modname} - determine gender for a given name
Summary(pl.UTF-8):	%{modname} - określenie płci dla podanego imienia
Name:		%{php_name}-pecl-%{modname}
Version:	0.7.0
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	ac54fe38f3ae6c67f55e84b81354403e
URL:		http://pecl.php.net/package/gender/
BuildRequires:	%{php_name}-devel >= 3:5.2.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.2.0
Suggests:	php-bzip2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gender PHP extension is a port of the gender.c program originally
written by Joerg Michael. The main purpose is to find out the gender
of first names. The actual database contains >40000 first names from
54 countries.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie gender to port programu gender.c, autorem którego jest
Joerg Michael. Celem programu jest określenie płci na podstawie
podanych imion. Aktualna baza danych zawiera ponad 40000 imion z ponad
54 krajów.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_pear_dir}/data/gender}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

install data/nam_dict.txt.bz2 $RPM_BUILD_ROOT%{php_pear_dir}/data/gender

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{php_pear_dir}/data/gender
