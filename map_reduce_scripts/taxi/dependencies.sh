#!/bin/bash
set -e

# install shapely
sudo yum install geos-devel.x86_64 -y
sudo pip install shapely

# install geoindex
wget -T 30 -t 3 https://pypi.python.org/packages/99/b5/020117b2986a6229e52fdfaa80f0e164ec733b71c59c680ea672c8d5a331/geoindex-0.0.1.tar.gz
tar -xzf geoindex-0.0.1.tar.gz
sudo easy_install -l geoindex-0.0.1