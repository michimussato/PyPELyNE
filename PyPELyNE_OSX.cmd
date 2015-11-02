#!/bin/sh

pypelyne_root="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
cd ${pypelyne_root};
source ${pypelyne_root}/conf/envVars_osx.txt;
python pypelyne_client.py;