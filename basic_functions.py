#import cast.analysers.log as console
class Basic():
    def __init__(self):
        self.line_of_code = 0
        self.line_of_comments = 0
        self.no_of_blank_lines = 0
        self.flag = 0
    def cal_loc(self):
        source_file = open("--Enter File Path--",'r')
        for i  in source_file:
            if self.flag == 1:
                if i.find('-->')==-1:
                    self.line_of_comments = self.line_of_comments + 1
                else:
                    self.line_of_comments = self.line_of_comments + 1
                    self.flag = 0
            else:
                #print(len(i))
                if len(i) == 1:
                    self.no_of_blank_lines =self.no_of_blank_lines + 1
                elif i.find('<!--')!=-1:
                    self.line_of_comments = self.line_of_comments + 1
                    self.flag = 1
                else:
                    self.line_of_code = self.line_of_code +1
        #print(str(self.line_of_comments))

if __name__ == "__main__":
    test= Basic()
    test.cal_loc()
