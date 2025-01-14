from evennia.contrib.grid import wilderness
from PIL import Image
from evennia.utils import logger

room_names = {(0,0,255):     "deep water",
              (0, 64,255):   "shallows",
              (255, 255, 0): "beachfront",
              (0, 255, 0):   "grassland",
              (0, 128, 0):   "woodland",
              (255,128,0):   "desert",
              (128,128,128): "hills",
              (64,64,64):    "mountains",}

room_descriptions = {"deep water": "This is very deep water, dangerous to swim in.",
                     "shallows":   "This is shallow water, can stand up in some places.",
                     "beachfront": "This is a sandy beachfront.",
                     "grassland":  "This is a stretch of rolling grassland.",
                     "woodland":   "This is a stretch of heavily wooded forest.",
                     "desert":     "This is a stretch of dry desert land.",
                     "hills":      "This is a stretch of hills, from rolling to rocky.",
                     "mountains":  "This is a stretch of very mountainous terrain, steep slopes and sheer cliffs."}

image_location = 'world/small_island_test.png'
pic = Image.open(image_location, 'r').convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)


#@py from world.wilderness_zones import test_island as ti; ti.wilderness.create_wilderness(mapprovider=ti.TestIslandMapProvider())
#@py from evennia.contrib.grid import wilderness; wilderness.enter_wilderness(me, coordinates=(0,0))
class TestIslandMapProvider(wilderness.WildernessMapProvider):
    def is_valid_coordinates(self, wilderness, coordinates):
        "Validates if these coordinates are inside the map"
        x, y = coordinates
        #y = pic.height - y - 1
        logger.log_msg('is_valid_coordinates - name: TestIslandProvider')
        if x < 0 or x >= pic.width or y < 0 or y >= pic.height:
            logger.log_msg('is_valid_coordinates: Not Valid Room - ' + str(coordinates))
            return False
        pixel = pic.getpixel((x, y))
        
        if pixel == (0,0,0):
            logger.log_msg('is_valid_coordinates: Not Valid Room - ' + str(coordinates))
            return False

        
        logger.log_msg('is_valid_coordinates: Valid Room - ' + str(coordinates))
        return True

    def get_location_name(self, coordinates):
        "Set the location name"
        x, y = coordinates
        #y = pic.height - y - 1
        pixel = pic.getpixel((x,y))
        room_name = 'unknown'
        try: 
            return room_names[pixel]
        except KeyError:
            logger.log_msg('get_location_name: Invalid Key - ' + str((coordinates, pixel)))
            return room_name

    def at_prepare_room(self, coordinates, caller, room):
        "Any other changes done to the room before showing it"
        x, y = coordinates
        #y = pic.height - y - 1
        pixel = pic.getpixel((x,y))
        logger.log_msg('at_prepare_room: Pixel - ' + str((coordinates, pixel)))
        try: 
            room_name = room_names[pixel]
            room.ndb.active_desc = room_descriptions[room_name]
        except KeyError:
            logger.log_msg('at_prepare_room: Invalid Key - ' + str((coordinates, pixel)))
            caller.msg(str((x,y))+ " " + str(pixel))