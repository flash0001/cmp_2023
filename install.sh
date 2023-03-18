#! /usr/bin/env bash 

su root -c 'apt-get install -y wget  build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev'


VERSION=3.11.2

PREFIX="${HOME}/local/Python/Python-${VERSION}"
mkdir -p "${PREFIX}"

wget https://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tar.xz

tar xfv Python-${VERSION}.tar.xz -C /tmp/
cd /tmp/Python-${VERSION} &&\
    ./configure --enable-optimization --prefix="${PREFIX}" &&\
    make -j 2 &&\
    make install


__PYTHONPATH=$PREFIX/bin
PIP=${__PYTHONPATH}/pip3

$PIP install --upgrade pip
$PIP install dash\
    dash-bootstrap-components\
    sqlalchemy\
    requests\
    pydantic\
    dash_echarts\
    plotly\
    pandas

. $HOME/.bashrc
if [[ -z "${PYTHONPATH}" ]]; then 
    echo "export PYTHONPATH=${__PYTHONPATH}" >> $HOME/.bashrc
    echo 'export PATH=${PYTHONPATH}:$PATH' >> $HOME/.bashrc
fi

exit 0
