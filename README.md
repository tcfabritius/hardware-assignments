# MicroPython libraries for the first year hardware project

This is an example project that can be used to install MicroPython libraries that are needed for
the first year hardware project. You can also use this as a template for your own 
project.

# To setup your Pico

You need to have git installed. Make sure that you have python installed and that is in the path. You can verify this in terminal
by running **python --version** or **python3 --version**. If you see pyhton version then python is in the path.

You also need to have mpremote installed. To install mpremote:

- **pip install mpremote**
  
  or
  
- **python -m pip install mpremote**

When the prerequisites are met then you can install the project and the libraries to your Pico.

## Check out the repository and install libraries

Start a terminal, go to (use **cd** command) the directory where you want to copy the project to.

<kbd>git clone --recurse-submodules https://gitlab.metropolia.fi/lansk/pico-test.git</kbd>

Start a terminal, go to the pico-test directory and run:

- **.\install.cmd** if you use Windows PowerShell or cmd

- **./install.sh** if you use Linux, OSX or GitBash

