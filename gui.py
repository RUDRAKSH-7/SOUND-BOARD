from pyray import *
from pygame import mixer
import pickle as pk #instead of the CSV file planning did earlier this build uses binary format for performance and ease of use purposes
import os #Path lib and os module have the similar use case (to check the existence of path and search for music file)
from pathlib import Path #pathlib will convert % variables of windows directories to expanded file path strings
import sys # sys module will be used for terminal arguments however the functionality and use case is not yet tested
mixer.init()
MAX_WIDTH = 1280; MAX_HEIGHT = 720
BG=(33, 39, 46,255)
FORE=(169, 199, 235,255)
HOVER=(169, 199, 235,150)
#loading last window size
with open("res/co.nfig","rb") as win:
    S_WIDTH, S_HEIGHT = pk.load(win)

# WINDOW INITIALIZE AND TEXTURES :
set_config_flags(ConfigFlags.FLAG_WINDOW_HIDDEN)
set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(int(S_WIDTH),int(S_HEIGHT),"SOUN BORE")
set_target_fps(90)

PAUSE = load_texture("res/pause.png")
PLAY = load_texture("res/play.png")
CDRIVE = load_texture("res/cdrive.png")
ADD_BUTTON = load_texture("res/add.png")
MUS = mixer.music.load("res/greenroom.mp3")
AUDIO_LIST = []
#loading audios (text for now) from audio.sav
with open("res/audios.sav","r") as audio:
    AUDIO_LIST = audio.readlines()
print(AUDIO_LIST)

#THE VARIABLE X FOR SCROLL FUNCTIONALITY
X = 110
set_window_min_size(500,600)
set_window_max_size(MAX_WIDTH,MAX_HEIGHT)

is_file_button_clicked = False #initialize
path_string = ""

err_timer = 0
path_error = False
def err_show(screen_height):
    draw_rectangle_rec((20,screen_height-(100*0.750),280,60),BG)# background
    draw_rectangle_lines_ex((20,screen_height-(100*0.750),280,60),5,RED) #red outline
    draw_text("No Music File",60,screen_height-60,32,RED)

clear_window_state(128)
while (not window_should_close()):
    mouse = get_mouse_position()
    wheel = get_mouse_wheel_move()
    S_WIDTH,S_HEIGHT = get_screen_width(),get_screen_height()
    begin_drawing(); clear_background(BG)

    # scroll_wheel
    if wheel != 0:
        X+=int(wheel)*30

    #Drawing sound buttons:
    for i in range(len(AUDIO_LIST)):
        # THE SCROLL WHEEL FUNCTIONALITY IS ACHIEVED THRU THE VARIABLE 'X' = 140 INITIALLY, DE/INCREASED ACCORDINGLY
        audio_rect = (20,(X+80*(i))+(5*i),S_WIDTH-40,70)
        text_pos = 40,30+(X+80*(i))+(5*i)

        if not check_collision_point_rec(mouse,audio_rect):
            draw_rectangle_lines_ex(audio_rect,5,FORE)
            draw_text(AUDIO_LIST[i],text_pos[0],text_pos[1],32,FORE)
        else:
            draw_rectangle_lines_ex(audio_rect,5,HOVER)
            draw_text(AUDIO_LIST[i],text_pos[0],text_pos[1],32,HOVER)

    #Draw stuff:
    draw_rectangle(0,0,S_WIDTH,100,BG)
    draw_text("SOUN-BORE",70,30,48,FORE)
    draw_rectangle(10,100,S_WIDTH-20,6,FORE)
    #check buttons and stuff
    # This button (+) will allow you to add a new audio to the list
    # if its pressed again the input entered into the textbox will be discarded
    if not check_collision_point_rec(mouse,(S_WIDTH-300,20,280,70)):
        #rectangle is the file open button for now (later it will be at a different position)
        # draw_rectangle_lines_ex((S_WIDTH-300,20,280,70),5,FORE) 
        draw_texture_ex(ADD_BUTTON,(S_WIDTH-300,20),0,1,WHITE)
        # draw_text(" + ",S_WIDTH-190,35,48,FORE)
    else:
        draw_texture_ex(ADD_BUTTON,(S_WIDTH-300,20),0,1,GRAY)
        # draw_text(" + ",S_WIDTH-190,35,48,HOVER)
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            path_string = ""
            is_file_button_clicked = not is_file_button_clicked
            path_error = False
            set_window_state(ConfigFlags.FLAG_WINDOW_RESIZABLE)

    
    # checking for user input and also, the existence of the path entered
    # this is going to return a RED popup if the file doesn't exist at the given path
    # or will add the file to list if it exists and will be loaded into the audio list
    if is_file_button_clicked:
        clear_window_state(ConfigFlags.FLAG_WINDOW_RESIZABLE)
        draw_texture_ex(CDRIVE,(20,S_HEIGHT-(100*0.750)-20),0,0.7500,WHITE)
        draw_rectangle_lines_ex((20,S_HEIGHT-(100*0.750)-20,S_WIDTH-40,100*0.750),3,FORE)
        draw_text(path_string,110,S_HEIGHT-int(100*0.750),28,FORE)
        
        # getting character pressed and appending it only if the char integer != 0
        char = get_char_pressed()
        if char != 0:
            path_string += chr(char)
        if is_key_pressed(KeyboardKey.KEY_BACKSPACE):
            path_string = path_string[:-1]
        if is_key_pressed(KeyboardKey.KEY_ENTER):
            is_file_button_clicked = False
            set_window_state(ConfigFlags.FLAG_WINDOW_RESIZABLE)

            #if path_string include a %USERPROFILE% kind of path (relative) then 'c:\' will be discarded and relative path will be checked
            path_string = fr"c:/{path_string}" if path_string[0] != "%" else os.path.expandvars(path_string)
            print(path_string)
            
            if os.path.exists(path_string) and (path_string.endswith(".wav") or path_string.endswith(".mp3")):
                print(True)
                AUDIO_LIST.append(path_string)
                with open("res/audios.sav","a+") as audio:
                    audio.write(f"{path_string}\n")
            else: # Displaying error message now (for 3 secs)
                path_error = True
            path_string = "" #resetting path string for next input
    if path_error:
        err_timer += 1/90
        if err_timer <= 3:
            err_show(S_HEIGHT)
        else:
            err_timer = 0
            path_error = False
    end_drawing()

unload_texture(PLAY);unload_texture(PAUSE);
unload_texture(CDRIVE); unload_texture(ADD_BUTTON)
#storing last size to config.csv
with open("res/co.nfig","wb") as win:
    pk.dump((S_WIDTH,S_HEIGHT),win)
close_window()
mixer.quit()
sys.exit(0)
