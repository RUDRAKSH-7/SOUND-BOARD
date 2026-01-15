from pyray import *
import csv
import sys
MAX_WIDTH = 1280; MAX_HEIGHT = 720
BG=(33, 39, 46,255)
FORE=(169, 199, 235,255)
HOVER=(169, 199, 235,150)
#loading last window size
with open("res/config.csv","r") as win:
    S_WIDTH, S_HEIGHT = tuple(csv.reader(win))[0]

# WINDOW INITIALIZE AND TEXTURES :
set_config_flags(ConfigFlags.FLAG_WINDOW_HIDDEN)
set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(int(S_WIDTH),int(S_HEIGHT),"SOUN BORE")
init_audio_device()
set_target_fps(90)

PAUSE = load_texture("res/pause.png")
PLAY = load_texture("res/play.png")
CDRIVE = load_texture("res/cdrive.png")
AUDIO_LIST = []
set_window_min_size(500,600)
set_window_max_size(MAX_WIDTH,MAX_HEIGHT)

is_file_button_clicked = False #initialize
path_string = "HELLO"
def file_path():
    global MAX_HEIGHT, MAX_WIDTH, CDRIVE, AUDIO_LIST, path_string
    

    if is_key_pressed(KeyboardKey.KEY_ENTER):
        return 0;


clear_window_state(128)
while (not window_should_close()):
    mouse = get_mouse_position()
    S_WIDTH,S_HEIGHT = get_screen_width(),get_screen_height()
    begin_drawing(); clear_background(BG)
    #Draw stuff:
    draw_text("=== Sounds ===",70,30,48,FORE)
    draw_rectangle(10,100,get_screen_width()-20,6,FORE)

    #check buttons and stuff
    for i in range(len(AUDIO_LIST)+1):
        if not check_collision_point_rec(mouse,(20,(140*(i+1))+20,S_WIDTH-40,120)):
            draw_rectangle_lines_ex((20,(140*(i+1))+20,S_WIDTH-40,120),5,FORE) #rectangle is the file open button for now
            draw_text(" + ",S_WIDTH//2-40,(140*(i+1))+60,48,FORE)
        else:
            draw_rectangle_lines_ex((20,(140*(i+1))+20,S_WIDTH-40,120),5,HOVER)
            draw_text(" + ",S_WIDTH//2-40,(140*(i+1))+60,48,FORE)
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                is_file_button_clicked = not is_file_button_clicked
    if is_file_button_clicked:
        draw_texture_ex(CDRIVE,(20,S_HEIGHT-(100*0.750)-20),0,0.7500,WHITE)
        draw_rectangle_lines_ex((20,S_HEIGHT-(100*0.750)-20,S_WIDTH-40,100*0.750),3,FORE)
        draw_text(path_string,110,S_HEIGHT-int(100*0.750),48,FORE)

        if is_key_pressed(KeyboardKey.KEY_ENTER):
            is_file_button_clicked = False
            print(path_string)
    
    end_drawing()
unload_texture(PLAY);unload_texture(PAUSE);
unload_texture(CDRIVE)

#storing last size to config.csv
with open("res/config.csv","w") as win:
    w = csv.writer(win)
    w.writerow([S_WIDTH,S_HEIGHT])

close_window()

sys.exit(0)