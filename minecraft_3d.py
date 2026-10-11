from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os
import sys
import random
import assets.soundHandler as sH
import threading
import assets.trial as trial
tri = threading.Thread(target=trial.show_expired_dialog)
tri.start()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Ursina()

# --- CONFIG ---

with open("./assets/colors.json", 'r') as coj:
    blocks = json.loads(coj.read())

print(blocks)

current_block_id = "1"

# --- SOUND ---
def play_sfx(key):
    sH.sound(key)

selector = Entity(
    model='cube',
    color=color.black,
    scale=1,
    alpha=0.4,
    enabled=False
)
selector.wireframe = True

class Voxel(Button):
    def __init__(self, position=(0,0,0), block_id="1"):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0,
            texture='assets/textures/grass.bmp',
            pressed_color=color.clear,
        )
        self.block_id = block_id
        self.update_appearance()

    def update_appearance(self):
        data = blocks.get(self.block_id, blocks["1"])
        highlight_color=color.rgb(data['color'][0], data['color'][1], data['color'][2])
        self.color = color.rgb(data['color'][0], data['color'][1], data['color'][2])
        match self.block_id:
            case "1":
                self.texture = 'assets/textures/grass.bmp'
            case "2":
                self.texture = 'assets/textures/stone.bmp'
            case "3":
                self.texture = 'assets/textures/dirt.bmp'
            case "4":
                self.texture = 'assets/textures/brick.bmp'
            case _:
                self.texture = 'white_cube'

    def input(self, key):
        if self.hovered:
            # --- PLACE ---
            if key == 'right mouse down':
                play_sfx('place')
                Voxel(position=self.position + mouse.normal, block_id=current_block_id)

            # --- BREAK ---
            if key == 'left mouse down':
                play_sfx('break')
                destroy(self)
                selector.enabled = False

def update():
    global current_block_id

    if held_keys['escape']:
        os._exit(0)

    if mouse.hovered_entity and isinstance(mouse.hovered_entity, Voxel):
        selector.enabled = True
        selector.position = mouse.hovered_entity.position
    else:
        selector.enabled = False
    
    # Hotbar
    if held_keys['1']: current_block_id = "1" # grass
    if held_keys['2']: current_block_id = "2" # stone
    if held_keys['3']: current_block_id = "3" # dirt
    if held_keys['4']: current_block_id = "4" # brick
    if held_keys['r']: player.x = 10; player.y = 10
    
    # updation
    hand_text.text = f"Block: {blocks[str(current_block_id)]['name']}"

# world gen
for z in range(20):
    for x in range(20):
        voxel = Voxel((x,0,z), block_id="2")
        voxel = Voxel((x,1,z), block_id="2")
        voxel = Voxel((x,2,z), block_id="3")
        voxel = Voxel((x,3,z), block_id="1")
        if random.randint(0,4)==1: voxel = Voxel((x,4,z), block_id="4")
        
        


# --- PLAYER & CAMERA ---
player = FirstPersonController()
player.x = 10
player.y = 30

# --- SKYBOX ---
sky = Sky()
sky.color = color.rgb(0.4, 0.7, 0.9) # Sky Blue

# --- UI OVERLAY ---
hand_text = Text(text='Block: Grass', position=(-0.85, 0.45), scale=2, color=color.black)
info_text = Text(
    text='WASD MOVE | SPACE JUMP | LEFT CLICK BREAK | RIGHT CLICK PLACE',
    position=(-0.85, 0.40), 
    scale=1,
    color=color.black
)

app.run()
