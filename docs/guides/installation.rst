Installation Guide
==================

Downloads
---------
* `Python`_ (version 2 and 3 are supported)
* `SuperCollider`_ 3.8 and above
* `sc3 plugins`_ (Some cool extra features for SuperCollider – recommended but not required)

Installing
----------
Follow the installation instructions for your downloads of Python and SuperCollider. When installing Python, click **yes** when asked if you want to add Python to your system path and **yes** if you want to install pip – this is used for automatically downloading/installing Python libraries such as FoxDot.

Install the latest version of FoxDot from the Python Package Index using pip from your command line (command prompt in Windows, terminal in MacOS and Linux) by executing: ::

    pip install FoxDot

Alternatively, you can build from the source on GitHub and keep up to date with the development version: ::

    git clone https://github.com/Qirky/FoxDot.git
    cd FoxDot
    python setup.py install

Open SuperCollder and install the FoxDot Quark (this allows FoxDot to communicate with SuperCollider – requires `Git`_ to be installed on your machine) by entering the following in the editor and pressing Ctrl+Return which “runs” a line of code: ::

    Quarks.install("FoxDot")

Recompile the SuperCollider class library by going to Language -> Recompile Class Library or pressing Ctrl+Shift+L.

If you don’t have `Git`_ installed, you can download an install the necessary SuperCollider Quarks directly from GitHub by running the 2 lines of code below in SuperCollider: ::

    Quarks.install("https://github.com/Qirky/FoxDotQuark.git")
    Quarks.install("https://github.com/supercollider-quarks/BatLib.git")

Startup
-------
Open SuperCollider and evaluate the following (this needs to be done before opening FoxDot): ::

    FoxDot.start

SuperCollider is now listening for messages from FoxDot. To start FoxDot from the command line  just type: ::

    python -m FoxDot

The FoxDot interface should open up and you’re ready to start jamming! Check out the :doc:`gettingstarted` guide for some useful tips on getting to know the basics of FoxDot. Happy coding!

Installing SC3 Plugins
----------------------
The SC3 Plugins are a collections of classes that extend the already massive SuperCollider library. Some of these are used for certain “effects” in FoxDot (such as bitcrush) and will give you an error in SuperCollider if you try to use them without installing the plugins. The SC3 Plugins can be downloaded from here.  Once downloaded place the folder into your SuperCollider “Extensions” folder and then restart SuperCollider. To find the location of the  “Extensions” folder, open SuperCollider and evaluate the following line of code: ::

    Platform.userExtensionDir

This will display the location of the “Extensions” folder in the  SuperCollider “post window”, usually on the right hand side of the screen. If this directory doesn’t exist, just create it and put the SC3 plugins in there and restart SuperCollider. When you next open FoxDot, go to the “Language” drop-down menu and tick “Use SC3 Plugins”. Restart FoxDot and you’re all set!

Installing with SuperCollider 3.7 or earlier
--------------------------------------------
If you are having trouble installing the FoxDot Quark in SuperCollider, it’s usually because the version of SuperCollider you are installing doesn’t have the functionality for installing Quarks or it doesn’t work properly. If this is the case, you can download the contents of the following SuperCollider script: `foxdot.scd`_. Once downloaded, open the file in SuperCollider and press Ctrl+Return to run it. This will make SuperCollider start listening for messages from FoxDot.

Installing on Linux
-------------------
Much of the installation (including Python & SuperCollider) has been automated into a simple shell script written by `Noisk8`_. You can download the `Linux Install`_ script from their GitHub which contains some information on what the script is doing and how to run it. (note: it is in Spanish but modern web browsers will translate that for you)

For more answers to other frequently asked questions, check out the `FAQ post`_ on the discussion forum.

Please report any issues or bugs on the project’s `GitHub`_ or if you have any questions, feel free to leave a message on the `discussion forum`_.


.. _Python: https://www.python.org/
.. _SuperCollider: http://supercollider.github.io/download
.. _sc3 plugins: http://sc3-plugins.sourceforge.net/
.. _Git: https://git-scm.com/downloads
.. _foxdot.scd: http://foxdot.org/wp-content/uploads/foxdot.scd
.. _Noisk8: https://github.com/Noisk8
.. _Linux Install: https://github.com/Noisk8/InstalandoFoxDot-En-linux
.. _FAQ post: http://foxdot.org/forum/?view=thread&id=1
.. _Github: https://github.com/Qirky/FoxDot/issues
.. _discussion forum: http://foxdot.org/forum/

