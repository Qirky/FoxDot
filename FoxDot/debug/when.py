def when(stmt, do=1, elsedo=2):
    print stmt, do, elsedo

when(lambda: x==1).do(lambda: x==1).elsedo(lambda: 10)
