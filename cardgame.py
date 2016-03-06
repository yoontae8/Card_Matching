from tkinter import *
from tkinter.messagebox import *
from score import *
import random
import time

class BuildScreen :

    def __init__(self, parent) :
        self.parent = parent
        
        #stage variables
        self.cardnum = 6
        self.stage = 0

        #score variables
        self.totalScore = 0

        #time variables
        self.totalTime = 0.0    # total elapsed time
        
        # the outmost frame
        self.main = Frame(parent)
        self.main.grid()

        # title bar 
        self.title = Frame(self.main, relief = RIDGE, borderwidth = 2)
        self.title['background']='cyan'
        self.title.pack(fill = BOTH)

        self.titleLabel = Label(self.title, text = "Card Matching", font = "Times 30", bg="cyan")
        self.titleLabel.pack(ipadx = 10, ipady = 10)

        self.tryLabel = Label(self.title, bg = 'cyan', relief = RAISED, borderwidth = 2)
        self.tryLabel.pack(fill = X, expand = YES)

        self.trytext = Label(self.tryLabel, bg = 'cyan')
        self.trytext.pack(side = RIGHT)

        self.difficulty = Label(self.tryLabel, bg = 'cyan')
        self.difficulty.pack(side = LEFT)

        # game board
        self.board = Frame(self.main, relief = RIDGE, borderwidth = 10, bg = 'light green')
        self.board.pack(fill=BOTH)

        # information panel
        self.info = Frame(self.main, height = 50,background = 'brown')
        self.info.pack(expand = YES, fill=BOTH)

        self.timeLabel = Label(self.info, bg = 'brown', fg = 'white')
        self.timeLabel.pack(side = RIGHT)

        self.scoreLabel = Label(self.info, bg = 'brown', fg = 'white')
        self.scoreLabel.pack(side = LEFT)

        
        # tuple of card lists
        self.imgtuple = ('0flash.gif', '1heart.gif', '2hydra.gif', '3note.gif',
                         '4pyramid.gif', '5skull.gif', '6star.gif', '7sun.gif',
                         '8temple.gif', '9yinyang.gif')
        
        random.seed()

    # get username
    def startGame(self) :
        self.username = ""

        self.inputLabel = Label(self.board, text = "Enter Username\n", font = "Helvetica 13", bg = 'light green')
        self.inputLabel.pack(padx = 5, pady = 3)
        self.inputEntry = Entry(self.board)
        self.inputEntry.focus_force()
        self.inputEntry.bind('<Return>', self.confirm)
        self.inputEntry.pack()
        self.okBtn = Button(self.board, text ="start", command = self.confirm)
        self.okBtn.pack()

    #take care of the username input
    def confirm(self, event = None) :
        if len(self.inputEntry.get()) > 10 :
            self.inputLabel.configure(text = "Username is\ntoo long")
        elif ':' in self.inputEntry.get() :
            self.inputLabel.configure(text = "Do not \nuse :")
        elif self.inputEntry.get() == '' :
            self.inputLabel.configure(text = "type \nsomething")
        else :
            self.username = self.inputEntry.get()
            self.inputLabel.destroy()
            self.inputEntry.destroy()
            self.okBtn.destroy()
            self.level()

    def level(self) :
        self.askLabel = Label(self.board, text = "Level of difficulty", font = "Helvetica 13", bg = 'light green')
        self.askLabel.pack(padx = 5, pady = 6)
        self.easyBtn = Button(self.board, text = 'Easy', font = 'Verdana 11', bg = 'light blue', fg = 'white', width = 8, command = lambda: self.setLevel(0.8, 'Easy'))
        self.easyBtn.pack(pady = 2)
        self.standardBtn = Button(self.board, text = 'Standard', font = 'Verdana 11', bg = 'blue', fg = 'white', width = 8, command = lambda: self.setLevel(1, 'Standard'))
        self.standardBtn.pack(pady = 2)
        self.hardBtn = Button(self.board, text = 'Hard', font = 'Verdana 11', bg = 'dark blue', fg = 'white', width = 8, command = lambda: self.setLevel(1.2, 'Hard'))
        self.hardBtn.pack(pady = 2)
        self.extremeBtn = Button(self.board, text = 'Extreme', font = 'Verdana 11', bg = 'purple', fg = 'white', width = 8, command = lambda: self.setLevel(1.4, 'Extreme'))
        self.extremeBtn.pack(pady = 2)

    def setLevel(self, lfactor, lstring) :
        self.lfactor = lfactor
        self.dif = lstring
        self.askLabel.destroy()
        self.easyBtn.destroy()
        self.standardBtn.destroy()
        self.hardBtn.destroy()
        self.extremeBtn.destroy()
        self.drawCards()

    #draw the Cards on the board, for each stage
    def drawCards(self) :
        # initial variable setting
        self.stage += 1
        self.cardnum += 2
        self.stageScore = 0
        self.addScore = int(100 + 10 * self.stage * self.lfactor)   # score for each currect choices
        self.column = self.cardnum // 2
        self.count = 0
        self.chance = int((self.stage * 2 + 5) * self.lfactor)
        self.select = True      # distinguishes the first click & second click
        self.blockClick = False   # block click event while showing wrong choice
        
        
        # time start
        self.start = time.time()
        self.run = True     # is gaming running?(when showing the result, stop)
        self.update()

        # set screen
        self.scoreLabel.configure(text = self.totalScore)
        if self.stage == 7 :
            self.titleLabel.configure(text = "Final Stage")
        else :
            self.titleLabel.configure(text = "Stage %d" % self.stage)

        self.trytext.configure(text = 'remaining tries : %02d' % self.chance)
        self.difficulty.configure(text = self.dif)

        # create image object
        self.imgObject = list()       # stores card image object
        self.imginfo = list()   # stores card information for check matching
        
        self.apply = self.imgtuple[:self.cardnum // 2]  # card shape to use
        self.apply *= 2
        self.apply = random.sample(self.apply, self.cardnum)    # mix the order
        ###hint for professor###
        print(self.apply[:len(self.apply)//2])
        print(self.apply[len(self.apply)//2:])

        for i in range(self.cardnum) :
            self.imgObject.append(PhotoImage(file = self.apply[i]))
            self.imginfo.append(int(self.apply[i][0]))
        self.backimg = PhotoImage(file = 'back.gif')

        # card setting
        self.card = list() # save
        for i in range(self.cardnum) :
            self.card.append(Button(self.board))
            
        k = 0
        for i in range(2) :
            for j in range(self.column) :
                self.card[k].configure(image = self.imgObject[k])
                self.card[k].grid(row = i, column = j, padx = 10, pady = 20)
                k += 1

        #after given seconds, flip the cards
        self.board.after(int((self.stage * 500 + 500) * ((1.4 - self.lfactor) * 2.5)), lambda: self.showBackAll())

    #turn all the cards to show the backside
    def showBackAll(self) :
        k = 0
        for i in range(2) :
            for j in range(self.column) :
                self.card[k].configure(image = self.backimg,
                                       command = lambda kind = k : self.cardChosen(kind))
                self.card[k].grid(row = i, column = j, padx = 10, pady = 20)
                k += 1
    #turn chosen cards to show the backside
    def showBack(self, num) :
        self.card[num].configure(image = self.backimg,
                                 command = lambda kind = num : self.cardChosen(kind))

    #take care of the card chosen event
    def cardChosen(self, kind) :
        # when showing the wrong result, do nothing
        if self.blockClick == True :
            return
        # flip and show the card image, and delete the event
        self.card[kind].config(image = self.imgObject[kind])
        self.card[kind].config(command = lambda: self.donothing())

        # at click 1/2
        if self.select :
            self.idx = kind     #save the card index
            self.select = False
            
        # at click 2/2 
        else :
            # if not matching with previous click
            if self.imginfo[self.idx] != self.imginfo[kind] :
                self.chance -= 1
                self.trytext.config(text = 'remaining tries : %02d' % self.chance)
                #deduce the incremental point by 30
                if self.addScore > 30 :     # minimum 10 point
                    self.addScore -= 30
                self.blockClick = True
                #show the choice for 0.7 second, and flip it again
                self.board.after(700, lambda: self.showBack(kind))
                self.board.after(700, lambda: self.showBack(self.idx))
                self.board.after(700, lambda: self.changeValue())   # block the other clicks
                #if wrong choice gets more than given time, game over
                if self.chance == 0 :
                    self.run = False    #stop the timer
                    showwarning(title = "Stage %d" % self.stage,
                             message = " [ Game Over ] ")
                    self.main.configure(bg = 'light green')
                    self.board.destroy()
                    self.info.destroy()
                    self.tryLabel.destroy()
                    self.titleLabel.configure(text = "Game Over")
                    self.scoreTitleLabel = Label(self.main, font = "Helvetica 20", bg = 'light green', text = "Record")
                    self.scoreTitleLabel.pack()
                    self.scoreboard = Frame(self.main, bg = 'light green')
                    self.scoreboard.pack(pady = 3)


                    sc = Score('score.txt')
                    self.slist = sc.getslist(self.username, self.totalScore)
                    self.sclistLabel = list()

                    if (self.username, self.totalScore) in self.slist :
                        for i in range(len(self.slist)) :
                            self.sclistLabel.append(Label(self.scoreboard))
                            self.sclistLabel[i].configure(font = "Times 11", text = "%02d : %10s\t%6s" % (i+1, self.slist[i][0], self.slist[i][1]),  bg = 'light green')
                            self.sclistLabel[i].pack()
                        for i in range(len(self.slist)) :
                            if self.username == self.slist[i][0] :
                                self.sclistLabel[i].configure(font = "Times 11 bold", relief = RIDGE, borderwidth = 1)
                                break
                    else :
                        for i in range(len(self.slist)) :
                            self.sclistLabel.append(Label(self.scoreboard))
                            self.sclistLabel[i].configure(font = "Times 11", text = "%02d : %10s\t%6s" % (i+1, self.slist[i][0], self.slist[i][1]),  bg = 'light green')
                            self.sclistLabel[i].pack()
                        self.outLabel = Label(self.scoreboard)
                        self.outLabel.configure(font = "Times 11 bold", text = "-- : %10s\t%6s" % (self.username, self.totalScore),  bg = 'light green', relief = RIDGE, borderwidth = 1)
                        self.outLabel.pack(pady = 5)
                        
                    self.closeBtn = Button(self.main, text = "finish", command = self.parent.destroy, bg = 'green')
                    self.closeBtn.pack(pady = 4)
                    
            #if choice matches
            else :
                self.stageScore += self.addScore
                self.scoreLabel.configure(bg = 'brown', fg = 'white', text = str(self.totalScore + self.stageScore))
                self.addScore = int(100 + 10 * self.stage * self.lfactor)   # initialize the addScore
                self.count += 1
                
                #stage clear
                if self.count == self.cardnum / 2 : 
                    self.run = False    #stop the timer
                    self.timeBonus= int((30.0 * self.stage - self.etime) * self.lfactor) # timebonus : (stagenumber) minutes - elapse seconds
                    if self.timeBonus < 0 :
                        self.timeBonus = 0
                    self.prevScore = self.totalScore
                    self.totalScore += self.stageScore + self.timeBonus
                    self.totalTime += self.etime
                    showinfo(title = "Stage %d" % self.stage,
                             message = " [Stage Clear]\n\nPrev Score  : %5d\nStage Score : %5d\nTime Bonus : %5d\n\n----------------------\nTotal Score  : %5d" % (self.prevScore, self.stageScore, self.timeBonus, self.totalScore))
                    if self.stage < 7 :
                        for i in range(self.cardnum) :
                            self.card[i].destroy()
                        self.drawCards()
                    # All clear
                    else :
                        self.main.configure(bg = 'light green')
                        self.board.destroy()
                        self.info.destroy()
                        self.tryLabel.destroy()
                        self.titleLabel.configure(text = "Game All Clear")
                        self.scoreTitleLabel = Label(self.main, font = "Helvetica 20", bg = 'light green', text = "Record")
                        self.scoreTitleLabel.pack()
                        self.scoreboard = Frame(self.main, bg = 'light green')
                        self.scoreboard.pack(pady = 3)
                        

                        sc = Score('score.txt')
                        self.slist = sc.getslist(self.username, self.totalScore)
                        self.sclistLabel = list()
                        if (self.username, self.totalScore) in self.slist :
                            for i in range(len(self.slist)) :
                                self.sclistLabel.append(Label(self.scoreboard))
                                self.sclistLabel[i].configure(font = "Times 11", text = "%02d : %10s\t%6s" % (i+1, self.slist[i][0], self.slist[i][1]),  bg = 'light green')
                                self.sclistLabel[i].pack()
                            for i in range(len(self.slist)) :
                                if self.username == self.slist[i][0] :
                                    self.sclistLabel[i].configure(font = "Times 11 bold", relief = RIDGE, borderwidth = 1)
                                    break
                        else :
                            for i in range(len(self.slist)) :
                                self.sclistLabel.append(Label(self.scoreboard))
                                self.sclistLabel[i].configure(font = "Times 11", text = "%02d : %10s\t%6s" % (i+1, self.slist[i][0], self.slist[i][1]),  bg = 'light green')
                                self.sclistLabel[i].pack()
                            self.outLabel = Label(self.scoreboard)
                            self.outLabel.configure(font = "Times 11 bold", text = "-- : %10s\t%6s" % (self.username, self.totalScore),  bg = 'light green', relief = RIDGE, borderwidth = 1)
                            self.outLabel.pack(pady = 5)
                            
                        self.closeBtn = Button(self.main, text = "finish", command = self.parent.destroy, background = 'green')
                        self.closeBtn.pack(pady = 4)
                                       
            self.select = True

    # block the card click event
    def donothing(self) :
        pass
    
    def changeValue(self) :
        self.blockClick = False

    #update the elapsed time    
    def update(self) :
        if self.run :
            self.etime = time.time() - self.start
            self.timeLabel.configure(bg = 'brown', fg = 'white', text = self.getFormatTime(self.etime))
            self.info.after(10, self.update)

    # change the time value to formatted time
    def getFormatTime(self, rawtime) :
        m = int(rawtime / 60)
        s = int(rawtime - m * 60.0)
        h = int((rawtime - m * 60.0 - s) * 100)
        return '%02d:%02d:%02d' % (m, s, h)
        

