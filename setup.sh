
yes 84 | SetupProject ROOT --ask
workon k3pi
export PYTHONPATH=$PWD:$PYTHONPATH
export PYTHONPATH=$PWD/CPP/lib:$PYTHONPATH
export LD_LIBRARY_PATH=$PWD/CPP/lib:$LD_LIBRARY_PATH
export SHAPECLASSES=$PWD/CPP/shape_classes/
