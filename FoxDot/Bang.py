from Code import execute

class Bang:

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

                try:

                    self.widget.text.tag_add(self.id, start, end)
                    self.widget.text.tag_config(self.id, **kwargs)

                    self.duration = 0.1

                    player.metro.schedule(self.remove, player.metro.now() + self.duration)

                except:

                    pass


    def remove(self):
        self.widget.text.tag_delete(self.id)
        return
      
