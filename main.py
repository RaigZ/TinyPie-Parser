from tkinter import *
import re


class MyGUI:

    def __init__(self, root):
        self.master = root
        self.master.title("Lexical Analyzer TinyPie")       #title label
        self.master.geometry("1100x350")

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

        # big box for output parser
        self.bigtext_parser = Text(self.master, height=15, width=50)
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

        self.old_list = []
        self.Mytokens = []
        self.inToken #= ("empty", "empty")
        self.num = 0

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
            print("current list_before", self.list_tokens)
            self.list_tokens = self.CutOneLineTokens(self.list_line[0])      #ask about the string parameter
            print("current list", self.list_tokens)
            for x in self.list_tokens:
                self.bigtext_result.insert(END, x + '\n')
            #########################


            #list_line   [one_string, two_string etc
            ###connect to parser
            self.old_list = self.list_tokens

            for x in self.list_tokens:
                str_x = x
                strip = str_x.strip("<>")
                split_list = strip.split(",")
                if split_list[1] == '':
                    split_list[1] = '>'
                inToken_save = (split_list[0], split_list[1])
                self.Mytokens.append(inToken_save)
                #print("OOOOOOO", self.Mytokens)


            #self.inToken = ("empty", "empty")
            #self.Mytokens = self.list_tokens
            empty_one = ""
            empyt_two = ""
            self.num += 1
            self.bigtext_parser.insert(END, "####Parse tree for line %d###" % self.num,'\n')
            self.parser()
            self.bigtext_parser.insert(END, '\n')


            self.Mytokens.clear()
            ######################
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
            string = ""
            for x in result_key:
                if x != ' ':
                    string += x
            result_key = string
            print_presnt = False
            for x in result_key:
                if x == 'p':
                    print_presnt = True
            if result_key[0] == 'p' or print_presnt:
                result_id = result_key
                string = ""
                for x in result_id:
                    if x != ' ':
                        string += x
                result_id = string
                one_string = re.sub(r'^(\s+)?(if?n?t?)?(else)?(float)?(print)?(\s+)?', '', one_string)
                result_sp = re.match(r'^[():;"](\s+)?', one_string)
                result_sp = result_sp.group()
                string = ""
                for x in result_sp:
                    if x != ' ':
                        string += x
                result_sp = string
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_sp_two = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_two = result_sp_two.group()
                string = ""
                for x in result_sp_two:
                    if x != ' ':
                        string += x
                result_sp_two = string
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_string = re.match(r'^((\w+)(\s+)?)*', one_string)
                result_string = result_string.group()
                string = ""
                # for x in result_string:
                #    if x != ' ':
                #        string += x
                # result_string = string
                one_string = re.sub(r'^((\w+)(\s+)?)*', '', one_string)
                result_sp_three = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_three = result_sp_three.group()
                string = ""
                for x in result_sp_three:
                    if x != ' ':
                        string += x
                result_sp_three = string
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                result_sp_four = re.match(r'^[():;"](\s+)?', one_string)
                result_sp_four = result_sp_four.group()
                string = ""
                for x in result_sp_four:
                    if x != ' ':
                        string += x
                result_sp_four = string
                one_string = re.sub(r'^[():;"](\s+)?', '', one_string)

                result_sp_five = re.match(r'^[():;"](\s+)?', one_string)
                if result_sp_five is not None:
                    result_sp_five = result_sp_five.group()
                    string = ""
                    for x in result_sp_five:
                        if x != ' ':
                            string += x
                    result_sp_five = string
                    one_string = re.sub(r'^[():;"](\s+)?', '', one_string)

                list_.append("<id,%s>" % result_id)
                list_.append("<sp,%s>" % result_sp)
                list_.append("<sp,%s>" % result_sp_two)
                list_.append("<lit_str,%s>" % result_string)
                list_.append("<sp,%s>" % result_sp_three)
                list_.append("<sp,%s>" % result_sp_four)
                if result_sp_five is not None:
                    list_.append("<sp,%s>" % result_sp_five)
                return list_
            elif result_key[0] == 'i' and result_key[1] == 'n' and result_key[2] == 't':
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                result_id = result_id.group()
                string = ""
                for x in result_id:
                    if x != ' ':
                        string += x
                result_id = string
                one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                result_op = result_op.group()
                string = ""
                for x in result_op:
                    if x != " ":
                        string += x
                result_op = string
                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                result_int = re.match(r'^\d+', one_string)
                if result_int is not None:
                    result_int = result_int.group()
                    one_string = re.sub(r'^\d+', '', one_string)
                    result_sp = re.match(r'^[():;"](\s+)?', one_string)
                    if result_sp is not None:
                        result_sp = result_sp.group()
                        string = ""
                        for x in result_sp:
                            if x != ' ':
                                string += x
                        result_sp = string
                        one_string = re.sub(r'^[():;"](\s+)?', '', one_string)
                    list_.append("<keyword,%s>" % result_key)
                    list_.append("<id,%s>" % result_id)
                    list_.append("<op,%s>" % result_op)
                    list_.append("<lit_int,%s>" % result_int)
                    if result_sp is not None:
                        list_.append("<sp,%s>" % result_sp)
                    return list_
                else:
                    list_.append("<keyword,%s>" % result_key)
                    for i in one_string:
                        list_.append("<id,%s>" % result_id)
                        list_.append("<op,%s>" % result_op)
                        result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                        result_id = result_id.group()
                        string = ""
                        for x in result_id:
                            if x != ' ':
                                string += x
                        result_id = string
                        one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                        if one_string is not None:  # is not None
                            result_op = re.match(r'^[=+>*](\s+)?', one_string)
                            if result_op != None:
                                result_op = result_op.group()
                                string = ""
                                for x in result_op:
                                    if x != ' ':
                                        string += x
                                result_op = string
                                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                            else:
                                list_.append("<id,%s>" % result_id)
                                result_sp = re.match(r'^[():;"](\s+)?', one_string)
                                if result_sp is not None:
                                    result_sp = result_sp.group()
                                    string = ""
                                    for x in result_sp:
                                        if x != ' ':
                                            string += x
                                    result_sp = string
                                if result_sp is not None:
                                    list_.append("<sp,%s>" % result_sp)
                                return list_
            elif result_key[0] == 'f' and result_key[1] == 'l' and result_key[2] == 'o':
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                result_id = result_id.group()
                string = ""
                for x in result_id:
                    if x != ' ':
                        string += x
                result_id = string
                one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                result_op = result_op.group()
                string = ""
                for x in result_op:
                    if x != ' ':
                        string += x
                result_op = string
                one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                result_int = re.match(r'^\d+\.\d+$', one_string)

                if result_int is not None:
                    result_int = result_int.group()
                    string = ""
                    for x in result_int:
                        if x != ' ':
                            string += x
                    result_int = string
                    one_string = re.sub(r'^\d+\.\d+$', '', one_string)
                    list_.append("<keyword,%s>" % result_key)
                    list_.append("<id,%s>" % result_id)
                    list_.append("<op,%s>" % result_op)
                    list_.append("<lit_float,%s>" % result_int)
                    return list_
                else:
                    list_.append("<keyword,%s>" % result_key)
                    list_.append("<id,%s>" % result_id)
                    result_num = re.match(r'^(\d+\.\d+)?(\d+)?(\s+)?', one_string)  # checking if a num is next
                    result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)  # checking wether next is string
                    if result_num is not None:
                        result_num = result_num.group()
                    if result_id is not None:
                        result_id = result_id.group()
                        string = ""
                        for x in result_id:
                            if x != ' ':
                                string += x
                        result_id = string
                    if result_num != "":
                        #print("made float new")
                        for i in one_string:
                            list_.append("<op,%s>" % result_op)
                            result_float = re.match(r'^(\d+\.\d+)(\s+)?', one_string)
                            if result_float is not None:
                                result_float = result_float.group()
                                string = ""
                                for x in result_float:
                                    if x != ' ':
                                        string += x
                                result_float = string
                                one_string = re.sub(r'^(\d+\.\d+)(\s+)?', '', one_string)
                                list_.append("<lit_float,%s>" % result_float)
                            else:
                                result_int = re.match(r'^(\d+)(\s+)?', one_string)
                                if result_int is not None:
                                    result_int = result_int.group()
                                    string = ""
                                    for x in result_int:
                                        if x != ' ':
                                            string += x
                                    result_int = string
                                    one_string = re.sub(r'^(\d+)(\s+)?', '', one_string)
                                    list_.append("<lit_int,%s>" % result_int)
                            if i is not None:
                                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                                if result_op is not None:
                                    result_op = result_op.group()
                                    string = ""
                                    for x in result_op:
                                        if x != ' ':
                                            string += x
                                    result_op = string
                                    one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                                else:
                                    result_sp = re.match(r'^[():;"]$', one_string)
                                    if result_sp is not None:
                                        result_sp = result_sp.group()
                                        one_string = re.sub(r'^[():;"]$', '', one_string)
                                        list_.append("<sp,%s>" % result_sp)
                                        return list_
                        # return list_
                    elif result_id != "":
                        for i in one_string:
                            list_.append("<op,%s>" % result_op)
                            list_.append("<id,%s>" % result_id)
                            result_id = re.match(r'^([a-zA-Z]+(\d+)?)(\s+)?', one_string)
                            result_id = result_id.group()
                            string = ""
                            for x in result_id:
                                if x != ' ':
                                    string += x
                            result_id = string
                            one_string = re.sub(r'^([a-zA-Z]+(\d+)?)(\s+)?', '', one_string)
                            if one_string is not None:
                                result_op = re.match(r'^[=+>*](\s+)?', one_string)
                                if result_op != None:
                                    result_op = result_op.group()
                                    string = ""
                                    for x in result_op:
                                        if x != ' ':
                                            string += x
                                    result_op = string
                                    one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                                else:
                                    list_.append("<id,%s>" % result_id)
                                    return list_

            elif result_key[0] == 'i' and result_key[1] == 'f':
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_sp = re.match(r'^[():;"]', one_string)
                result_sp = result_sp.group()
                one_string = re.sub(r'^[():;"]', '', one_string)
                string = ""
                for x in result_key:
                    if x != ' ':
                        string += x
                list_.append("<keyword,%s>" % string)
                list_.append("<sp,%s>" % result_sp)
                for i in one_string:
                    result_id = re.match(r'^(([a-zA-Z]+(\d+)?)(\s+)?)', one_string)
                    if result_id is not None:
                        result_id = result_id.group()
                        string = ""
                        for x in result_id:
                            if x != " ":
                                string += x
                        one_string = re.sub(r'^(([a-zA-Z]+(\d+)?)(\s+)?)', '', one_string)
                        list_.append("<lit_str,%s>" % string)
                    result_op = re.match(r'^[=+>*](\s+)?', one_string)
                    if result_op is not None:
                        result_op = result_op.group()
                        string = ""
                        for x in result_op:
                            if x != " ":
                                string += x
                        one_string = re.sub(r'^[=+>*](\s+)?', '', one_string)
                        list_.append("<op,%s>" % string)

                    result_int = re.match(r'^\d+', one_string)
                    if result_int is not None:
                        result_int = result_int.group()
                        string = ""
                        for x in string:
                            if x != ' ':
                                string += x
                        one_string = re.sub(r'^\d+', '', one_string)
                        list_.append("<lit_int,%s>" % string)

                    result_sp = re.match(r'^[():;"]', one_string)
                    if result_sp is not None:
                        result_sp = result_sp.group()
                        one_string = re.sub(r'^[():;"]', '', one_string)
                        list_.append("<sp,%s>" % result_sp)
                        result_sp = re.match(r'^[():;"]$', one_string)
                        result_sp = result_sp.group()
                        one_string = re.sub(r'^[():;"]$', '', one_string)
                        list_.append("<sp,%s>" % result_sp)
                return list_

            elif result_key[0] == 'e' and result_key[1] == 'l' and result_key[2] == 's' and result_key[3] == 'e':
                one_string = re.sub(r'^(if?n?t?)?(else)?(float)?(\s+)?', '', one_string)
                result_sp = re.match(r'^[():;"]$', one_string)
                result_sp = result_sp.group()
                string = re.sub(r'^[():;"]$', '', one_string)
                list_.append("<keyword,%s>" % result_key)
                list_.append("<sp,%s>" % result_sp)
                return list_

# Mytokens=[("id","myvar"),("op","="),("int","5"),("op","+"),("int","6"),("op","+"),("float","2.3"),("sep",";")]
    inToken = ("empty", "empty")

# myvar=2*3*4*2.3;
# Mytokens = [("id","myvar"),("op","="),("int","2"),("op","*"),("int","3"),("op","*"),("int","4"),("op","*"), ("float","2.3"), ("sep",";")]

# float myVar =5*4.3+2.1;    or     float mynum= 3.4+7*2.1;
# Mytokens=[("id","myvar"),("op","="),("int","5"),("op","*"),("float","4.3"),("op","+"),("float","2.1"),("sep",";")]
# Mytokens=[("id","mynum"),("op","="),("float","3.4"),("op","+"),("int","7"),("op","*"),("float","2.1"),("sep",";")]

# myvar=2*3.3+4*5.5
#Mytokens=[("id","myvar"),("op","="),("int","2"),("op","*"),("float","3.3"),("op","+"),("int","4"),("op","*"),("float","5.5"),("sep",";")]

# myvar=2.4+5*6.1+3.5
    #Mytokens = [("keyword", "float"), ("id", "myvar"), ("op", "="), ("float", "2.4"), ("op", "+"), ("int", "5"), ("op", "*"), ("float", "6.1"), ("op", "+"), ("float", "3.5"), ("sep", ";")]


    def accept_token(self):
        global inToken
        print("     accept token from the list:" + inToken[1])
        string = "     accept token from the list:" + inToken[1]
        self.bigtext_parser.insert(END, string + '\n')
        inToken = self.Mytokens.pop(0)


    def math(self):
        print("\n----parent node math, finding children nodes:")
        string = "\n----parent node math, finding children nodes:"
        self.bigtext_parser.insert(END, string + '\n')
        global inToken
        if (inToken[0] == "lit_float"):
            print("child node (internal): float")
            string = "child node (internal): float"
            self.bigtext_parser.insert(END, string + '\n')
            print("   float has child node (token):" + inToken[1])
            string = "   float has child node (token):" + inToken[1]
            self.bigtext_parser.insert(END, string + '\n')
            self.accept_token()

            if (inToken[1] == "+"):
                print("child node (token):" + inToken[1])
                string = "child node (token):" + inToken[1]
                self.bigtext_parser.insert(END, string + '\n')
                self.accept_token()

                print("child node (internal): math")
                string = "child node (internal): math"
                self.bigtext_parser.insert(END, string + '\n')
                self.math()
            elif (inToken[1] == "*"):
                print("child node (token):" + inToken[1])
                string = "child node (token):" + inToken[1]
                self.bigtext_parser.insert(END, string + '\n')
                self.accept_token()

                print("child node (internal): math")
                string = "child node (internal): math"
                self.bigtext_parser.insert(END, string + '\n')
                self.math()
            else:
                print("error, you need + after the int in the math")
                string = "error, you need + after the int in the math"
                self.bigtext_parser.insert(END, string + '\n')

        elif (inToken[0] == "lit_int"):
            print("child node (internal): int")
            string = "child node (internal): int"
            self.bigtext_parser.insert(END, string + '\n')
            print("   int has child node (token):" + inToken[1])
            string ="    int has child node (token):" + inToken[1]
            self.bigtext_parser.insert(END, string + '\n')
            self.accept_token()

            if (inToken[1] == "+"):
                print("child node (token):" + inToken[1])
                string = "child node (token):" + inToken[1]
                self.bigtext_parser.insert(END, string + '\n')
                self.accept_token()

                print("child node (internal): math")
                string = "child node (internal): math"
                self.bigtext_parser.insert(END, string + '\n')
                self.math()
            elif (inToken[1] == "*"):
                print("child node (token):" + inToken[1])
                string = "child node (token):" + inToken[1]
                self.bigtext_parser.insert(END, string + '\n')
                self.accept_token()

                print("child node (internal): math")
                string = "child node (internal): math"
                self.bigtext_parser.insert(END, string + '\n')
                self.math()
            else:
                print("error, you need + after the int in the math")
                string = "error, you need + after the int in the math"
                self.bigtext_parser.insert(END, string + '\n')

        else:
            print("error, math expects float or int")
            string = "error, math expects float or int"
            self.bigtext_parser.insert(END, string + '\n')

    def exp(self):
        #print("\n---keyword node:")  #must be after paerant
        #global inToken;
        #typeK, token = inToken;
        #if (typeK == "keyword"):
        #    print("keyword node (root): keyword")
        #    print("   keyword has root node (token):" + token)
        #    accept_token()
        print("\n----parent node exp, finding children nodes:")
        string = "\n----parent node exp, finding children nodes:"
        self.bigtext_parser.insert(END, string + '\n')
        global inToken;
        typeK, token = inToken;
        if (typeK == "keyword"):
            print("keyword node (root): keyword")
            string = "keyword node (root): keyword"
            self.bigtext_parser.insert(END, string + '\n')
            print("   keyword has root node (token):" + token)
            string = "   keyword has root node (token):" + token
            self.bigtext_parser.insert(END, string + '\n')
            self.accept_token()
        else:
            print("expexted keyword as the first element of the expression!\n")
            string = "expexted keyword as the first element of the expression!\n"
            self.bigtext_parser.insert(END, string + '\n')
            return
        #global inToken;
        typeT, token = inToken;
        if (typeT == "id"):
            print("child node (internal): identifier")
            string = "child node (internal): identifier"
            self.bigtext_parser.insert(END, string + '\n')
            print("   identifier has child node (token):" + token)
            string = "   identifier has child node (token):" + token
            self.bigtext_parser.insert(END, string + '\n')
            self.accept_token()
        else:
            print("expect identifier as the second element of the expression!\n")
            string = "expect identifier as the second element of the expression!\n"
            self.bigtext_parser.insert(END, string + '\n')
            return

        if (inToken[1] == "="):
            print("child node (token):" + inToken[1])
            string = "child node (token):" + inToken[1]
            self.bigtext_parser.insert(END, string + '\n')
            self.accept_token()
        else:
            print("expect = as the second element of the expression!")
            string = "expect = as the second element of the expression!"
            self.bigtext_parser.insert(END, string + '\n')
            return

        print("Child node (internal): math")
        string = "Child node (internal): math"
        self.bigtext_parser.insert(END, string + '\n')
        self.math()


    def parser(self):
        global inToken
        inToken = self.Mytokens.pop(0)
        self.exp()
        if (inToken[1] == ";"):
            print("\nparse tree building success!")
            string = "\nparse tree building success!"
            self.bigtext_parser.insert(END, string + '\n')
        return


    #parser()

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyGUI(myTkRoot)
    myTkRoot.mainloop()


