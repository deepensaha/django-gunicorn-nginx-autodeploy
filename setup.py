import os
import subprocess
import pathlib
import shutil
import getpass

# Check if virtual environment exists
has_venv = input('Do you already have a virtual environment(yes/no): ')

if has_venv == 'yes':
    # Ask for path full path of virtual env
    venv_path = input(
        'Enter full path of virtual environment directory: ')

    env_name = os.path.basename(venv_path)

    # Check if directory exists
    if(os.path.isdir(venv_path)):
        if(os.path.exists(venv_path)):
            print('Initiating Environment Setup Process...')
            subprocess.call(
                './__setup__/_env_init_.sh -c {cenv} -p {envp}'.format(cenv=0, envp=venv_path), shell=True)
    else:
        print('Please enter path of directory')
else:
    # Ask for environment name
    env_name = input('Enter name for virtual environment: ')

    print('Initiating Environment Setup Process...')
    subprocess.call(
        './__setup__/_env_init_.sh -c {cenv} -n {envn}'.format(cenv=1, envn=env_name), shell=True)

# Get Socket and Service name
socket_name = service_name = input('Enter Socket/Service Name: ')
ss_base_path = '/etc/systemd/system/'

# Initiating process for socket creation
sys_socket_path = ss_base_path + socket_name + '.socket'
temp_socket_path = './__setup__/' + socket_name + '.socket'

if not pathlib.Path(sys_socket_path).exists():
    print('Initiating socket file creation...')
    socket_template_path = './__setup__/socket.template'

    with open(socket_template_path, 'r') as socket_template:
        socket_template_data = socket_template.read().replace('__SOCKETNAME__', socket_name)

        with open(temp_socket_path, 'w+') as temp_socket:
            temp_socket.write(socket_template_data)
            temp_socket.close()

    subprocess.call(['sudo', 'mv', temp_socket_path, sys_socket_path])
    print('Socket File created...')
else:
    print('Socket file already exists')


# Initiating process for service creation
sys_service_path = ss_base_path + service_name + '.service'
temp_service_path = './__setup__/' + service_name + '.service'
service_template_path = './__setup__/service.template'
user = getpass.getuser()
current_dir = os.getcwd()
gunicorn_path = current_dir + os.path.sep + env_name + \
    os.path.sep + 'bin' + os.path.sep + 'gunicorn'
project_name = os.path.basename(current_dir)

print('Initiating service file creation...')

if not pathlib.Path(sys_service_path).exists():
    with open(service_template_path, 'r') as service_template:
        service_template_data = service_template.read() \
            .replace('__SERVICENAME__', service_name) \
            .replace('__SOCKETNAME__', socket_name) \
            .replace('__USER__', user) \
            .replace('__WORKINGDIR__', current_dir) \
            .replace('__GUNICORNPATH__', gunicorn_path) \
            .replace('__PROJECTNAME__', project_name)

        with open(temp_service_path, 'w+') as temp_service:
            temp_service.write(service_template_data)
            temp_service.close()

    subprocess.call(['sudo', 'mv', temp_service_path, sys_service_path])
    print('Service File created...')
else:
    print('Service file already exists')


# Nginx Config Creation
domain_name = input('Enter the domain name for nginx configuration : ')

sys_nginx_config_path = '/etc/nginx/sites-available/' + domain_name
sys_nginx_enable_path = '/etc/nginx/sites-enabled/' + domain_name
sys_symlink_path = '/etc/nginx/sites-enabled/'
nginx_template_path = './__setup__/nginx.template'
temp_nginx_config_path = './__setup__/' + domain_name

print('Initiating nginx file creation...')

if not pathlib.Path(sys_nginx_config_path).exists():
    if not pathlib.Path(sys_nginx_enable_path).exists():
        with open(nginx_template_path, 'r') as nginx_template:
            nginx_template_data = nginx_template.read() \
                .replace('__DOMAINNAME__', domain_name) \
                .replace('__ROOTDIR__', current_dir) \
                .replace('__SOCKETNAME__', socket_name)

            with open(temp_nginx_config_path, 'w+') as temp_nginx:
                temp_nginx.write(nginx_template_data)
                temp_nginx.close()

        subprocess.call(
            ['sudo', 'mv', temp_nginx_config_path, sys_nginx_config_path])
        subprocess.call(
            ['sudo', 'ln', '-s', sys_nginx_config_path, sys_symlink_path])

        print('Nginx Configured...')
    else:
        print('Symlink for domain name exists')
else:
    print('NGINX Config already exists')


# Restarting all processes
print('Restarting Processess')
subprocess.call(
    './__setup__/_finalize_.sh {socketname}'.format(socketname=socket_name), shell=True)

# For Local Development Setup
print('Please add an entry to /etc/hosts file if you are setting up on local machine and restart your nginx server')
