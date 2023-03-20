# gettext is used by wine and some of its dependencies
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define intl_major 8
%define extpo_major 0
%define major 0
%define libintl %mklibname intl %{intl_major}
%define libasprintf %mklibname asprintf %{major}
%define libgettextpo %mklibname gettextpo %{extpo_major}
%define libgettextmisc %mklibname gettextmisc
%define devname %mklibname gettext -d
%define lib32intl %mklib32name intl %{intl_major}
%define lib32asprintf %mklib32name asprintf %{major}
%define lib32gettextpo %mklib32name gettextpo %{extpo_major}
%define lib32gettextmisc %mklib32name gettextmisc
%define dev32name %mklib32name gettext -d
%define _disable_rebuild_configure 1

# (tpg) optimize it a bit
%ifnarch %{riscv}
%global optflags %{optflags} -O3
%endif

%bcond_with check
%bcond_with java
%bcond_with csharp
%bcond_without emacs

Summary:	GNU libraries and utilities for producing multi-lingual messages
Name:		gettext
Version:	0.21.1
Release:	4
License:	GPLv3+ and LGPLv2+
Group:		System/Internationalization
Url:		http://www.gnu.org/software/gettext/
Source0:	http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.xz
Source2:	po-mode-init.el
Source100:	%{name}.rpmlintrc
# KDE example comes from 2003, it's really useless now
Patch0:		gettext-0.19.1-drop-kde-example.patch
# (tpg) Mageia patches
Patch1:		gettext-0.20.1-unescaped-left-brace.patch
Patch2:		0001-Backport-libcroco-upstream-merge-request-parser-limi.patch
Patch3:		gettext-0.21-clang.patch

# (tpg) Fedora patches
Patch4:		https://src.fedoraproject.org/rpms/gettext/raw/rawhide/f/gettext-0.21.1-disable-libtextstyle.patch
Patch5:		https://src.fedoraproject.org/rpms/gettext/raw/rawhide/f/gettext-0.21.1-covscan.patch

BuildRequires:	wget
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	pkgconfig(libacl)
BuildRequires:	gomp-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	texlive-dvips.bin
# Needed to make sure gettext realizes we have
# a working iconv()
BuildRequires:	locales-extra-charsets
%if %{with compat32}
BuildRequires:	devel(libunistring)
BuildRequires:	devel(libncursesw)
BuildRequires:	libc6
%endif
%if %with check
# test suite
BuildRequires:	locales-fa
BuildRequires:	locales-fr
BuildRequires:	locales-ja
BuildRequires:	locales-zh
%endif
%if %{with csharp}
# (Abel) we pick mono here, though pnet can be used as well.
BuildRequires:	mono
%endif
%if %with java
BuildRequires:	jdk-current
%endif
Provides:	bundled(libcroco) = 0.6.13
Requires:	%{name}-base = %{EVRD}
Requires:	%{libgettextmisc} = %{EVRD}
%if %{with emacs}
BuildRequires:	emacs
%endif

%description
The GNU gettext package provides a set of tools and documentation for producing
multi-lingual messages in programs. Tools include a set of conventions about
how programs should be written to support message catalogs, a directory and
file naming organization for the message catalogs, a runtime library which
supports the retrieval of translated messages, and stand-alone programs for
handling the translatable and the already translated strings. Gettext provides
an easy to use library and tools for creating, using, and modifying natural
language catalogs and is a powerful and simple method for internationalizing
programs.

If you would like to internationalize or incorporate multi-lingual messages
into programs that you're developing, you should install gettext.

Build Option:
--with csharp          Enables C# support in gettext
--without java         Disables Java support in gettext

%package -n %{libintl}
Summary:	Basic libintl library for internationalization
Group:		System/Libraries
License:	LGPL

%description -n %{libintl}
This package contains the libintl library, which is important for
system internationalization.

%package -n %{libasprintf}
Summary:	%{name} libasprintf needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Conflicts:	%{_lib}gettextmisc < 0.18.1.1-4

%description -n %{libasprintf}
This package contains libasprintf shared library.

%package -n %{libgettextpo}
Summary:	%{name} libgettextpo needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Conflicts:	%{_lib}gettextmisc < 0.18.1.1-4

%description -n %{libgettextpo}
This package contains libgettextpo shared library.

%package -n %{libgettextmisc}
Summary:	Other %{name} libraries needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Provides:	%{mklibname textstyle 0} = 0.21.1-1
Obsoletes:	%{mklibname textstyle 0} < 0.21.1-1

%description -n %{libgettextmisc}
This package contains all other libraries used by %{name} utilities,
and are not very widely used outside %{name}.

%if %{with compat32}
%package -n %{lib32intl}
Summary:	Basic libintl library for internationalization (32-bit)
Group:		System/Libraries
License:	LGPL
Provides:	libintl = %{EVRD}

%description -n %{lib32intl}
This package contains the libintl library, which is important for
system internationalization.

%package -n %{lib32asprintf}
Summary:	%{name} libasprintf needed by %{name} utilities (32-bit)
Group:		System/Libraries
License:	LGPL

%description -n %{lib32asprintf}
This package contains libasprintf shared library.

%package -n %{lib32gettextpo}
Summary:	%{name} libgettextpo needed by %{name} utilities (32-bit)
Group:		System/Libraries
License:	LGPL

%description -n %{lib32gettextpo}
This package contains libgettextpo shared library.

%package -n %{lib32gettextmisc}
Summary:	Other %{name} libraries needed by %{name} utilities (32-bit)
Group:		System/Libraries
License:	LGPL
Provides:	%{mklib32name textstyle 0} = 0.21.1-1
Obsoletes:	%{mklib32name textstyle 0} < 0.21.1-1

%description -n %{lib32gettextmisc}
This package contains all other libraries used by %{name} utilities,
and are not very widely used outside %{name}.

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
License:	LGPL
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32gettextpo} = %{EVRD}
Requires:	%{lib32asprintf} = %{EVRD}
Requires:	%{lib32gettextmisc} = %{EVRD}
Requires:	%{lib32intl} = %{EVRD}

%description -n %{dev32name}
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.
%endif

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{EVRD}
Requires:	%{libgettextpo} = %{EVRD}
Requires:	%{libasprintf} = %{EVRD}
Requires:	%{libgettextmisc} = %{EVRD}
Requires:	%{libintl} = %{EVRD}
# (tpg) autopoint requires cmp
Requires:	diffutils
%rename		%{name}-devel

%description -n %{devname}
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.

%package base
Summary:	Basic binary for showing translation of textual messages
Group:		System/Internationalization
Requires:	%{libintl} = %{EVRD}

%description base
This package contains the basic binary from %{name}. It is splitted from
%{name} because initscript need it to show translated boot messages.

%if %{with java}
%package java
Summary:	Java binding for GNU gettext
Group:		System/Internationalization
Requires:	%{name} = %{version}

%description java
This package contains class file that implements the main GNU libintl
functions in Java. This allows compiling GNU gettext message catalogs
into Java ResourceBundle classes.
%endif

%if %{with csharp}
%package csharp
Summary:	C# binding for GNU gettext
Group:		System/Internationalization
Requires:	mono

%description csharp
This package contains class file that implements the main GNU libintl
functions in C#. This allows compiling GNU gettext message catalogs
into C# dll or resource files.
%endif

%package emacs
Summary:	Emacs editor integration for gettext
Enhances:	emacs
Requires:	emacs

%description emacs
Emacs editor integration for gettext

%prep
%autosetup -p1

# Defeat libtextstyle attempt to bundle libxml2.  The comments
# indicate this is done because the libtextstyle authors do not want
# applications using their code to suffer startup delays due to the
# relocations in the two libraries.  This is not a sufficient reason for us.
rm -rf libtextstyle/lib/{glib,libxml}
for l in LIBGLIB LIBXML; do
    sed -i -e "s,\(gl_$l(\[\).*\(\])\),\1no\2,g" $(grep -rl -e "gl_$l(\[.*\])")
done

autoreconf -fi

export CONFIGURE_TOP=$(pwd)

%if %with java
. %{_sysconfdir}/profile.d/90java.sh
%endif

%if %{with compat32}
mkdir build32
cd build32
%configure32 --with-included-libcroco --with-included-glib --with-included-libxml
cd ..
%endif

mkdir build
cd build
# ARM -fuse-ld=bfd addition is a workaround for a crash in
# ARM32 ld.gold when linking clang++ code.
# FIXME remove when binutils is fixed.
%ifarch %{arm}
CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%endif
%configure \
	--disable-static \
	--disable-rpath \
	--enable-shared \
	--with-included-gettext \
	--without-included-regex \
	--without-included-glib \
	--with-included-libcroco \
	--enable-openmp \
%if %{with csharp}
	--enable-csharp=mono \
%else
	--disable-csharp \
%endif
%if ! %{with java}
	--disable-java \
%endif

# Eliminate hardcoded rpaths; workaround libtool reordering -Wl,--as-needed
# after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC=.g..|& -Wl,--as-needed|' \
    -i $(find . -name libtool)

%build
%if %with java
. %{_sysconfdir}/profile.d/90java.sh
%endif

%if %{with compat32}
%make_build -C build32
%endif

%make_build -C build

%if %{with check}
%check
LC_ALL=C make check
%endif

%install
%if %{with compat32}
%make_install -C build32
# We get 64-bit versions of the same tools in
# %{_libdir}/gettext -- no need for duplication
rm -rf %{buildroot}%{_prefix}/lib/gettext
rm -rf %{buildroot}%{_prefix}/lib/GNU.Gettext.dll
%endif
%make_install -C build

# remove unwanted files
rm -f %{buildroot}%{_includedir}/libintl.h \
      %{buildroot}%{_datadir}/locale/locale.alias
rm -f gettext-runtime/intl-java/javadoc2/package-list

%if %{with emacs}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
%endif

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf %{buildroot}/%{_datadir}/locale/$i; done

# move installed doc back to %%doc
rm -rf htmldoc examples
mkdir htmldoc
for i in gettext-runtime/man/*.html; do
  rm -f %{buildroot}%{_datadir}/doc/gettext/`basename $i`
done
rm -rf %{buildroot}%{_datadir}/doc/gettext/javadoc*
mv %{buildroot}%{_datadir}/doc/gettext/* %{buildroot}/%{_datadir}/doc/libasprintf/* htmldoc ||:
mv htmldoc/examples examples

# remove java stuff, otherwise rpm complains
%if !%{with java}
rm -f %{buildroot}%{_libdir}/%{name}/gnu.gettext.* \
      %{buildroot}%{_datadir}/%{name}/*.jar
%endif

# cleanup rpaths
for i in %{buildroot}%{_bindir}/* $(find %{buildroot}%{_libdir} -type f); do
    if file $i | grep "ELF 64-bit" >/dev/null; then
	chrpath -l $i && chrpath --delete $i
    fi
done

%find_lang %{name} --all-name

# libintl is completely superflous (glibc, musl and uClibc-ng all have
# its functionality built in), so let's avoid bloat where possible...
# (We need libintl.so.8 anyway, for 3rd party applications built on
# other distros)
rm -f %{buildroot}%{_libdir}/libintl.so
cat >%{buildroot}%{_libdir}/libintl.so <<EOF
/* GNU ld script */
EOF

%if %{with compat32}
rm -f %{buildroot}%{_prefix}/lib/libintl.so
cat >%{buildroot}%{_prefix}/lib/libintl.so <<EOF
/* GNU ld script */
EOF
%endif

# For some reason, the post scripts fail to do this
#strip --strip-unneeded %buildroot/%_lib/libintl.so.8.*
%define strip_boot %{_target_platform}-strip
%{strip_boot} --strip-unneeded %{buildroot}%{_libdir}/libintl.so.*

%files
%doc AUTHORS README COPYING gettext-runtime/ABOUT-NLS gettext-runtime/BUGS NEWS THANKS
%{_bindir}/envsubst
%{_bindir}/gettext.sh
%{_bindir}/msg*
%{_bindir}/recode-sr-latin
%{_bindir}/xgettext
%dir %{_datadir}/gettext
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/%{name}/projects
%{_datadir}/%{name}/javaversion.class
%{_datadir}/%{name}/styles
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/its
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/cldr-plurals
%{_libdir}/%{name}/hostname
%{_libdir}/%{name}/project-id
%{_libdir}/%{name}/urlget
%{_libdir}/%{name}/user-email
%if %{with java}
%exclude %{_libdir}/%{name}/gnu.gettext.*
%endif
%doc %{_infodir}/gettext.*
%doc %{_mandir}/man1/envsubst.*
%doc %{_mandir}/man1/msg*
%doc %{_mandir}/man1/xgettext.*
%doc %{_mandir}/man1/recode-sr-latin.*

%files base -f %{name}.lang
%doc gettext-runtime/man/*.1.html
%doc gettext-runtime/intl/COPYING*
%{_bindir}/gettext
%{_bindir}/ngettext
%doc %{_mandir}/man1/gettext*
%doc %{_mandir}/man1/ngettext*

%if %{with emacs}
%files emacs
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_datadir}/emacs/site-lisp/*.el*
%endif

%files -n %{libintl}
%{_libdir}/libintl.so.%{intl_major}*

%files -n %{libasprintf}
%{_libdir}/libasprintf.so.%{major}*

%files -n %{libgettextpo}
%{_libdir}/libgettextpo.so.%{extpo_major}*

%files -n %{libgettextmisc}
%{_libdir}/libgettextlib-*.so
%{_libdir}/libgettextsrc-*.so

%files -n %{devname}
%doc gettext-runtime/man/*.3.html examples htmldoc
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/archive*
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/po
%{_datadir}/aclocal/*
%{_includedir}/*
%doc %{_infodir}/autosprintf*
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libasprintf.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%doc %{_mandir}/man1/autopoint.*
%doc %{_mandir}/man3/*

%if %{with java}
%files java
%doc gettext-runtime/intl-java/javadoc*
%{_libdir}/%{name}/gnu.gettext.*
%{_datadir}/%{name}/*.jar
%endif

%if %{with csharp}
%files csharp
%doc gettext-runtime/intl-csharp/csharpdoc/*
%{_libdir}/*.dll
%{_libdir}/gettext/*.exe
%endif

%if %{with compat32}
%files -n %{lib32intl}
%{_prefix}/lib/preloadable_libintl.so

%files -n %{lib32asprintf}
%{_prefix}/lib/libasprintf.so.%{major}*

%files -n %{lib32gettextpo}
%{_prefix}/lib/libgettextpo.so.%{extpo_major}*

%files -n %{lib32gettextmisc}
%{_prefix}/lib/libgettextlib-*.so
%{_prefix}/lib/libgettextsrc-*.so

%files -n %{dev32name}
%{_prefix}/lib/libasprintf.so
%{_prefix}/lib/libgettextlib.so
%{_prefix}/lib/libgettextpo.so
%{_prefix}/lib/libgettextsrc.so
%{_prefix}/lib/libintl.so
%endif
