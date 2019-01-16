%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service magnum

%global common_desc \
Magnum is an OpenStack project which provides a set of services for \
provisioning, scaling, and managing container orchestration engines.

Name:		openstack-%{service}
Summary:	Container Management project for OpenStack
Version:	7.1.0
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://github.com/openstack/magnum.git

Source0:	https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz

Source1:	%{service}.logrotate
Source2:	%{name}-api.service
Source3:	%{name}-conductor.service

BuildArch: noarch

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python2-pbr
BuildRequires: python2-setuptools
BuildRequires: python-werkzeug
BuildRequires: systemd-units
BuildRequires: openstack-macros
# Required for config file generation
BuildRequires: python2-pycadf
BuildRequires: python2-osprofiler

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
%{common_desc}

%package -n python-%{service}
Summary: Magnum Python libraries

Requires: python2-pbr
Requires: python2-babel
Requires: PyYAML
Requires: python2-sqlalchemy
Requires: python2-wsme
Requires: python-webob
Requires: python2-alembic
Requires: python-decorator
Requires: python2-docker >= 2.4.2
Requires: python-enum34
Requires: python2-eventlet
Requires: python2-iso8601
Requires: python2-jsonpatch
Requires: python2-keystonemiddleware >= 4.17.0
Requires: python2-netaddr

Requires: python2-octaviaclient >= 1.6.0
Requires: python2-oslo-concurrency >= 3.26.0
Requires: python2-oslo-config >= 2:5.2.0
Requires: python2-oslo-context >= 2.19.2
Requires: python2-oslo-db >= 4.27.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-messaging >= 5.29.0
Requires: python2-oslo-middleware >= 3.31.0
Requires: python2-oslo-policy >= 1.30.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-service >= 1.24.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-oslo-versionedobjects >= 1.31.2
Requires: python2-oslo-reports >= 1.18.0
Requires: python2-osprofiler

Requires: python2-pycadf
Requires: python2-pecan

Requires: python2-barbicanclient >= 4.5.2
Requires: python2-glanceclient >= 1:2.8.0
Requires: python2-heatclient >= 1.10.0
Requires: python2-neutronclient >= 6.7.0
Requires: python2-novaclient >= 9.1.0
Requires: python2-kubernetes
Requires: python2-keystoneclient >= 1:3.8.0
Requires: python2-keystoneauth1 >= 3.4.0

Requires: python2-cliff >= 2.8.0
Requires: python2-requests
Requires: python2-six
Requires: python2-stevedore >= 1.20.0
Requires: python2-taskflow
Requires: python2-cryptography
Requires: python-werkzeug
Requires: python2-marathon


%description -n python-%{service}
%{common_desc}

%package common
Summary: Magnum common

Requires: python-%{service} = %{version}-%{release}

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

Requires:    python-%{service} = %{version}-%{release}

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-stevedore
BuildRequires:  graphviz

%description -n %{name}-doc
%{common_desc}

This package contains documentation files for Magnum.
%endif

# tests
%package -n python-%{service}-tests
Summary:          Tests for OpenStack Magnum

Requires:        python-%{service} = %{version}-%{release}

BuildRequires:   python2-fixtures
BuildRequires:   python2-hacking
BuildRequires:   python2-mock
BuildRequires:   python2-oslotest
BuildRequires:   python2-os-testr
BuildRequires:   python2-subunit
BuildRequires:   python2-stestr
BuildRequires:   python2-testscenarios
BuildRequires:   python2-testtools
BuildRequires:   python2-tempest

# copy-paste from runtime Requires
BuildRequires: python2-babel
BuildRequires: PyYAML
BuildRequires: python2-sqlalchemy
BuildRequires: python2-wsme
BuildRequires: python-webob
BuildRequires: python2-alembic
BuildRequires: python-decorator
BuildRequires: python2-docker >= 2.4.2
BuildRequires: python-enum34
BuildRequires: python2-eventlet
BuildRequires: python2-iso8601
BuildRequires: python2-jsonpatch
BuildRequires: python2-keystonemiddleware
BuildRequires: python2-netaddr

BuildRequires: python2-octaviaclient
BuildRequires: python2-oslo-concurrency
BuildRequires: python2-oslo-config
BuildRequires: python2-oslo-context
BuildRequires: python2-oslo-db
BuildRequires: python2-oslo-i18n
BuildRequires: python2-oslo-log
BuildRequires: python2-oslo-messaging
BuildRequires: python2-oslo-middleware
BuildRequires: python2-oslo-policy
BuildRequires: python2-oslo-serialization
BuildRequires: python2-oslo-service
BuildRequires: python2-oslo-utils
BuildRequires: python2-oslo-versionedobjects
BuildRequires: python2-oslo-versionedobjects-tests
BuildRequires: python2-oslo-reports

BuildRequires: python2-pecan

BuildRequires: python2-barbicanclient
BuildRequires: python2-glanceclient
BuildRequires: python2-heatclient
BuildRequires: python2-neutronclient
BuildRequires: python2-novaclient
BuildRequires: python2-kubernetes
BuildRequires: python2-keystoneclient

BuildRequires: python2-requests
BuildRequires: python2-six
BuildRequires: python2-stevedore
BuildRequires: python2-taskflow
BuildRequires: python2-cryptography
BuildRequires: python2-marathon

%description -n python-%{service}-tests
%{common_desc}

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -rf {test-,}requirements{-bandit,}.txt tools/{pip,test}-requires

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
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

oslo-config-generator --config-file etc/%{service}/magnum-config-generator.conf --output-file %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}

# Remove duplicate config directory /usr/etc/magnum, we are keeping config files at /etc/magnum
rmdir %{buildroot}%{_prefix}/etc/%{service}

%check
# Remove hacking tests, we don't need them
rm magnum/tests/unit/test_hacking.py
stestr --test-path=./magnum/tests/unit run

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


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

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%post api
%systemd_post %{name}-api.service

%preun api
%systemd_preun %{name}-api.service

%postun api
%systemd_postun_with_restart %{name}-api.service

%changelog
* Wed Jan 16 2019 RDO <dev@lists.rdoproject.org> 7.1.0-1
- Update to 7.1.0

* Wed Oct 31 2018 RDO <dev@lists.rdoproject.org> 7.0.2-1
- Update to 7.0.2

* Fri Aug 24 2018 RDO <dev@lists.rdoproject.org> 7.0.1-1
- Update to 7.0.1

* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 7.0.0-1
- Update to 7.0.0
