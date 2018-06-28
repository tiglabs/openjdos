#!/bin/sh
# Author: YYK
sunshine_war="~/sunshine.war"
sunshine_service="/etc/init.d/sunshine-server"
tomcat_folder_path=""
sunshine_property_folder=~/.sunshine/
[ ! -d $sunshine_property_folder ] && mkdir $sunshine_property_folder || exit 1
old_sunshine_property=$sunshine_property_folder/sunshine.properties-old
tomcat_path_save=$sunshine_property_folder/tomcat_path

[ -f $tomcat_path_save ] && tomcat_folder_path=`cat $tomcat_path_save`

#default is upgrade
fresh_install=0
user_selection=""
interactive_install=0

set -u # undefined variables are errors

error_tmp_file=`mktemp`
trap "rm $error_tmp_file 2>/dev/null" EXIT

help (){
    echo "Usage: $0 [options] [TOMCAT_PATH]

Description:
    Sunshine Installer will install sunshine.war to the given Tomcat folder.
It is assumed all tools and services are installed, including Tomcat,
MySQL server, RabbitMQ server, Ansible etc. The default behavior (without -f)
will upgrade current Sunshine and keep previous sunshine.properties.
    Without command line options, it will pop up a menu for user interaction.

Options:
  -u DB_USER    Database user name, default is 'root'
  -p DB_PASSWD  Database user password, default is ''
  -s DB_HOST    Database host server name, default is 'localhost'
  -P DB_PORT    Database host server mysql port, default is '3306'
  -f            Fresh installation. Will deploy fresh sunshine database. Default
                behavior is just upgrade sunshine and not deploy new database.
  -w WAR_FILE   The path to sunshine.war file, default is '$sunshine_war'
  -h            Show this help.
"
    exit 1
}

err_quit(){
    echo -e "$(tput setaf 1)$*\n$(tput sgr0)"
    echo -e "$(tput setaf 1)Sunshine Installation Failed\n$(tput sgr0)"
    exit 1
}

show_config(){
    if [ "0" = "$1" ]; then
        tput setaf 2
        echo ' ... [ok]'
    else
        tput setaf 1
        echo ' ... [need config]'
    fi
    tput sgr0
}

show_menu(){
    is_ok=1
    tput clear
    tput sgr0
    tput cup 3 20
    tput setaf 3
    tput rev
    echo "Sunshine Server Installation Menu"
    tput sgr0

    tput cup 8 15
    echo "1. Apache Tomcat Configuration"
    tput cup 8 50
    check_tomcat 'quiet'
    tomcat_flag=$?
    show_config $tomcat_flag

    tput cup 9 15
    echo "2. MySQL Database Configuration"
    tput cup 9 50
    check_mysql 'quiet'
    mysql_flag=$?
    show_config $mysql_flag

    [ $mysql_flag -eq 0 ] && [ $tomcat_flag -eq 0 ] && is_ok=0

    [ $is_ok -ne 0 ] && tput setaf 7
    tput cup 10 15
    echo "3. Upgrade Sunshine Server"

    tput cup 11 15
    echo "4. Fresh Install Sunshine Server"

    tput sgr0
    tput cup 12 15
    echo "5. Quit"

    tput bold
    tput cup 14 13
    read -p "Enter your state[1-5]: " user_selection

    tput clear
    tput sgr0
    tput rc

    case $user_selection in
        1)  config_tomcat
            show_menu;;
        2)  config_db
            show_menu ;;
        3)  if [ $is_ok -eq 0 ];then
                fresh_install=0
            else
                show_menu
            fi
            ;;
        4)  if [ $is_ok -eq 0 ];then
                fresh_install=1
            else
                show_menu
            fi
            ;;
        5)  exit ;;
        *)  show_menu ;;
    esac
}

#set db user,password etc.
config_db(){
    tput clear
    tput sgr0
    tput cup 3 10
    tput setaf 3
    tput rev
    echo "Config MySQL Connection"
    tput sgr0
    tput cup 5 15
    echo "Current Database Configurations:"
    tput setaf 3
    tput cup 6 20
    echo "1. Database Host: $db_host"
    tput cup 7 20
    echo "2. Database Port: $db_port"
    tput cup 8 20
    echo "3. Database Username: $db_user_name"
    tput cup 9 20
    echo "4. Database Password: $db_user_passwd"

    tput sgr0
    tput bold
    tput cup 12 15
    read -p "Enter the item you want to modify or any key for Quit [1-4]: " db_line

    tput cup 15 15
    case $db_line in
        1)  read -p "Input the MySQL server name:" db_host
            config_db ;;
        2)  read -p "Input the MySQL server port:" db_port
            config_db ;;
        3)  read -p "Input the MySQL server user name:" db_user_name
            config_db ;;
        4)  read -p "Input the MySQL server user password:" db_user_passwd
            config_db ;;
        *)  ;;
    esac

    tput clear
    tput sgr0
    tput rc
}

#set tomcat_path
config_tomcat(){
    tput clear
    tput sgr0
    tput cup 3 10
    tput setaf 3
    tput rev
    echo "Set Tomcat Directory"
    tput sgr0
    tput cup 8 15
    echo "Current Tomcat path is: $tomcat_folder_path"
    tput setaf 3
    tput cup 20 10
    echo "Tomcat path should be a folder, including webapps, bin and other Tomcat's contents. Use [TAB] for auto completion."
    tput sgr0
    tput bold
    tput cup 12 15
    read -e -p "Set new Tomcat's path: " tmp_tomcat_folder_path
    if [ $tmp_tomcat_folder_path != '\r' ] && [ $tmp_tomcat_folder_path != '\n' ]; then
        tomcat_folder_path=$tmp_tomcat_folder_path
    fi

    webapp_folder=$tomcat_folder_path/webapps
    sunshine_folder=$webapp_folder/sunshine
    sunshine_property="$sunshine_folder/WEB-INF/classes/sunshine.properties"
    set_db_config
    tput clear
    tput sgr0
    tput rc
}

# check mysql connection.
check_mysql(){
    if [ ! -z $1 ];then
        error_log=/dev/null
    else
        error_log=$error_tmp_file
    fi
    mysql --user=$db_user_name --password=$db_user_passwd --host=$db_host --port=$db_port >/dev/null 2>$error_log << EOF
DROP DATABASE IF EXISTS testSunshineInstallationDb;
CREATE DATABASE testSunshineInstallationDb;
DROP DATABASE testSunshineInstallationDb;
EOF
    return $?
}

check_tomcat(){
    webapp_folder=$tomcat_folder_path/webapps
    if [ ! -d $webapp_folder ]; then
        [ ! -z $1 ] && return 1
        err_quit "Tomcat's web application folder: $webapp_folder doesn't not exist"
    fi

    if [ ! -f $tomcat_folder_path/bin/startup.sh ]; then
        [ ! -z $1 ] && return 1
        err_quit "Is $tomcat_folder_path tomcat folder? Can't find $tomcat_folder_path/bin/startup.sh "
    fi
    return 0
}

set_db_config(){
    #base on old sunshine.properties to get current db configurations.
    if [ -f $sunshine_property ];then
        /bin/cp -f $sunshine_property $old_sunshine_property
        db_info=`grep 'DbFacadeDataSource.jdbcUrl' $sunshine_property|awk -F'//' '{print $2}'|awk -F'/' '{print $1}'`
        db_df_host=`echo $db_info|awk -F: '{print $1}'`
        db_df_port=`echo $db_info|awk -F: '{print $2}'`
        db_df_user=`grep 'DbFacadeDataSource.user' $sunshine_property|awk -F=  '{print $2}'|tr -d '\r'|tr -d '\n'`
        db_df_passwd=`grep 'DbFacadeDataSource.password' $sunshine_property|awk -F=  '{print $2}'|tr -d '\r'|tr -d '\n'`
    else
        if [ -f $old_sunshine_property ]; then
            db_info=`grep 'DbFacadeDataSource.jdbcUrl' $old_sunshine_property|awk -F'//' '{print $2}'|awk -F'/' '{print $1}'`
            db_df_host=`echo $db_info|awk -F: '{print $1}'`
            db_df_port=`echo $db_info|awk -F: '{print $2}'`
            db_df_user=`grep 'DbFacadeDataSource.user' $old_sunshine_property|awk -F=  '{print $2}'|tr -d '\r'|tr -d '\n'`
            db_df_passwd=`grep 'DbFacadeDataSource.password' $old_sunshine_property|awk -F=  '{print $2}'|tr -d '\r'|tr -d '\n'`
        else
            db_df_host=localhost
            db_df_port=3306
            db_df_user=root
            df_df_passwd=""
        fi
    fi

    db_user_name=${db_user_name-"$db_df_user"}
    db_user_passwd=${db_user_passwd-"$db_df_passwd"}
    db_host=${db_host-"$db_df_host"}
    db_port=${db_port-"$db_df_port"}
}

cancel(){
    tput clear
    tput sgr0
    tput rc
    echo "Cancel installation by User"
    exit 1
}

trap cancel INT

[ $# -eq 0 ] && interactive_install=1

OPTIND=1
while getopts "u:p:s:P:fw:h" Option
do
    case $Option in
        u ) db_user_name=$OPTARG;;
        p ) db_user_passwd=$OPTARG;;
        s ) db_host=$OPTARG;;
        P ) db_port=$OPTARG;;
        f ) fresh_install=1;;
        w ) sunshine_war=$OPTARG;;
        h ) help;;
        * ) help;;
    esac
done
shift `expr $OPTIND - 1`

if [ $interactive_install -eq 0 ]; then
    # only one left-over - the path to tomcat
    [ $# -eq 1 ] || help

    tomcat_folder_path=$1
    webapp_folder=$tomcat_folder_path/webapps
    sunshine_folder=$webapp_folder/sunshine
    sunshine_property="$sunshine_folder/WEB-INF/classes/sunshine.properties"
    set_db_config
else
    config_tomcat
    config_db
    show_menu
fi

echo $tomcat_folder_path > $tomcat_path_save
# Above: do configuration
#-------------
# Below: begin installation or upgrading
if [ $fresh_install -eq 0 ];then
    echo "Upgrade Sunshine Server ..."
    if [ ! -f $sunshine_service ];then
        err_quit "Do not find sunshine service script in $sunshine_service. If not install Sunshine yet, please add option -f"
    fi
    echo "Stop Sunshine Server ..."
    $sunshine_service stop
    if [ $? -ne 0 ]; then
        pid=`ps -aef|grep java|grep 'org.apache.catalina.startup.Bootstrap'|awk '{print $2}'`
        ps -p $pid > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            err_quit "Can not stop Sunshine server by '$sunshine_service stop'. Kill Tomcat service manually and rerun the install.sh again."
        fi
    fi
    echo "Sunshine Server is not running"
else
    echo "Install Sunshine Server ..."
    if [ -f $sunshine_service ];then
        $sunshine_service stop
    fi
fi

check_cmd(){
    #$1 is command name
    #$2 is command's package name
    which $1 >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        err_quit "Can not find command: [$1], you need to install [$2] firstly."
    fi
}

check_cmd unzip unzip
check_cmd mysql mysql
check_cmd rabbitmqctl rabbitmq-server
check_cmd ansible ansible

check_mysql
if [ $? -ne 0 ];then
    err_quit "Can not operate mysql database with
    [user:] $db_user_name
    [password:] $db_user_passwd
    [mysql server:] $db_host:$db_port

    The reason is:
    `cat $error_tmp_file`
    "
fi

# check rabbitmq-server connection.
rabbitmqctl status >/dev/null 2>$error_tmp_file
if [ $? -ne 0 ]; then
    err_quit "Can not get rabbitmq server's status.
    The reason is :
    `cat $error_tmp_file`
    "
fi

check_tomcat
/bin/rm -rf $sunshine_folder
/bin/rm -f $webapp_folder/sunshine.war

if [ ! -f $sunshine_war ]; then
    err_quit "Did not find sunshine.war: $sunshine_war"
fi

cp $sunshine_war $webapp_folder
cd $webapp_folder

unzip -q -d sunshine sunshine.war
if [ $fresh_install -eq 1 ]; then
    sed -i "s/DbFacadeDataSource.user.*/DbFacadeDataSource.user=$db_user_name/" $sunshine_property
    sed -i "s/DbFacadeDataSource.password.*/DbFacadeDataSource.password=$db_user_passwd/" $sunshine_property
    sed -i "s/DbFacadeDataSource.jdbcUrl.*/DbFacadeDataSource.jdbcUrl=jdbc:mysql:\/\/$db_host:$db_port\/sunshine/" $sunshine_property
    sed -i "s/RestApiDataSource.jdbcUrl.*/RestApiDataSource.jdbcUrl=jdbc:mysql:\/\/$db_host:$db_port\/sunshine_rest/" $sunshine_property

    db_script_folder=sunshine/WEB-INF/classes/db
    database=$db_script_folder/database.sql
    schema=$db_script_folder/schema.sql
    trigger=$db_script_folder/trigger.sql
    schema_rest=$db_script_folder/schema-rest.sql
    schema_quartz=$db_script_folder/sunshine_quartz.sql
    view=$db_script_folder/view.sql

    create_sunshine_db(){
        mysql --user=$db_user_name --password=$db_user_passwd --host=$db_host --port=$db_port < $1 >/dev/null 2>$error_tmp_file
        if [ $? -ne 0 ];then
            err_quit "Create Sunshine Initial Database Failed.
        The reason is:
        `cat $error_tmp_file`"
        fi
    }

    update_sunshine_db(){
        mysql --user=$db_user_name --password=$db_user_passwd --host=$db_host --port=$db_port -t $1 < $2 >/dev/null 2>$error_tmp_file
        if [ $? -ne 0 ];then
            err_quit "Create Sunshine Initial Database Failed.
        The reason is:
        `cat $error_tmp_file`"
        fi
    }
    #can not directly call deploydb.sh, since the empty password string will
    # make the parameters sequence wrong.
    create_sunshine_db  $database
    create_sunshine_db  $schema
    create_sunshine_db  $view
    #create_sunshine_db $trigger
    create_sunshine_db  $schema_rest
    update_sunshine_db "sunshine_quartz" $schema_quartz
else
    /bin/cp -f $old_sunshine_property $sunshine_property
fi

sunshine_service_script=$webapp_folder/sunshine/WEB-INF/classes/install/sunshine-server

if [ ! -f $sunshine_service_script ]; then
    err_quit "Did not find sunshine server script: $sunshine_service_script"
fi

#since tomcat_folder_path is a path, should use '#' instead of '/' in sed
sed -i "s#^TOMCAT_PATH=.*#TOMCAT_PATH=$tomcat_folder_path#" $sunshine_service_script
/bin/cp -f $sunshine_service_script /etc/init.d/
chmod a+x /etc/init.d/sunshine-server

if [ $fresh_install -eq 1 ]; then
    echo -e "$(tput setaf 2)Sunshine has been installed to $webapp_folder\n$(tput sgr0)"
else
    echo -e "$(tput setaf 2)Sunshine has been upgraded in $webapp_folder\n$(tput sgr0)"
fi
echo -e "$(tput setaf 2)sunshine-server has been installed to /etc/init.d . Run \`/etc/init.d/sunshine-server start\` to start sunshine service.\n$(tput sgr0)"
[ -f $old_sunshine_property ] && echo -e "$(tput setaf 2)Original sunshine.properties was saved in $old_sunshine_property\n$(tput sgr0)"

# vim: set et ts=4 sw=4 ai:
