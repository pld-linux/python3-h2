#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	hyper-h2 - HTTP/2 protocol stack
Summary(pl.UTF-8):	hyper-h2 - stos protokołu HTTP/2
Name:		python3-h2
# beware of twisted compatibility (<5 in twisted 25.5.0)
Version:	4.4.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/h2/
Source0:	https://files.pythonhosted.org/packages/source/h/h2/h2-%{version}.tar.gz
# Source0-md5:	8ad21558fadb74bc42af25681c9ba7ef
URL:		https://pypi.org/project/h2/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:82
BuildRequires:	python3-wheel >= 0.46.3
%if %{with tests}
BuildRequires:	python3-hpack >= 4.2
BuildRequires:	python3-hpack < 5
BuildRequires:	python3-hyperframe >= 6.1
BuildRequires:	python3-hyperframe < 7
BuildRequires:	python3-hypothesis >= 6.119.4
BuildRequires:	python3-pytest >= 8.3.3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 7.4.7
%endif
Requires:	python3-modules >= 1:3.10
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
%py3_build_pyproject

%if %{with tests}
# test_changing_max_frame_size exceeds timeout
# test_range_of_acceptable_outputs: hypothesis error "The method ... was called from multiple different executors. This may lead to flaky tests and nonreproducible errors when replaying from database."
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_changing_max_frame_size and not test_range_of_acceptable_outputs'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/h2
%{py3_sitescriptdir}/h2-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,*.html,*.js}
%endif
