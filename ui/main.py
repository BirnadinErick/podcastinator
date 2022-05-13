import curses
from ui._utils import *
from ui.consts import *
import json


# begin bootstrap dummy data --------------------------------------------------------
def get_subs():
    with open('dummy/subs.json', 'r') as file:
        return json.load(file)

def get_epi():
    with open('dummy/epi.json', 'r') as file:
        return json.load(file)
# end bootstrap dummy data ----------------------------------------------------------

# begin strings --------------------------------------------------------
TITLE:str = "PODCASTINATOR  v1.0.0"
CMDS_HELP:str = "Quit(: + q);  Settings(: + s)"
now_playing:str = "Nothing Playing Now, Play some podcast and enjoy your time"

# end strings ----------------------------------------------------------


def main(scr):
    global TITLE, CMDS_HELP, now_playing, time
    
    clear_refresh(scr)
    curses.start_color()
    curses.init_pair(1, RED, BLACK)
    curses.init_pair(2, CYAN, BLACK)
    curses.init_pair(3, YELLOW, BLACK)

    PRIMARY = curses.color_pair(1)
    SECONDARY = curses.color_pair(2)
    HIGHLIGHT = curses.color_pair(3)
    HEIGHT, WIDTH = scr.getmaxyx()
    pdtitle:str = ""
    pdauthor:str = ""
    cursor_x = 0
    cursor_y = 0

    titlebar = curses.newwin(1,WIDTH,0,0)
    mainarea_l = curses.newwin(HEIGHT-4, WIDTH//2,1,0)
    mainarea_r = curses.newwin(HEIGHT-4, WIDTH//2,1,WIDTH//2)
    statusbar = curses.newwin(3, WIDTH, HEIGHT-3,0)

    def f5_win():
        titlebar.refresh()
        mainarea_l.refresh()
        mainarea_r.refresh()
        statusbar.refresh()

    mainarea_l.border('|', '|', '-','_', '+', '+', '+', '+')
    mainarea_r.border('|', '|', '-','_', '+', '+', '+', '+')

    titlebar.attron(PRIMARY|curses.A_REVERSE)
    mainarea_l.attron(SECONDARY)

    titlebar.addstr(f"{TITLE} {' '*(WIDTH-(len(TITLE)+len(CMDS_HELP)+3))} {CMDS_HELP}")

    f5_win()
    subs = get_subs()["subs"]
    epis = get_epi()["BEngShow"]
    cmd_mode = False
    cursor_last = (0,0)
    subs_loc = {}
    epi_loc = {}
    sub_pg, epi_pg = {}, {'now':1, 'total':4}

    while True:
        statusbar.addstr(0,0,f"{now_playing}{' '*(WIDTH-len(now_playing))}", HIGHLIGHT)
        statusbar.addstr(1,0,f"{pdtitle} {'by' if pdtitle != '' else '  '} {pdauthor} {' '*(WIDTH-(len(pdtitle)+ 4+len(pdauthor)+1))}", HIGHLIGHT|curses.A_ITALIC|curses.A_REVERSE)

        mainarea_l.addstr(1,1, "Subscriptions", SECONDARY|curses.A_REVERSE|curses.A_BOLD)
        mainarea_l.addstr(2,1, "-"*(WIDTH//2-2), SECONDARY)
       
        for i in range(len(subs)):
            mainarea_l.addstr(i+3, 4, str(subs[i]).title())
            subs_loc[i+3] = subs[i]

        f5_win()
        key = scr.getch()

        try:
            if key == ord('q'):
                if cmd_mode:
                    break
            elif key == ord(':'):
                cmd_mode = True
            elif key == curses.KEY_DOWN:
                cursor_y = cursor_y + 1
            elif key == curses.KEY_UP:
                cursor_y = cursor_y - 1
            elif key == curses.KEY_RIGHT:
                cursor_x = cursor_x + 1
            elif key == curses.KEY_LEFT:
                cursor_x = cursor_x - 1
            elif key == curses.KEY_IC:
                if cursor_x >= WIDTH//2:
                    try:
                        pdtitle = epi_loc[cursor_y-1]
                        pdauthor = "Dummy Author"
                        now_playing = "Now Playing:"
                        pipe_to_kernel(epi_loc[cursor_y-1])
                        continue
                    except KeyError:
                        pass

                else:
                    mainarea_r.erase()
                    mainarea_r.border('|', '|', '-','_', '+', '+', '+', '+')

                    try:
                        sub = subs_loc[cursor_y-1]
                        mainarea_r.addstr(1,1, str(sub),SECONDARY|curses.A_REVERSE|curses.A_BOLD)
                        mainarea_r.addstr(2,1, "-"*(WIDTH//2-2), SECONDARY)
                        
                        pagination = f"{epi_pg['now']} of {epi_pg['total']}"
                        mainarea_r.addstr(1, WIDTH//2-(len(pagination)+3), pagination)

                        i = 2
                        for epi in epis:
                            # epi = epis[i]
                            mainarea_r.addstr(i+1, 2, f"+ {epi['title']}"[:(WIDTH//2)-5], HIGHLIGHT)
                            mainarea_r.addstr(i+2, 6, epi["summary"][:(WIDTH//2)-10]+"...", HIGHLIGHT)
                            epi_loc[i+1] = epi['title']
                            i += 2

                    except KeyError:
                        pass
                    else:
                        cursor_last = (cursor_y, cursor_x)
                        cursor_y, cursor_x = 4, WIDTH//2+1
            elif key == curses.KEY_DC:
                try:
                    mainarea_r.erase()
                    mainarea_r.border('|', '|', '-','_', '+', '+', '+', '+')
                    cursor_y, cursor_x = cursor_last
                except:
                    pass
            elif key == curses.KEY_PPAGE:
                if cursor_x >= WIDTH//2:
                    epi_pg['now'] = epi_pg['now']-1 if epi_pg['now'] > 1 else 1
                    pagination = f"{epi_pg['now']} of {epi_pg['total']}"
                    mainarea_r.addstr(1, WIDTH//2-(len(pagination)+3), pagination)
                    i = 2
                    for epi in epis:
                        mainarea_r.addstr(i+1, 2, f"- {epi['title']}"[:(WIDTH//2)-5], HIGHLIGHT)
                        mainarea_r.addstr(i+2, 6, epi["summary"][:(WIDTH//2)-10]+"...", HIGHLIGHT)
                        epi_loc[i+1] = epi['title']
                        i += 2
                else:
                    pass
            elif key == curses.KEY_NPAGE:
                if cursor_x >= WIDTH//2:
                    epi_pg['now'] = epi_pg['now']+1 if epi_pg['now'] < epi_pg['total'] else epi_pg['total']
                    pagination = f"{epi_pg['now']} of {epi_pg['total']}"
                    mainarea_r.addstr(1, WIDTH//2-(len(pagination)+3), pagination)
                    i = 2
                    for epi in epis:
                        mainarea_r.addstr(i+1, 2, f"* {epi['title']}"[:(WIDTH//2)-5], HIGHLIGHT)
                        mainarea_r.addstr(i+2, 6, epi["summary"][:(WIDTH//2)-10]+"...", HIGHLIGHT)
                        epi_loc[i+1] = epi['title']
                        i += 2
                else:
                    pass
            else:
                pass
            
            cursor_x = max(0, cursor_x)
            cursor_x = min(WIDTH-1, cursor_x)

            cursor_y = max(0, cursor_y)
            cursor_y = min(HEIGHT-1, cursor_y)
            scr.move(cursor_y, cursor_x)

        except curses.ERR:
            pass
        else:
            pass
        
if __name__ == "__main__":
    curses.wrapper(main)