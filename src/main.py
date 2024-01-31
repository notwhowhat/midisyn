import time 
import random
import rtmidi
from rich.console import Console, Group
from rich.padding import Padding
from rich.live import Live
from rich.style import Style
from rich.table import Table

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
#midiout.open_port(1)

console = Console()

class Note:
    def __init__(self, key: int, velocity: int, start: int, end: int) -> None:
        self.key: int = key
        self.velocity: int = velocity
        self.start: int = start
        self.end: int = end

        self.sent: str = 'empty'

    def message(self, now: int) -> tuple:
        # will send out an apropriate midi message according to if it's on or not.
        if self.start < now:
            if self.end < now:
                if self.sent != 'off':
                    # it should be off, but it isn't, cause it's
                    # the first time, shown by sent not being off
                    self.sent = 'off'
                    return (0x80, self.key, self.velocity)
            elif self.sent == 'empty':
                # it is time to start, but it hasn't done it before, because it's empty
                self.sent = 'on'
                return (0x90, self.key, self.velocity)



def main() -> None:
    keys: list = []
    for n in range(21, 127):
        # in every one of these lists, the note events will be.
        keys.append([])

    # these note tuples will be ordered in a specific way:
    # note name, note value, time
    #notes[60].append((0x90, 112, 0))
    #notes[60].append((0x80, 0, 500_000_000))
    keys[60].append(Note(60, 112, 0, 500_000_000))
    keys[62].append(Note(62, 112, 500_000_000, 1_000_000_000))
    #keys[62].append(Note(62, 112, 1_500_000_000, 2_000_000_000))



    #white: Style = Style(color='blue on white')
    #roll: list = []
    #roll.append(('C#    ', 'white on black'))
    #roll.append(('C    ', 'black on white'))
    # this will be how many ns a char is
    scale: int = 500_000_000
    key: list = []
    for i in range(16):
        key.append(' ')
    for note in keys[62]:
        #for i in range(int((note.end - note.start) / scale)):
        index = int(note.start / scale)
            #print(index)
            #key[int(note.start % scale)] = 'O'
        key[index] = 'O'
            #key[i] = 'O'


    with Live(refresh_per_second=30) as live:
        while 1:
            console.clear()
            #for i in range(10):
                #console.print(random.choice(['hi', 'bye']), style='blue on white')#'#FF0000')
            #for key in roll:
                #console.print(key[0], style=key[1])
            #console.print('|[black on white]C    [/]#')
            console.print(str(key))
            pass

    start = time.time_ns()
    while 1:
        for key in keys:
            for note in key:
                now = time.time_ns() - start
                message: tuple = note.message(now)
                if message != None:
                    midiout.send_message(message)

def midi_stuff():
    print(available_ports)
    if available_ports:
        midiout.open_port(0)

    with midiout:
        note_on = [0x90, 60, 112]
        note_off = [0x80, 60, 0]

        for i in range(8):
            midiout.send_message([0x90, 60, 112])
            time.sleep(0.125)
            midiout.send_message([0x90, 60, 0])
            time.sleep(0.125)

            midiout.send_message([0x90, 48, 112])
            time.sleep(0.125)
            midiout.send_message([0x90, 48, 0])
            time.sleep(0.125)

def print_stuff():
    table = Table()

    table.add_column("Row ID")
    table.add_column("Description")
    table.add_column("Level")

    with Live(console=console, refresh_per_second=4) as live:
        for row in range(12):
            time.sleep(0.4)
            table.add_row(f"{row}", f"description {row}", "[red]ERROR")

            console.print(random.choice(['hi', 'hello', 'bye']))

           

            

if __name__ == '__main__':
    main()
    del midiout
