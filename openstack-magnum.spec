%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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

Source0:	https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source1:	%{service}.logrotate
Source2:	%{name}-api.service
Source3:	%{name}-conductor.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: python3-pbr
BuildRequires: python3-setuptools
BuildRequires: python3-werkzeug
BuildRequires: systemd-units
BuildRequires: openstack-macros
# Required for config file generation
BuildRequires: python3-pycadf
BuildRequires: python3-osprofiler

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
%{common_desc}

%package -n python3-%{service}
Summary: Magnum Python libraries
%{?python_provide:%python_provide python3-%{service}}

Requires: python3-pbr >= 5.5.0
Requires: python3-sqlalchemy >= 1.2.0
Requires: python3-wsme >= 0.8.0
Requires: python3-webob >= 1.8.1
Requires: python3-alembic >= 0.9.6
Requires: python3-docker >= 4.3.0
Requires: python3-eventlet >= 0.28.0
Requires: python3-iso8601 >= 0.1.11
Requires: python3-jsonpatch >= 1.16
Requires: python3-keystonemiddleware >= 9.0.0
Requires: python3-netaddr >= 0.7.18

Requires: python3-oslo-concurrency >= 4.1.0
Requires: python3-oslo-config >= 2:8.1.0
Requires: python3-oslo-context >= 3.1.0
Requires: python3-oslo-db >= 8.2.0
Requires: python3-oslo-i18n >= 5.0.0
Requires: python3-oslo-log >= 4.2.0
Requires: python3-oslo-messaging >= 12.2.0
Requires: python3-oslo-middleware >= 4.1.0
Requires: python3-oslo-policy >= 3.6.0
Requires: python3-oslo-service >= 2.2.0
Requires: python3-oslo-utils >= 4.2.0
Requires: python3-oslo-versionedobjects >= 2.1.0
Requires: python3-oslo-reports >= 2.1.0
Requires: python3-oslo-upgradecheck >= 1.3.0
Requires: python3-osprofiler

Requires: python3-pycadf >= 1.1.0
Requires: python3-pecan >= 1.3.3

Requires: python3-barbicanclient >= 5.0.0
Requires: python3-glanceclient >= 1:3.2.0
Requires: python3-heatclient >= 2.2.0
Requires: python3-neutronclient >= 7.2.0
Requires: python3-novaclient >= 17.2.0
Requires: python3-keystoneclient >= 1:3.20.0
Requires: python3-keystoneauth1 >= 3.14.0
Requires: python3-octaviaclient >= 2.1.0
Requires: python3-cinderclient >= 7.1.0

Requires: python3-cliff >= 2.8.0
Requires: python3-requests >= 2.20.1
Requires: python3-six >= 1.10.0
Requires: python3-stevedore >= 3.3.0
Requires: python3-taskflow >= 2.16.0
Requires: python3-cryptography >= 2.1.4
Requires: python3-werkzeug >= 0.9

Requires: python3-decorator >= 3.4.0
Requires: python3-setuptools >= 30.0.0
Requires: python3-yaml >= 3.13
Requires: python3-oslo-serialization >= 3.2.0


%description -n python3-%{service}
%{common_desc}

%package common
Summary: Magnum common

Requires: python3-%{service} = %{version}-%{release}

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

Requires:    python3-%{service} = %{version}-%{release}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-stevedore
BuildRequires:  graphviz

%description -n %{name}-doc
%{common_desc}

This package contains documentation files for Magnum.
%endif

# tests
%package -n python3-%{service}-tests
Summary:          Tests for OpenStack Magnum
%{?python_provide:%python_provide python3-%{service}-tests}

Requires:        python3-%{service} = %{version}-%{release}

BuildRequires:   python3-fixtures
BuildRequires:   python3-hacking
BuildRequires:   python3-mock
BuildRequires:   python3-oslotest
BuildRequires:   python3-os-testr
BuildRequires:   python3-subunit
BuildRequires:   python3-stestr
BuildRequires:   python3-testscenarios
BuildRequires:   python3-testtools
BuildRequires:   python3-webtest

# copy-paste from runtime Requires
BuildRequires: python3-sqlalchemy
BuildRequires: python3-wsme
BuildRequires: python3-webob
BuildRequires: python3-alembic
BuildRequires: python3-docker
BuildRequires: python3-eventlet
BuildRequires: python3-iso8601
BuildRequires: python3-jsonpatch
BuildRequires: python3-keystonemiddleware
BuildRequires: python3-netaddr

BuildRequires: python3-oslo-concurrency
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-context
BuildRequires: python3-oslo-db
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-messaging
BuildRequires: python3-oslo-middleware
BuildRequires: python3-oslo-policy
BuildRequires: python3-oslo-service
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-versionedobjects
BuildRequires: python3-oslo-versionedobjects-tests
BuildRequires: python3-oslo-reports
BuildRequires: python3-oslo-upgradecheck

BuildRequires: python3-pecan

BuildRequires: python3-barbicanclient
BuildRequires: python3-glanceclient
BuildRequires: python3-heatclient
BuildRequires: python3-neutronclient
BuildRequires: python3-novaclient
BuildRequires: python3-keystoneclient
BuildRequires: python3-octaviaclient
BuildRequires: python3-cinderclient

BuildRequires: python3-requests
BuildRequires: python3-requests-mock
BuildRequires: python3-six
BuildRequires: python3-stevedore
BuildRequires: python3-taskflow
BuildRequires: python3-cryptography
BuildRequires: python3-marathon

BuildRequires: python3-PyYAML
BuildRequires: python3-decorator
BuildRequires: vim
Requires: vim

%description -n python3-%{service}-tests
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -rf {test-,}requirements{-bandit,}.txt tools/{pip,test}-requires

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

%build
%{py3_build}

%install
%{py3_install}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
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
PYTHON=%{__python3} stestr --test-path=./magnum/tests/unit run --concurrency 1

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%exclude %{python3_sitelib}/%{service}/tests


%files common
%{_bindir}/magnum-db-manage
%{_bindir}/magnum-driver-manage
%{_bindir}/magnum-status
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
%{_bindir}/magnum-api-wsgi
%{_unitdir}/%{name}-api.service


%if 0%{?with_doc}
%files -n %{name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%post api
%systemd_post %{name}-api.service

%preun api
%systemd_preun %{name}-api.service

%postun api
%systemd_postun_with_restart %{name}-api.service

%changelog
