#!/usr/bin/python

"""
    Copyright Ryan Kirkbride 2015

    This is a very simple way to import FoxDot and combine it with the Tk
    interface module located in the App folder.

    Overwriting the App.submit() method is how you connect the app to the
    FoxDot environment. Any other methods that involve communicating with
    FoxDot must be defined in your own application e.g. App.killall()

"""

if __name__ == "__main__":

    from FoxDot import Code
    from App import App

    # Load FoxDot Modules into the environment

    class interface(App):

        Code.execute( "from FoxDot import *" )
        Code.execute( "Clock.start()" )

        def submit(self, code_str):
            
            """ Overwrites the empty method to send a piece of
                FoxDot code to the environment. """

            try:
                    
                Code.execute( code_str )

            except:

                return

        def killall(self, event):

            Code.execute("Clock.clear()")
        
            return "break"

        def terminate(self):

            """ Overrides the close window event to make sure
                the TempoClock thread is properly stopped """

            Code.execute("Clock.stop()")

            return
        
    a = interface()

    a.run()
