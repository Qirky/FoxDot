from __future__ import absolute_import, division, print_function

from .Code import execute

class Bang:

    duration = 0.1

    def __init__(self, player, kwargs):

        self.widget = execute.namespace['FoxDot']

        self.func = kwargs.get("func", None)

        # Argument is by default, the  player
        
        self.args = kwargs.get("args", (player,))

        # User can supply a function to call on bang

        if self.func:

            try:

                self.func.__call__(*self.args)

            except Exception as e:

                print(e)

        else:

            # Get visible portion of the text window

            try:
            
                a = self.widget.text.index("@0,0")
                b = self.widget.text.index("@0,%d" % self.widget.text.winfo_height())

                a, b = (int(s.split(".")[0]) for s in (a, b))

            except:

                a, b = 9999, 0

            # Only update visuals if the line is visible

            if a <= player.line_number <= b:
                
                row = player.line_number
                col = player.whitespace
                env   = player.envelope
                event = player.event
                
                duration = event['sus']

                self.id = "{}_bang".format(player.id)

                start = "%d.%d" % (row, col)
                end   = "%d.end" % row

                def bang():
                    self.widget.addTask(target=self.widget.text.tag_add, args=(self.id, start, end))
                    self.widget.addTask(target=self.widget.text.tag_config, args=(self.id,), kwargs=kwargs)
                    return

                clock = player.metro

                t = clock.seconds_to_beats(clock.latency)

                clock.schedule(bang, player.metro.now() + t )

                clock.schedule(self.remove, player.metro.now() + self.duration + t)

            return

    def remove(self):
        self.widget.addTask(target=self.widget.text.tag_delete, args=(self.id,))
        return
      
