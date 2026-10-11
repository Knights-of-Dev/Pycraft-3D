from ursina import *

def sound(key):
    match key:
        case 'break':
            Audio('sound/break.wav', pitch=random.uniform(0.8, 1.2), loop=False, autoplay=True)
        case 'place':
            Audio('sound/place.wav', pitch=random.uniform(0.8, 1.2), loop=False, autoplay=True)
