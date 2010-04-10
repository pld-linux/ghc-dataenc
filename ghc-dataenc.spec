%define	pkgname	dataenc
Summary:	Data encoding library
Name:		ghc-%{pkgname}
Version:	0.13.0.2
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	65f6e8fdbc0adef572afdacd2c492289
URL:		http://hackage.haskell.org/package/%{pkgname}/
BuildRequires:	ghc >= 6.10
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		libsubdir	ghc-%(/usr/bin/ghc --numeric-version)/%{pkgname}-%{version}

%description
Data encoding library currently providing Base16, Base32,
Base32Hex, Base64, Base64Url, Base85, Python string escaping,
Quoted-Printable, URL encoding, uuencode, xxencode, and yEncoding.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--libsubdir=%{libsubdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{libsubdir}/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/ghc-pkg update %{_libdir}/%{libsubdir}/%{pkgname}.conf

%postun
if [ "$1" = "0" ]; then
	/usr/bin/ghc-pkg unregister %{pkgname}-%{version}
fi

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/html
%{_libdir}/%{libsubdir}
