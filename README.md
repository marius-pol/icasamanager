# iCasa manager
A Python 3 manager for [iCasa platform](http://adeleresearchgroup.github.io/iCasa), which includes a smart home simulator for dynamic pervasive environments. iCasa manager offers the possibility to run the simulator, retrieve its state, and execute commands, directly from Python.

# Installation

## Requirements

### iCasa platform
iCasa platform requires Java Development Toolkit 6, or 8 (Java 7 and 11 may cause problems). On Ubuntu 20.04:

    sudo apt install openjdk-8-jdk-headless
    
iCasa platform may be downloaded from [here](http://adeleresearchgroup.github.io/iCasa/snapshot/download.html). Once started, the simulator GUI is accessible from a browser at [http://localhost:9000/simulator](http://localhost:9000/simulator).

iCasa manager downloads and runs the simulator automatically.

### iCasa manager
iCasa Manager requires a Python >=3.8 installation, with additional libraries that may be installed with:

    pip3 install -r requirements.txt
    
# Example

iCasa platform offers a teaching distribution with apps, which contains a [Light Follow Me application](<http://adeleresearchgroup.github.io/iCasa/snapshot/tutoIDE.html>). The application switches the lights on when a person enters a room in the smart home.

iCasa manager includes an example script that runs the Light Follow Me application, and moves persons randomly in the smart home to show how it works.

![Light Follow Me Tutorial screenshot](http://adeleresearchgroup.github.io/iCasa/snapshot/tutorial/followMe.png)

(image from [Light Follow Me tutorial](<http://adeleresearchgroup.github.io/iCasa/snapshot/tutoIDE.html>))
