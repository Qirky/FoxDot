# Tutorial 7: Clock Basics


# To stop all player objects, you can press Ctrl+.  (Hold Ctrl and hit the period)
# Which is a shortcut for the command:
Clock.clear()

# Change the tempo (this takes effect at the next bar) Default is 120.
Clock.bpm = 144

# To see what is scheduled to be played.
print(Clock)

# To see what the latency is
print(Clock.latency)

# Sometimes you want to know when the start of the next X beat cycle. To
# do this we use the 'mod' method. For example if we want to see when
# the start of the next 32 beat cycle is we can do
print(Clock.mod(32))