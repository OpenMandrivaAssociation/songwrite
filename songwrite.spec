%global oname Songwrite3
%global name	%(echo %oname | tr [:upper:] [:lower:])
%global mod		%(m=%{oname}; echo ${m:0:1})

Summary:	Guitar tabulature editor with playing and printing
Name:		%{name}
Version:	0.2
Release:	2
License:	GPLv3
Group:		Sound
Source0:	https://pypi.io/packages/source/%{mod}/%{oname}/%{oname}-%{version}.tar.gz
Url:		https://pypi.org/project/Songwrite3/
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)

#Requires:	pythonegg(editobj2)
Requires:	TiMidity++
Requires:	lilypond
Requires:	hicolor-icon-theme

BuildArch:	noarch
%rename		songwrite

%description
Songwrite2 is a tablature (guitar partition) editor. It's the successor of
songwrite. Songwrite2 is coded in Python and uses Tk (Tkinter); it relies on
Timidity to play midi and on GNU Lilypond for printing.

%files -f %{name}.lang
%license LICENSE.txt
%doc README.rst CHANGES AUTHORS doc/*
%{_bindir}/%{name}
%{py3_puresitedir}/%{name}
%{py3_puresitedir}/*.egg-info/
#%%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/*.appdata.xml
#%%{_docdir}/%{name}/{en,fr}
#%%{_docdir}/%{name}/*xml
%{_mandir}/man1/%{name}.1.*

#-----------------------------------------------------------------------

%prep
%autosetup -n %{oname}-%{version}

%build
%py_build

%install
%py_install

# fix shebang
sed -i 's|#!/usr/bin/python -s -O|#!/usr/bin/python -s|' %{buildroot}%{_bindir}/*

# docs
rm -fr %{buildroot}%{py3_puresitedir}/%{name}/doc/
touch %{buildroot}%{py3_puresitedir}/%{name}/doc
ln -fs %{_docdir}/%{name} %{buildroot}%{py3_puresitedir}/%{name}/doc

# manual
rm -fr %{buildroot}%{py3_puresitedir}/%{name}/manpage
install -dm 0755 %{buildroot}%{_mandir}/man1/
install -pm 0644 manpage/man1/* %{buildroot}%{_mandir}/man1/

# .desktop
install -dm 0755 %{buildroot}%{_datadir}/applications
desktop-file-install %{name}.desktop \
	--remove-key=Encoding \
	--set-icon=%{name} \
	--remove-category=Application \
	--dir=%{buildroot}%{_datadir}/applications

rm -fr %{buildroot}%{py3_puresitedir}/%{name}/manpage
install -dm 0755 %{buildroot}%{_mandir}/man1/
install -pm 0644 manpage/man1/* %{buildroot}%{_mandir}/man1/

# shared-mime-info data
install -dm 0755 %{buildroot}%{_datadir}/mime/packages
install -pm 0644 application-x-songwrite.xml %{buildroot}%{_datadir}/mime/packages/%{name}.appdata.xml

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" data/%{name}.png \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -size 32x32 data/%{name}.png \
	%{buildroot}%{_datadir}/pixmaps/%{name}.xpm
			
# locales
mv %{buildroot}%{py3_puresitedir}/%{name}/locale %{buildroot}%{_datadir}
rm -f %{buildroot}%{_datadir}/locale/*/*/*.po
%find_lang %{name}
