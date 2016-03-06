from tkinter import *
from cardgame import *

class Main :

    def __init__(self, parent) :
        self.parent = parent
        game = BuildScreen(self.parent)

        game.startGame()
        
        #menu section

        #menu outcomes
        self.aboutimg = PhotoImage(file = 'about.gif')
        
        
        menu = Menu(self.parent)
        self.parent.config(menu = menu)

        #file menu - restart and close
        filemenu = Menu(menu)
        menu.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Restart", command = self.restart)
        filemenu.add_separator()
        filemenu.add_command(label = "Close", command = self.parent.destroy)

        #help menu - about and help
        helpmenu = Menu(menu)
        menu.add_cascade(label = "Help", menu = helpmenu)
        helpmenu.add_command(label = "How to play", command = self.gamehelp)
        helpmenu.add_separator()
        helpmenu.add_command(label = "About Card-matching", command = self.about)

        setmenu = Menu(menu)
        menu.add_cascade(label = "Setting", menu = setmenu)
        setmenu.add_command(label = "clear the record", command = self.clear)
        
    def restart(self) :
        self.parent.destroy()
        root = Tk()
        game1 = Main(root)
        root.mainloop()

    def about(self) :
        abWin = Toplevel(self.parent)
        abLabel = Label(abWin, image = self.aboutimg)
        abLabel.pack()
        
    def gamehelp(self) :
        helpWin = Toplevel(self.parent)
        text2 = Text(helpWin, height=20, width=60, bg = 'dark blue')
        scroll = Scrollbar(helpWin, command=text2.yview)
        text2.configure(yscrollcommand=scroll.set)
        text2.tag_configure('bold_italics', foreground = 'white', font=('Arial', 12, 'bold', 'italic'))
        text2.tag_configure('big', foreground = 'light gray', font=('Verdana', 20, 'bold'))
        text2.tag_configure('color',  foreground = 'white', font=('Tempus Sans ITC', 12, 'bold'))
        text2.insert(END,'How to Play\n\n', 'big')
        quote = """This is card matching game.

First, enter your username, and choose the level.
Then the cards will appear.

There is total seven stages to clear.

Shape of the cards will be shown for given time.
You have to memorize as many as you can.

choose any card, and find the one that has same shape with it.

The less you mistake, the more you get a point.

And there is time bonus, so make it as fast as you can.

Good luck!"""
        text2.insert(END, quote, 'color')
        text2.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)

    def clear(self) :
        if askyesno("clear record", "Are you sure?"):
            chandle = open('score.txt', 'w')
            chandle.close()
            showwarning("Yes", "Record has been cleared")
                        

root = Tk()
game = Main(root)
root.title(string = "Card-matching")

root.mainloop()
