def Location_Worker(location):
    coastal_govs = ['jendouba', 'bizerte', 'ariana', 'nabeul', 'monastir', 'mahdia', 'sfax', 'gabes', 'medenine']
    if location in coastal_govs:
        return '1' 
    else:
        return '0'
