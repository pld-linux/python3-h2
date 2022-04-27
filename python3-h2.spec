#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	hyper-h2 - HTTP/2 protocol stack
Summary(pl.UTF-8):	hyper-h2 - stos protokołu HTTP/2
Name:		python3-h2
# beware of twisted compatibility
Version:	4.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/h2/
Source0:	https://files.pythonhosted.org/packages/source/h/h2/h2-%{version}.tar.gz
# Source0-md5:	4274f9619c0a43bb4ae01b6b02bf0c99
URL:		https://pypi.org/project/h2/
BuildRequires:	python3-modules >= 1:3.6.1
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hpack >= 4.0
BuildRequires:	python3-hpack < 5
BuildRequires:	python3-hyperframe >= 6.0
BuildRequires:	python3-hyperframe < 7
BuildRequires:	python3-hypothesis >= 5.5
BuildRequires:	python3-pytest >= 6.0.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg >= 4.0.2
%endif
Requires:	python3-modules >= 1:3.6.1
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
%py3_build

%if %{with tests}
# test_changing_max_frame_size exceeds timeout
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest test -k 'not test_changing_max_frame_size'
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/h2
%{py3_sitescriptdir}/h2-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,*.html,*.js}
%endif
