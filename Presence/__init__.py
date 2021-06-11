# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Presence",
    "author" : "mey",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import atexit
import datetime
import os
import subprocess
import time
from sys import platform

import bpy
from bpy.app.handlers import persistent
from discoIPC import ipc

# Settings
showFilename = True;
showTimeElapsed = True;

base_activity = {
    'assets': {
        'large_image': 'blender',
        'large_text': 'Blender ' + bpy.app.version_string.split(" ")[0],
        'small_image': 'default_file',
        'small_text': '(Untitled)'
    },
    'timestamps': {},
}

pid = os.getpid()
objcount = 0
timeElapsed = int(time.time())
active = 0
rendering = 0
rendertime = 0

client = ipc.DiscordIPC('817084302847246346') # Replace your clientID with the 18 digit template
client.connect()
print('\nStarting Discord ICP ...\n')

@atexit.register
def disconnect():
    main()
    print('Disconnecting Discord ICP ...\n')
    client.disconnect()

@persistent
def main():
    client.update_activity(set_activity())

@persistent
def resetTime(scene):
    bpy.ops.wm.modal_timer_operator()

@persistent
def render_begin(scene):
    global rendering
    global rendertime
    global active
    rendering = 1
    active = 2
    rendertime = int(time.time())

@persistent
def render_cancel(scene):
    global rendering
    global rendertime
    global active
    rendering = 0
    rendertime = 0
    active = 1

@persistent
def render_complete(scene):
    global rendering
    global rendertime
    global active
    rendering = 0
    rendertime = 0
    #time_taken = int(time.time()) - int(rendertime)
    #time_end = int(time.time())
    active = 1

@persistent
def set_activity():
    global rendering
    global rendertime
    global objcount

    if platform == "linux" or platform == "linux2":
        if not subprocess.getstatusoutput('xdotool')[0] == 0:
            pidcheck = subprocess.getstatusoutput('xdotool getwindowfocus getwindowpid')[1]

            if not str(pidcheck) != str(pid):
                if rendering == 1:
                    active = 2
                else:
                    active = 0
            else:
                if rendering == 1:
                    active = 2
                else:
                    active = 0
    else:
        if rendering == 1:
            active = 2
        else:
            active = 0

    #Set activity for the player
    activity = base_activity
    if showFilename == True:
        if bpy.path.basename(bpy.context.blend_data.filepath)[:-6]:
            activity['assets']['small_text'] = bpy.path.basename(bpy.context.blend_data.filepath)[:-6]
        else:
            activity['assets']['small_text'] = "(Untitled)"

    if active == 0:
        string = bpy.context.mode.split("_")
        string1 = string[0].lower().capitalize()

        if len(string) > 1:
            string1 = string1 + " " + string[1].lower().capitalize()

        activity['details'] = string1 + " Mode"
    elif active == 1:
        activity['details'] = 'Idle'
    elif active == 2:
        activity['details'] = 'Rendering for ' + '0' + str(datetime.timedelta(seconds=((int(time.time() - rendertime))))) # Hacky

    if bpy.context.mode == "OBJECT" and active != 2:
        count = len(bpy.data.objects)
        activity['state'] = '(' + str(len(bpy.context.selected_objects)) + '/' + str(count) + ' ' + ("object" if count == 1 else "objects") + ' selected)'
    else:
        if active != 2:
            ob = bpy.context.object
            ob.update_from_editmode()

            if ob.type == "MESH":
                count = len(bpy.context.object.data.vertices)
                selected = len([v.index for v in bpy.context.object.data.vertices if v.select])
                activity['state'] = '(' + str(selected) + '/' + str(count) + ' ' + ("vertex" if count == 1 else "vertices") + ' selected)'
            elif ob.type == "ARMATURE":
                count = len(bpy.context.object.data.bones)
                selected = len([b.name for b in bpy.context.object.data.bones if b.select])
                activity['state'] = '(' + str(selected) + '/' + str(count) + ' ' + ("bone" if count == 1 else "bones") + ')'
                
        else:
            activity['state'] = "Frame " + str(bpy.context.scene.frame_current) + "/" + str(bpy.context.scene.frame_end - bpy.context.scene.frame_start)

    if showTimeElapsed == True:
        activity['timestamps']['start'] = timeElapsed

    return activity

timerfile = 0
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    @persistent
    def modal(self, context, event):
        if event.type == 'TIMER':
            global filename
            global timerfile
            
            if time.time() - timerfile > 0.05:
                timerfile = time.time()
                main()

        return {'PASS_THROUGH'}

    @persistent
    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(2, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    @persistent
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.app.handlers.load_post.append(resetTime)
    bpy.app.handlers.render_pre.append(render_begin)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_complete.append(render_complete)
    bpy.app.handlers.load_post.append(resetTime)
    bpy.ops.wm.modal_timer_operator()


def unregister():
    bpy.app.handlers.load_post.remove(resetTime)
    bpy.app.handlers.render_complete.remove(render_complete)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_pre.remove(render_begin)
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()



