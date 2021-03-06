#!/usr/bin/env python

from distutils.core import setup

setup(name='freemix',
      description='freemix is a free live video editing software, intended for and made by freedom loving live video artists',
      keywords='video live edition',
      version='0.2',
      url='https://edge.launchpad.net/freemix',
      license='GPL-2',
      author='Luis de Bethencourt',
      author_email='luisbg@ubuntu.com',
      long_description="""
      freemix is a free live video editing software, intended for and made by freedom loving live video artists.
      
      Based on pygtk and gstreamer, freemix gives the video artist a videosources table and a sequencer to mix videos live. While handling the sequencer bpm, video pitch and much more. 
      """,
      package_dir={'':'src'},
      packages=[''],
      scripts=['src/freemix'],
      py_modules=['controller','engine','gui','sequencer','videosource','videotable'],
      data_files=[
                  ('/usr/share/freemix',['README']),
                  (
                   '/usr/share/freemix/img',['img/freemix.png',
                                        'img/freemix_small.png',
                                        'img/empty.png',
                                        'img/VHSTapeOpen.png']
                  ),
                  (
                   '/usr/share/freemix/docs/',['docs/key_accelerators',
                                          'docs/use',
                                          'README']
                  ),
                  ('/usr/share/applications',['src/freemix.desktop']),
                  ('/usr/share/pixmaps',['img/freemix_small.png']),
                 ]
      )
