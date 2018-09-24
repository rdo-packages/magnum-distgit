# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service magnum

%global common_desc \
Magnum is an OpenStack project which provides a set of services for \
provisioning, scaling, and managing container orchestration engines.

Name:		openstack-%{service}
Summary:	Container Management project for OpenStack
Version:	XXX
Release:	XXX
License:	ASL 2.0
URL:		https://github.com/openstack/magnum.git

Source0:	https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz

Source1:	%{service}.logrotate
Source2:	%{name}-api.service
Source3:	%{name}-conductor.service

BuildArch: noarch

BuildRequires: git
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-werkzeug
BuildRequires: systemd-units
BuildRequires: openstack-macros
# Required for config file generation
BuildRequires: python%{pyver}-pycadf
BuildRequires: python%{pyver}-osprofiler

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
%{common_desc}

%package -n python%{pyver}-%{service}
Summary: Magnum Python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}

Requires: python%{pyver}-pbr
Requires: python%{pyver}-babel
Requires: python%{pyver}-sqlalchemy
Requires: python%{pyver}-wsme
Requires: python%{pyver}-webob
Requires: python%{pyver}-alembic
Requires: python%{pyver}-docker >= 2.4.2
Requires: python%{pyver}-eventlet
Requires: python%{pyver}-iso8601
Requires: python%{pyver}-jsonpatch
Requires: python%{pyver}-keystonemiddleware >= 4.17.0
Requires: python%{pyver}-netaddr

Requires: python%{pyver}-oslo-concurrency >= 3.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-db >= 4.27.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-messaging >= 5.29.0
Requires: python%{pyver}-oslo-middleware >= 3.31.0
Requires: python%{pyver}-oslo-policy >= 1.30.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires: python%{pyver}-oslo-reports >= 1.18.0
Requires: python%{pyver}-osprofiler

Requires: python%{pyver}-pycadf
Requires: python%{pyver}-pecan

Requires: python%{pyver}-barbicanclient >= 4.5.2
Requires: python%{pyver}-glanceclient >= 1:2.8.0
Requires: python%{pyver}-heatclient >= 1.10.0
Requires: python%{pyver}-neutronclient >= 6.7.0
Requires: python%{pyver}-novaclient >= 9.1.0
Requires: python%{pyver}-kubernetes
Requires: python%{pyver}-keystoneclient >= 1:3.8.0
Requires: python%{pyver}-keystoneauth1 >= 3.4.0

Requires: python%{pyver}-cliff >= 2.8.0
Requires: python%{pyver}-requests
Requires: python%{pyver}-six
Requires: python%{pyver}-stevedore >= 1.20.0
Requires: python%{pyver}-taskflow
Requires: python%{pyver}-cryptography
Requires: python%{pyver}-werkzeug
Requires: python%{pyver}-marathon

# Handle python2 exception
%if %{pyver} == 2
Requires: PyYAML
Requires: python-decorator
Requires: python-enum34
%else
Requires: python%{pyver}-PyYAML
Requires: python%{pyver}-decorator
%endif


%description -n python%{pyver}-%{service}
%{common_desc}

%package common
Summary: Magnum common

Requires: python%{pyver}-%{service} = %{version}-%{release}

Requires(pre): shadow-utils

%description common
Components common to all OpenStack Magnum services

%package conductor
Summary: The Magnum conductor

Requires: %{name}-common = %{version}-%{release}

%{?systemd_requires}

%description conductor
OpenStack Magnum Conductor

%package api
Summary: The Magnum API

Requires: %{name}-common = %{version}-%{release}

%{?systemd_requires}

%description api
OpenStack-native ReST API to the Magnum Engine

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:    Documentation for OpenStack Magnum

Requires:    python%{pyver}-%{service} = %{version}-%{release}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  graphviz

%description -n %{name}-doc
%{common_desc}

This package contains documentation files for Magnum.
%endif

# tests
%package -n python%{pyver}-%{service}-tests
Summary:          Tests for OpenStack Magnum
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}

Requires:        python%{pyver}-%{service} = %{version}-%{release}

BuildRequires:   python%{pyver}-fixtures
BuildRequires:   python%{pyver}-hacking
BuildRequires:   python%{pyver}-mock
BuildRequires:   python%{pyver}-oslotest
BuildRequires:   python%{pyver}-os-testr
BuildRequires:   python%{pyver}-subunit
BuildRequires:   python%{pyver}-stestr
BuildRequires:   python%{pyver}-testscenarios
BuildRequires:   python%{pyver}-testtools
BuildRequires:   python%{pyver}-tempest

# copy-paste from runtime Requires
BuildRequires: python%{pyver}-babel
BuildRequires: python%{pyver}-sqlalchemy
BuildRequires: python%{pyver}-wsme
BuildRequires: python%{pyver}-webob
BuildRequires: python%{pyver}-alembic
BuildRequires: python%{pyver}-docker >= 2.4.2
BuildRequires: python%{pyver}-eventlet
BuildRequires: python%{pyver}-iso8601
BuildRequires: python%{pyver}-jsonpatch
BuildRequires: python%{pyver}-keystonemiddleware
BuildRequires: python%{pyver}-netaddr

BuildRequires: python%{pyver}-oslo-concurrency
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-oslo-context
BuildRequires: python%{pyver}-oslo-db
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-messaging
BuildRequires: python%{pyver}-oslo-middleware
BuildRequires: python%{pyver}-oslo-policy
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-service
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-versionedobjects
BuildRequires: python%{pyver}-oslo-versionedobjects-tests
BuildRequires: python%{pyver}-oslo-reports

BuildRequires: python%{pyver}-pecan

BuildRequires: python%{pyver}-barbicanclient
BuildRequires: python%{pyver}-glanceclient
BuildRequires: python%{pyver}-heatclient
BuildRequires: python%{pyver}-neutronclient
BuildRequires: python%{pyver}-novaclient
BuildRequires: python%{pyver}-kubernetes
BuildRequires: python%{pyver}-keystoneclient

BuildRequires: python%{pyver}-requests
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-stevedore
BuildRequires: python%{pyver}-taskflow
BuildRequires: python%{pyver}-cryptography
BuildRequires: python%{pyver}-marathon

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: PyYAML
BuildRequires: python-decorator
BuildRequires: python-enum34
%else
BuildRequires: python%{pyver}-PyYAML
BuildRequires: python%{pyver}-decorator
%endif

%description -n python%{pyver}-%{service}-tests
%{common_desc}

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -rf {test-,}requirements{-bandit,}.txt tools/{pip,test}-requires

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

%build
%{pyver_build}

%install
%{pyver_install}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/%{service}/
mkdir -p %{buildroot}%{_localstatedir}/run/%{service}/
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# install systemd unit files
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-conductor.service

mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/
mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/certificates/
mkdir -p %{buildroot}%{_sysconfdir}/%{service}/

oslo-config-generator-%{pyver} --config-file etc/%{service}/magnum-config-generator.conf --output-file %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}

# Remove duplicate config directory /usr/etc/magnum, we are keeping config files at /etc/magnum
rmdir %{buildroot}%{_prefix}/etc/%{service}

%check
# Remove hacking tests, we don't need them
rm magnum/tests/unit/test_hacking.py
stestr-%{pyver} --test-path=./magnum/tests/unit run

%files -n python%{pyver}-%{service}
%license LICENSE
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%exclude %{pyver_sitelib}/%{service}/tests


%files common
%{_bindir}/magnum-db-manage
%{_bindir}/magnum-driver-manage
%license LICENSE
%dir %attr(0750,%{service},root) %{_localstatedir}/log/%{service}
%dir %attr(0755,%{service},root) %{_localstatedir}/run/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}/certificates
%dir %attr(0755,%{service},root) %{_sysconfdir}/%{service}
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/magnum.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%pre common
# 1870:1870 for magnum - rhbz#845078
getent group %{service} >/dev/null || groupadd -r --gid 1870 %{service}
getent passwd %{service}  >/dev/null || \
useradd --uid 1870 -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
-c "OpenStack Magnum Daemons" %{service}
exit 0


%files conductor
%doc README.rst
%license LICENSE
%{_bindir}/magnum-conductor
%{_unitdir}/%{name}-conductor.service

%post conductor
%systemd_post %{name}-conductor.service

%preun conductor
%systemd_preun %{name}-conductor.service

%postun conductor
%systemd_postun_with_restart %{name}-conductor.service


%files api
%doc README.rst
%license LICENSE
%{_bindir}/magnum-api
%{_unitdir}/%{name}-api.service


%if 0%{?with_doc}
%files -n %{name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests

%post api
%systemd_post %{name}-api.service

%preun api
%systemd_preun %{name}-api.service

%postun api
%systemd_postun_with_restart %{name}-api.service

%changelog
