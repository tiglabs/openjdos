#!/bin/bash
current_folder=`pwd`
relative_script_parent_path=`dirname $0`
if [ ${relative_script_parent_path:0:1} = "/" ]; then
    cwd=$relative_script_parent_path
else
    cwd=$current_folder/$relative_script_parent_path
fi

pypi_path=file://$cwd/../../../static/pypi/simple

usage() {
    echo "usage:$0 [sunshine-cli|sunshine-ctl|sunshine-dashboard|sunshine-ui]"
    exit 1
}

tool=$1
force=$2

if [ -z $tool ]; then
  usage
fi

install_pip() {
    pip --version | grep 7.0.3 >/dev/null || easy_install -i $pypi_path --upgrade pip
}

install_virtualenv() {
    virtualenv --version | grep 12.1.1 >/dev/null || pip install -i $pypi_path --ignore-installed virtualenv==12.1.1
}

cd $cwd

install_pip
install_virtualenv
cd /tmp

if [ $tool = 'sunshine-cli' ]; then
    CLI_VIRENV_PATH=/var/lib/sunshine/virtualenv/sunshinecli
    [ ! -z $force ] && rm -rf $CLI_VIRENV_PATH
    if [ ! -d "$CLI_VIRENV_PATH" ]; then
        virtualenv $CLI_VIRENV_PATH
        if [ $? -ne 0 ]; then
            rm -rf $CLI_VIRENV_PATH
            exit 1
        fi
    fi
    . $CLI_VIRENV_PATH/bin/activate
    cd $cwd
    pip install -i $pypi_path --trusted-host localhost --ignore-installed sunshinecli-*.tar.gz apibinding-*.tar.gz
    if [ $? -ne 0 ]; then
        rm -rf $CLI_VIRENV_PATH
        exit 1
    fi
    pip show sunshinelib
    if [ $? -ne 0 ]; then
        # fresh install sunshinelib
        echo "Installing sunshinelib..."
        pip install -i $pypi_path --trusted-host localhost --ignore-installed sunshinelib-*.tar.gz
        if [ $? -ne 0 ]; then
            rm -rf $CLI_VIRENV_PATH
            exit 1
        fi
    else
        # upgrade sunshinelib
        echo "Upgrading sunshinelib..."
        pip install -U -i $pypi_path --trusted-host localhost sunshinelib-*.tar.gz
        if [ $? -ne 0 ]; then
            rm -rf $CLI_VIRENV_PATH
            exit 1
        fi
    fi
    chmod +x /usr/bin/sunshine-cli

elif [ $tool = 'sunshine-ctl' ]; then
    cd $cwd
    pip install sunshinectl-*.tar.gz
    CTL_VIRENV_PATH=/var/lib/sunshine/virtualenv/sunshinectl
    rm -rf $CTL_VIRENV_PATH && virtualenv $CTL_VIRENV_PATH || exit 1
    . $CTL_VIRENV_PATH/bin/activate
    cd $cwd
    #pip install -i $pypi_path --trusted-host localhost --ignore-installed sunshinectl-*.tar.gz || exit 1
    pip install sunshinectl-*.tar.gz || exit 1
    chmod +x /usr/bin/sunshine-ctl
    python $CTL_VIRENV_PATH/lib/python2.7/site-packages/sunshinectl/generate_sunshinectl_bash_completion.py

elif [ $tool = 'onekey_deploy_ctl' ]; then
    cd $cwd
    #pip install -i $pypi_path --trusted-host localhost --ignore-installed sunshinectl-*.tar.gz || exit 1
    pip install onekey_deploy-*.tar.gz || exit 1
    chmod +x /usr/bin/onekey_deploy_ctl

elif [ $tool = 'sunshine-dashboard' ]; then
    UI_VIRENV_PATH=/var/lib/sunshine/virtualenv/sunshine-dashboard
    [ ! -z $force ] && rm -rf $UI_VIRENV_PATH
    if [ ! -d "$UI_VIRENV_PATH" ]; then
        virtualenv $UI_VIRENV_PATH
        if [ $? -ne 0 ]; then
            rm -rf $UI_VIRENV_PATH
            exit 1
        fi
    fi
    . $UI_VIRENV_PATH/bin/activate
    cd $cwd
    pip show versiontools
    if [ $? -ne 0 ]; then
        # fresh install versiontools
        echo "Installing versiontools..."
        pip install -i $pypi_path --trusted-host localhost versiontools
        if [ $? -ne 0 ]; then
            rm -rf $UI_VIRENV_PATH
            exit 1
        fi
    else
        # upgrade versiontools
        echo "Upgrading versiontools..."
        pip install -U -i $pypi_path --trusted-host localhost versiontools
        if [ $? -ne 0 ]; then
            rm -rf $UI_VIRENV_PATH
            exit 1
        fi
    fi
    pip show sunshine-dashboard
    if [ $? -ne 0 ]; then
        #fresh install sunshine_dashboard
        echo "Installing sunshine_dashboard..."
        pip install -i $pypi_path --trusted-host localhost --upgrade sunshine_dashboard-*.tar.gz
        if [ $? -ne 0 ]; then
            rm -rf $UI_VIRENV_PATH
            exit 1
        fi
    else
        #upgrae sunshine_dashboard
        echo "Upgrading sunshine_dashboard..."
        pip install -U -i $pypi_path --trusted-host localhost --upgrade sunshine_dashboard-*.tar.gz
        if [ $? -ne 0 ]; then
            rm -rf $UI_VIRENV_PATH
            exit 1
        fi
    fi

    chmod +x /etc/init.d/sunshine-dashboard

elif [ $tool = 'sunshine-ui' ]; then
    cd $cwd
    ui_home='/usr/local/sunshine/sunshine-ui/'
    mkdir -p $ui_home
    cp -f sunshine-ui.war $ui_home
    rm -rf $ui_home/tmp
    unzip sunshine-ui.war -d $ui_home/tmp
    cp -f sunshine-ui /etc/init.d/
    chmod a+x /etc/init.d/sunshine-ui
else
    usage
fi

