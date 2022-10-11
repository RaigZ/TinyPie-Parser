from tkinter import *
import re


class MyGUI:

    def __init__(self, root):
        self.master = root
        self.master.title("Lexical Analyzer TinyPie")       #title label
        self.master.geometry("975x350")

        #two labels for the two boxes
        self.label_input = Label(self.master, text="Source Code Input:\t\t\t")
        self.label_input.grid(row=0, column=0, sticky=E)
        self.label_result = Label(self.master, text="Lexical Anayzled Result:")
        self.label_result.grid(row=0, column=1, sticky=W)

        self.label_parser = Label(self.master, text="Parse Tree:")
        self.label_parser.grid(row=0, column=2, sticky=W)

        #big box getting big input
        self.bigtext_input = Text(self.master, height=15, width=40)
        self.bigtext_input.grid(row=1, column=0, sticky=W)

        #big box getting output
        self.bigtext_result = Text(self.master, height=15, width=40)
        self.bigtext_result.grid(row=1, column=1, sticky=E)

        #big box for output parser
        self.bigtext_parser = Text(self.master, height=15, width=40)
        self.bigtext_parser.grid(row=1, column=2, sticky=E)

        #label for current processing lines
        self.current_num = Label(self.master, text="Current Processing Line: ")
        self.current_num.grid(row=2, column=0, sticky=W)
        self.current_num_counter = Entry(self.master, width=10)     #used entry for current line number
        self.current_num_counter.grid(row=2, column=0, sticky=E)

        #two buttons for next line and quit
        self.nextlinebutton = Button(self.master, text="Next Line", command=self.submitt_nextline)
        self.nextlinebutton.grid(row=3, column=0, sticky=E)
        self.quitlinebutton = Button(self.master, text="Quit", command=self.submitt_quit)
        self.quitlinebutton.grid(row=3, column= 2, sticky=E)

        self.list_line = []         #saving all input string into list
        self.list_gone = False
        self.num_counter = 0
        self.list_tokens = []


    #text is copy/pasted and shown in the output box. Current processing line add 1 and shows 1
    def submitt_nextline(self):   #adding 1 to every new line
        #get every line if list empty
        if len(self.list_line) == 0 and self.list_gone == False:
            whole_text = self.bigtext_input.get("1.0", END)
            str_line = ""
            i = 0
            while i < len(whole_text):
                if whole_text[i] != '\n':
                    str_line += whole_text[i]
                elif whole_text[i] == '\n':
                    #print(str_line)
                    self.list_line.append(str_line)
                    str_line = ""
                i += 1
            #print(self.list_line, "list")
        else:
            print("List not empty")      #used to check list
        if len(self.list_line) != 0:
            #*********Going to insert/combine lexer here***************
            #want to use function CutOneLineTokens to return the string into a list of tokens to display by index
            self.list_tokens = self.CutOneLineTokens(self.list_line[0])      #ask about the string parameter
            for x in self.list_tokens:
                self.bigtext_result.insert(END, x + '\n')
            self.list_tokens.clear()
            self.bigtext_result.insert(END, '\n')
            self.current_num_counter.delete(0, END)
            self.num_counter += 1
            self.current_num_counter.insert(0, str(self.num_counter))        #counter # of current process line
            del self.list_line[0]
            #print(self.list_line)
            if len(self.list_line) == 0:
                self.list_gone = True


    def submitt_quit(self):         #simply ending the program
        self.master.destroy()
        self.master.quit()
        print("program exited")

    def CutOneLineTokens(self, one_string):
        list_ = []
        print("testing string input %s" % one_string)
        for x in one_string:
            result_key = re.match(r'^(\s+)?(if?n?t?)?(else)?(float)?(print)?(\s+)?', one_string)
            result_key = result_key.group()
            # print(result_key)
            print_presnt = False
            for x in result_key:
                if x == 'p':
                    print_presnt = True
            if result_key[0] == 'p' or print_presnt:
                # print("made print")
                result_id = result_key
                one_string = re.sub(r'^(\s+)?(if?n?t?)?(else)?(float)?(print)?(\s+)?', '', one_string)
                result_sp = re.match(r'^[():;"](\s+)?', one_string)
                result_sp = result_sp.group()
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_sp_two = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_two = result_sp_two.group()
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_string = re.match(r'^((\w+)(\s+)?)*', one_string)
                result_string = result_string.group()
                one_string = re.sub(r'^((\w+)(\s+)?)*', '', one_string)
                result_sp_three = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_three = result_sp_three.group()
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_sp_four = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_four = result_sp_four.group()
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                list_.append("<identifier,%s>" % result_id)
                list_.append("<separator,%s>" % result_sp)
                list_.append("<separator,%s>" % result_sp_two)
                list_.append("<lit_str,%s>" % result_string)
                list_.append("<separator,%s>" % result_sp_three)
                list_.append("<separator,%s>" % result_sp_four)
                return list_
            elif result_key[0] == 'i' and result_key[1] == 'n' and result_key[2] == 't':
                # print("made int")
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                result_id = result_id.group()
                one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                result_op = result_op.group()
                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                result_int = re.match(r'^\d+$', one_string)
                #result_int = result_int.group()
                if result_int is not None:
                    result_int = result_int.group()
                    one_string = re.sub(r'^\d+$', '', one_string)
                    list_.append("<keyword,%s>" % result_key)
                    list_.append("<identifier,%s>" % result_id)
                    list_.append("<operator,%s>" % result_op)
                    list_.append("<lit_int,%s>" % result_int)
                    return list_
                else:
                    list_.append("<keyword,%s>" % result_key)
                    for i in one_string:
                        list_.append("<identifier,%s>" % result_id)
                        list_.append("<operator,%s>" % result_op)
                        result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                        result_id = result_id.group()
                        one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                        if one_string is not None:  # is not None
                            result_op = re.match(r'^[=+>*](\s+)?', one_string)
                            if result_op != None:
                                result_op = result_op.group()
                                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                            else:
                                list_.append("<identifier,%s>" % result_id)
                                # print(list_, "finsh")
                                return list_
            elif result_key[0] == 'f' and result_key[1] == 'l' and result_key[2] == 'o':
                # print("made float")
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                result_id = result_id.group()
                one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                result_op = result_op.group()
                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                result_int = re.match(r'^\d+\.\d+$', one_string)
                # result_int = result_int.group()
                if result_int is not None:
                    # print("made float num")
                    result_int = result_int.group()
                    one_string = re.sub(r'^\d+\.\d+$', '', one_string)
                    list_.append("<keyword,%s>" % result_key)
                    list_.append("<identifier,%s>" % result_id)
                    list_.append("<operator,%s>" % result_op)
                    list_.append("<lit_float,%s>" % result_int)
                    return list_
                else:
                    list_.append("<keyword,%s>" % result_key)
                    for i in one_string:
                        # print("made float strings", one_string)
                        list_.append("<identifier,%s>" % result_id)
                        list_.append("<operator,%s>" % result_op)
                        # print(list_)
                        result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                        result_id = result_id.group()
                        one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                        if one_string is not None:  # is not None
                            result_op = re.match(r'^[=+>*](\s+)?', one_string)
                            if result_op != None:
                                result_op = result_op.group()
                                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                            else:
                                list_.append("<identifier,%s>" % result_id)
                                # print(list_, "finsh")
                                return list_
            elif result_key[0] == 'i' and result_key[1] == 'f':
                # print("made if")
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                # print(one_string)
                result_sp = re.match(r'^[():;"]', one_string)
                result_sp = result_sp.group()
                one_string = re.sub(r'^[():;"]', '', one_string)
                # print(one_string)
                result_id = re.match(r'^(([a-zA-Z]+(\d+)?)(\s+)?)', one_string)
                result_id = result_id.group()
                one_string = re.sub(r'^(([a-zA-Z]+(\d+)?)(\s+)?)', '', one_string)

                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                result_op = result_op.group()
                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)

                result_int = re.match(r'^\d+', one_string)
                result_int = result_int.group()
                one_string = re.sub(r'^\d+', '', one_string)

                result_sp_end_one = re.match(r'^[():;]', one_string)
                result_sp_end_one = result_sp_end_one.group()
                one_string = re.sub(r'^[():;]', '', one_string)

                result_sp_end_two = re.match(r'^[():;"]$', one_string)
                result_sp_end_two = result_sp_end_two.group()
                one_string = re.sub(r'^[():;"]$', '', one_string)

                list_.append("<keyword,%s>" % result_key)
                list_.append("<separator,%s>" % result_sp)
                list_.append("<identifier,%s>" % result_id)
                list_.append("<operator,%s>" % result_op)
                list_.append("<lit_int,%s>" % result_int)
                list_.append("<operator,%s>" % result_sp_end_one)
                list_.append("<operator,%s>" % result_sp_end_two)
                return list_
            elif result_key[0] == 'e' and result_key[1] == 'l' and result_key[2] == 's' and result_key[3] == 'e':
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_sp = re.match(r'^[():;"]$', one_string)
                result_sp = result_sp.group()
                string = re.sub(r'^[():;"]$', '', one_string)
                list_.append("<keyword,%s>" % result_key)
                list_.append("<separator,%s>" % result_sp)
                return list_


if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyGUI(myTkRoot)
    myTkRoot.mainloop()




