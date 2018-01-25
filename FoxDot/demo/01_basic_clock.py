# Tutorial 1: Clock Basics


# To stop all player objects, you can press Ctrl+.  (Hold Ctrl and hit the period)
# Which is a shortcut for the command:
Clock.clear()

# Change the tempo (this takes effect at the next bar) Default is 120.
Clock.bpm = 144

# To see what is scheduled to be played.
print(Clock)

# To see what the latency is
print(Clock.latency)
