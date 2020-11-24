%{?python_enable_dependency_generator}

Name:           electrum
Version:	4.0.5
Release:	1
Summary:        A lightweight Bitcoin Client

License:        MIT
URL:            https://electrum.org/
Source0:        https://download.electrum.org/%{version}/Electrum-%{version}.tar.gz
Source1:        https://download.electrum.org/%{version}/Electrum-%{version}.tar.gz.asc
#Wed Feb 01 2017, exported the upstream gpg key using the command:
#gpg2 --export --export-options export-minimal 6694D8DE7BE8EE5631BED9502BD5824B7F9470E6 > gpgkey-electrum.gpg
Source2:        gpgkey-electrum.gpg
Source3:        electrum.appdata.xml

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-qt5-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

BuildRequires:  appstream-util
BuildRequires:  gnupg2
Requires:       python-qt5
Requires:       python-crytography
Requires:       python-pycryptodomex
Conflicts:      python3-trezor < 0.11.2

%description
Electrum is an easy to use Bitcoin client. It protects you from losing
coins in a backup mistake or computer failure, because your wallet can
be recovered from a secret phrase that you can write on paper or learn
by heart. There is no waiting time when you start the client, because
it does not download the Bitcoin block chain.

%prep
gpgv --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%setup -q -n Electrum-%{version}
rm -rf Electrum.egg-info
rm -rf packages

#qdarkstyle is an optional dependency that is not yet packed for Fedora
sed -i '/^qdarkstyle*/d' ./contrib/requirements/requirements.txt

%build
%{py3_build}

%install
%{py3_install}
install -Dpm 644 %{SOURCE3} %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
# Source: dmalcolm.fedorapeople.org/python3.spec
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# Install Desktop file, fix categories
desktop-file-install                                    \
--remove-category="Network"                             \
--add-category="Office"                                 \
--add-category="Finance"                                \
--delete-original                                       \
--dir=%{buildroot}%{_datadir}/applications              \
%{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%files -f %{name}.lang
%doc AUTHORS
%doc README.rst
%doc RELEASE-NOTES
%doc PKG-INFO
%license LICENCE
%{_bindir}/electrum
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{python3_sitelib}/*
