# LINFO2241 : Project setup

Welcome to this installation guide ! We'll guide you through the setup of LINFO2241's project :)

## SSH Setup (Mandatory for Mac users, recommended for the others)

If you are using a MacOS computer, you must setup your SSH access to UCLouvain network to work on this project. To do so, you must go **physically** to the Intel room in Réaumur building and connect to a computer. Once connected, simply follow the following steps :

### On your computer

Generate a key that will be used to communicate safely with UCLouvain Network (I'm sure you don't want your wonderful project to leak to other students ;)). You just have to open a terminal and type the following :

```bash
ssh-keygen -t ed25519 -C "John Doe's nice ssh key !"
eval "$(ssh-agent -s)"
#Linux
ssh-add ~/.ssh/id_ed25519
#MacOS
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```
Simply follow the steps on the screen and set a password if you want additional security (You'll have to enter it each time you want to connect to UCLouvain, so keep it in mind).

Now, you can simply show your key with :

```bash
cat ~/.ssh/id_ed25519.pub
# It should output something like "ssh-ed25519 AAAAC3N..."
```

Keep the result of this command in mind, you'll need it in the next steps.

### On the Intel computer

Once logged in a computer in the Intel Room, open a terminal and run :

```bash
vi ~/.ssh/authorized_keys 
```

This command will open a in-terminal text editor. Don't panic, this will be over soon.

Type `i` to enter in insertion mode, and type the output of the command from the previous step (The weird thing starting with `ssh-ed25519 AAA...`). The funny part is that the output of the command was on your MacOS laptop and now you have to retype it on the Intel computer. You can be brave and retype it yourself or send it through any channel (Usually, by mail) to then simply copy/paste it. Once done, press `Esc` and type `:wq` to save and leave the editor.

Alternatively you can use nano to edit the file, but learning a few vi commands is handy.

```bash
nano ~/.ssh/authorized_keys 
```

### Back on your computer

Now, you should be able to connect to the SSH gateway by typing this in a terminal :

```bash
ssh YourID@studssh.info.ucl.ac.be -i ~/.ssh/id_ed25519
```

Where you replace `YourID` by your UCLouvain identifier.

Then you can connect to the Intel room servers using

```bash
ssh didacXX
```
where XX is the id of the machine you want to connect to (didac01 for instance). You can find a list of the servers available [here](https://wiki.student.info.ucl.ac.be/Mat%C3%A9riel/SalleIntel). Beware that the wiki hasn't been updated yet and thus the hostnames are still intelXX on the website. Apart from that, every instruction on that page should hold.

If the connection doesn't work, please reach out to an assistant, we'll fix that.

You are highly encouraged to use an ssh config to simplify the connection to the remote computers.

~/.ssh/config :

```bash
Host studssh
  HostName studssh.info.ucl.ac.be
  User $YOURUSERNAME
  ForwardX11 yes
  ForwardX11Trusted yes
  ForwardAgent yes
  StrictHostKeyChecking no
  IdentityFile ~/.ssh/$YOURKEY
  ServerAliveInterval 60

Host didac01
  HostName didac01
  User $YOURUSERNAME
  ForwardX11 yes
  ForwardAgent yes
  StrictHostKeyChecking no
  ProxyCommand ssh studssh -W %h:%p
  ServerAliveInterval 60
```

From your computer, you can use

```bash
ssh didac01
```

***If you use VSCode as your text editor, the SSH extension is very convenient to code remotely. Use it***

## Prerequisites

For this project, you'll need **Linux**. If your machine is running on Windows or MacOS, please do not panic.

- **For Windows users** : Please setup WSL through the tutorial [here](https://learn.microsoft.com/en-us/windows/wsl/install). The default Ubuntu distribution will do just fine.
- **For Mac users** : You'll need to connect to UCL servers through SSH. Just follow the steps in the previous section.

You'll need basic compilation tools to work on this project. If you're working on UCLouvain's servers (MacOS), they are already installed. For the others, the procedure depends on which distribution you're running. It should go be one of the following :  

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install build-essential libpcre3-dev zlib1g-dev libssl-dev
```

### Fedora

```bash
sudo dnf install make automake gcc gcc-c++ kernel-devel pcre-devel zlib-devel libssl47
```

### ArchLinux/Manjaro

```bash
sudo pacman -S base-devel pcre2 zlib openssl
```

## Download repositories and build

If you haven't cloned the repository yet, open a terminal, then type :

```bash
git clone git@forge.uclouvain.be:LINFO2241/project-2023-student.git ARCHI_2023
cd ARCHI_2023
export PROJECT_PATH=$PWD
```

## Server setup

(**Warning** : Do not run these commands in a bash script)

```bash
# Downloading NGINX
wget https://nginx.org/download/nginx-1.23.0.tar.gz
tar -xzf nginx-1.23.0.tar.gz
rm nginx-1.23.0.tar.gz
mv nginx-1.23.0/ nginx/
# Download required extension
git clone https://github.com/Taymindis/nginx-link-function.git
# You should include the nginx-link-function header into the c include path
export C_INCLUDE_PATH=$PROJECT_PATH/nginx-link-function/src
# Compile nginx
cd nginx
# NGINX will be installed here
mkdir install
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install
make
make install
```

If you close your teminal, you might need to reuse these two commands or your code may not compile anymore :

```bash
# From the root directory of the project
export PROJECT_PATH=$PWD
export C_INCLUDE_PATH=$PROJECT_PATH/nginx-link-function/src
```

To get more debug information about nginx, you can use the `--with-debug` option to the configure script :
```bash
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install --with-debug
```

Additionnaly, you can specify compiler flags with `--with-cc-opt`

```bash
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install --with-cc-opt='-O0 -g'
```

Congratulations, you're just a few steps away from the end of this tutorial! There are just a few changes to apply.

First, you must create a log file for the application :  

```bash
touch $PROJECT_PATH/nginx/install/logs/error.log
```

Now, you're ready for the final step of this guide: building dependencies!

```bash
cd $PROJECT_PATH/project/server_implementation
make build
```

To run the server you can simply do :

```bash
make run
```

If you want more debugging information you can use the run_debug target :

```bash
make run_debug
```

This will also show additional logs if you added --with-debug to the configuration during NGINX installation. 

**Warning** : if you use make run instead of make run_debug. NGINX won't show errors even when they are present. When developping prefer the run_debug target.


## Testing your server

There is multiple ways to generate a HTTP request. You can for instance, use the following command :


```bash
wget --post-data '8,16,1,1So4BA8QEeuKeKAykWviFOyI' http://localhost:8888/ -q -O -
```

As the server returns encrypted file, it is normal to see weird characters outputed by this command.

Feel free to use whatever means you like for sending requests, it is not part of the evaluation (for now :D ).

[This](exptected_response.html) is the expected output of the server with the request above. You can use the linux diff tool to see if your server produces the expected output.

Other solutions can be :

- **[curl](https://gist.github.com/subfuzion/08c5d85437d5d4f00e58)** : another command-based client similar to wget
- **[Insomnia](https://insomnia.rest/)** : An application with a graphical user interface
- **[Postman](https://www.postman.com/)** : Like Insomnia, but it's proprietary software

## WRK

Starting from the second phase of the project, you are expected to automate your measurements. We recommend you [WRK](https://github.com/wg/wrk). It enables the generation of custom HTTP traffic through LUA scripts and collects statistics such as the latency and the throughput. For this project we will use [this](https://github.com/delimitrou/DeathStarBench/tree/master/wrk2) version of WRK. This is an improved version with an open loop design as opposed to the original closed loop design. The client doesn't wait for the server responds to send new requests. We provide you this version in this project in the wrk2-DeathStarBench folder. To build it, you can execute the following commands :

```bash
cd $PROJECT_PATH/wrk2-DeathStarBench
make
cd ..
./wrk2-DeathStarBench/wrk http://localhost:8888/  -d30s  --latency -R256 -s project/wrk_scripts/post.lua
```

- R256 specifies the rate: 256 request/s
- d30s specifies the length of the experiment
- s wrk_scripts/post.lua specifies the path to the lua script to use.

You can type 

```bash
./wrk2-DeathStarBench/wrk --help
```

to get more information about the different options.

**The --timeout option can be used to increase the timeout delay. This could be important when dealing with hard workloads to avoid excessive timeouts.**

**Don't forget to run your server before using WRK to send requests !!!**


## Deliverables
In addition to the deliverable already specified in the project statement, there is one more deliverable.
# Experiments & Plots 
You will have to fill the executable bash script [make_plots.sh](./project/make_plots.sh). This script should rerun your experiments, collect new data to a previously blank [data/results.csv](./project/data/results.csv) file and then generate the corresponding plots in the [plots](./project/plots/) directory. Plotting should be done to the best of your abilities. If your plotting abilities are not that good yet, you can always take another look at the material available on moodle 😉. The tools available to your for that purpose are bash, python 3 (numpy, pandas, matplotlib), gnuplot. 
