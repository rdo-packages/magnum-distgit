%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815afec729392386480e076dcc0dfe2d21c023c9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate os-api-ref
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service magnum

%global common_desc \
Magnum is an OpenStack project which provides a set of services for \
provisioning, scaling, and managing container orchestration engines.

Name:		openstack-%{service}
Summary:	Container Management project for OpenStack
Version:	17.0.1
Release:	1%{?dist}
License:	Apache-2.0
URL:		https://github.com/openstack/magnum.git

Source0:	https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

#

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
BuildRequires: pyproject-rpm-macros
BuildRequires: systemd-units
BuildRequires: openstack-macros

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
%{common_desc}

%package -n python3-%{service}
Summary: Magnum Python libraries

Requires: python3-osprofiler

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

BuildRequires:  graphviz

%description -n %{name}-doc
%{common_desc}

This package contains documentation files for Magnum.
%endif

# tests
%package -n python3-%{service}-tests
Summary:          Tests for OpenStack Magnum

Requires:        python3-%{service} = %{version}-%{release}

BuildRequires: python3-oslo-versionedobjects-tests
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

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# docs generation requires everything to be installed first
%if 0%{?with_doc}
%tox -e docs
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

PYTHONPATH=%{buildroot}/%{python3_sitelib} oslo-config-generator --config-file etc/%{service}/magnum-config-generator.conf --output-file %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
# The automatic value of pybasedir is wrong and unneeded and makes build to fail
sed -i "/#pybasedir.*/d" %{buildroot}%{_sysconfdir}/%{service}/magnum.conf


chmod 640 %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}

# Remove duplicate config directory /usr/etc/magnum, we are keeping config files at /etc/magnum
rmdir %{buildroot}%{_prefix}/etc/%{service}

%check
# Remove hacking tests, we don't need them
rm magnum/tests/unit/test_hacking.py
%tox -e %{default_toxenv}

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.dist-info
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
* Wed Oct 04 2023 RDO <dev@lists.rdoproject.org> 17.0.0-1
- Update to 17.0.0

* Fri Sep 15 2023 RDO <dev@lists.rdoproject.org> 17.0.0-0.1.0rc1
- Update to 17.0.0.0rc1

