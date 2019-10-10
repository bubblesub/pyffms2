project(
  'ffms2',
  'c',
  'cpp',
  default_options : [
    'buildtype=release',
    'warning_level=2',
    'b_ndebug=if-release',
    'c_std=c99',
    'cpp_std=c++11'
  ],
  meson_version : '>=0.51.1',
  version : '2.30.0'
)

add_project_arguments(
  '-DFFMS_EXPORTS',
  '-D_FILE_OFFSET_BITS=64',
  '-D__STDC_CONSTANT_MACROS',
  language : ['c', 'cpp']
)

ffms2_sources = [
  'src/core/audiosource.cpp',
  'src/core/audiosource.h',
  'src/core/ffms.cpp',
  'src/core/filehandle.cpp',
  'src/core/filehandle.h',
  'src/core/indexing.cpp',
  'src/core/indexing.h',
  'src/core/track.cpp',
  'src/core/track.h',
  'src/core/utils.cpp',
  'src/core/utils.h',
  'src/core/videosource.cpp',
  'src/core/videosource.h',
  'src/core/videoutils.cpp',
  'src/core/videoutils.h',
  'src/core/zipfile.cpp',
  'src/core/zipfile.h',
  'src/vapoursynth/vapoursource.cpp',
  'src/vapoursynth/vapoursource.h',
  'src/vapoursynth/vapoursynth.cpp',
  'src/vapoursynth/VapourSynth.h',
  'src/vapoursynth/VSHelper.h',
]

ffmsindex_sources = [
  'src/index/ffmsindex.cpp',
  'src/index/vsutf16.h'
]

includes = include_directories('include')

deps = [
  dependency('libavformat', version : '>=53.20.0'),
  dependency('libavcodec', version : '>=53.24.0'),
  dependency('libswresample', version : '>=1.0.0'),
  dependency('libswscale', version : '>=0.7.0'),
  dependency('libavutil', version : '>=51.21.0'),
]

if host_machine.cpu_family().endswith('x86')
  add_project_arguments(
    '-m32',
    '-mfpmath=sse',
    '-msse',
    '-march=pentium3',
    '-mtune=pentium3',
    language : ['c', 'cpp']
  )
endif

compiler = meson.get_compiler('cpp')
host = host_machine.system() == 'windows'

ffms2_ldflags = []
if host and get_option('default_library') == 'static'
  mingw_path = '/usr/x86_64-w64-mingw32/lib'
  deps += [
    compiler.find_library('libz', dirs: mingw_path, static: true),
    compiler.find_library('bcrypt', dirs: mingw_path, static: true),
  ]
  ffms2_ldflags += '-static'
else
  deps += [dependency('zlib')]
endif

ffms2_lib = shared_library(
  'ffms2',
  ffms2_sources,
  name_prefix: '',
  link_args: ffms2_ldflags,
  dependencies : deps,
  include_directories : includes,
  install : true,
  gnu_symbol_visibility : 'hidden'
)

ffmsindex_ldflags = []
if (compiler.get_id() == 'gcc' or compiler.get_id() == 'clang') and host
  ffmsindex_ldflags += '-municode'
endif

if host and get_option('default_library') == 'static'
  ffmsindex_ldflags += '-static'
endif

executable(
  'ffmsindex',
  ffmsindex_sources,
  link_args : ffmsindex_ldflags,
  link_with : ffms2_lib,
  include_directories : includes,
  install : true,
  gnu_symbol_visibility : 'hidden'
)

import('pkgconfig').generate(
  ffms2_lib,
  filebase : 'ffms2',
  name : 'ffms2',
  description : 'The Fabulous FM Library 2'
)

install_data(
  ['doc/ffms2-api.md', 'doc/ffms2-changelog.md'],
  install_dir : join_paths(get_option('datadir'), 'doc', 'ffms2')
)

install_headers(['include/ffms.h', 'include/ffmscompat.h'])
