#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	hyper-h2 - HTTP/2 protocol stack
Summary(pl.UTF-8):	hyper-h2 - stos protokołu HTTP/2
Name:		python-h2
Version:	3.2.0
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/h2/
Source0:	https://files.pythonhosted.org/packages/source/h/h2/h2-%{version}.tar.gz
# Source0-md5:	197a99c09f344a0dd987fab9801dc8d0
URL:		https://pypi.org/project/h2/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-enum34 < 2
BuildRequires:	python-hpack >= 3.0
BuildRequires:	python-hpack < 4
BuildRequires:	python-hyperframe >= 5.2.0
BuildRequires:	python-hyperframe < 6
BuildRequires:	python-hypothesis
BuildRequires:	python-pytest
# >= 4.6.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hpack >= 3.0
BuildRequires:	python3-hpack < 4
BuildRequires:	python3-hyperframe >= 5.2.0
BuildRequires:	python3-hyperframe < 6
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
# >= 4.6.5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is a pure-Python implementation of a HTTP/2 protocol
stack. It's written from the ground up to be embeddable in whatever
program you choose to use, ensuring that you can speak HTTP/2
regardless of your programming paradigm.

%description -l pl.UTF-8
Ten pakiet to czysto pythonowa implementacja stosu protokołu HTTP/2.
Jest napisana od podstaw tak, aby była osadzalna w dowolnym programie,
zapewniając obsługę HTTP/2 niezależnie od paradygmatu programowania.

%package -n python3-h2
Summary:	hyper-h2 - HTTP/2 protocol stack
Summary(pl.UTF-8):	hyper-h2 - stos protokołu HTTP/2
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-h2
This package is a pure-Python implementation of a HTTP/2 protocol
stack. It's written from the ground up to be embeddable in whatever
program you choose to use, ensuring that you can speak HTTP/2
regardless of your programming paradigm.

%description -n python3-h2 -l pl.UTF-8
Ten pakiet to czysto pythonowa implementacja stosu protokołu HTTP/2.
Jest napisana od podstaw tak, aby była osadzalna w dowolnym programie,
zapewniając obsługę HTTP/2 niezależnie od paradygmatu programowania.

%package apidocs
Summary:	API documentation for Python h2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona h2
Group:		Documentation

%description apidocs
API documentation for Python h2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona h2.

%prep
%setup -q -n h2-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest test
%endif
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst HISTORY.rst LICENSE README.rst
%{py_sitescriptdir}/h2
%{py_sitescriptdir}/h2-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-h2
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/h2
%{py3_sitescriptdir}/h2-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_modules,_static,*.html,*.js}
%endif
