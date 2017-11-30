from .Sequences import *

# Other useful functions that don't return a single pattern

def CalculateEuclideanDelay(durations):
    """ Calculates a pattern of durations and delays using nested
        tuples/PGroups and the PDur algorithm -- currently not implemented.
    """
    durs, dels = Pattern(), Pattern()
    for item in asStream(durations).data:
        # If it's a pattern / list, calc the delays
        if isinstance(item, (list, Pattern)):
            a, b = CalculateEuclideanDelay(item)
            durs.append(a)
            dels.append(b)
        # if it's a tuple/PGroup, calculate the PDur
        elif isinstance(item, (tuple, PGroup)):
            dur = PDur(*item)
            durs.append(sum(dur))
            dels.append(dur.accum().group())
        # If neither, just add the duration and a zero delay
        else:
            durs.append(item)
            dels.append(0)
    return durs, dels

def CalculateDelaysFromDur(durations):
    """ Used to calculate delays when the `dur` argument is given tuples.
        It replicates two events.
    """
    # If it's a PvarGenerator, this needs more work
    #if isinstance(durations, Pattern.PvarGenerator):
    #    durs = durations.transform(lambda a, b: CalculateDelaysFromDur(b.now())[0])
    #    dels = durations.transform(lambda a, b: CalculateDelaysFromDur(b.now())[1]) # could be more efficient?
    #    return durs, dels
    # If its a Pvar, create a new Pvar that uses this function as its transformation function
    if isinstance(durations, Pattern.Pvar):
        durs = durations.transform(lambda a, b: CalculateDelaysFromDur(a)[0])
        dels = durations.transform(lambda a, b: CalculateDelaysFromDur(a)[1])
        return durs, dels
    # Continue if not a pvargenerator
    durs, dels = Pattern(), Pattern()
    for item in asStream(durations).data:
        # If it's a pattern / list, calc the delays
        if isinstance(item, (list, Pattern)):
            a, b = CalculateDelaysFromDur(item)
            durs.append(a)
            dels.append(b)
        # if it's a tuple/PGroup, first dur as dur and then differences as delays
        elif isinstance(item, (tuple, PGroup)):
            if len(item) > 1:
                dur = min(item)
                durs.append(dur)
                dels.append(PGroup([offset - dur for offset in item]))
            else:
                durs.append(item[0])
                dels.append(0)
        # If neither, just add the duration and a zero delay
        else:
            durs.append(item)
            dels.append(0)
    return durs, dels.rotate(-1)
    
        
