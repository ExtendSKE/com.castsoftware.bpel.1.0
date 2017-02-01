import cast.analysers.ua
import cast.analysers.log
import tag_checker as TC

class MyExtension(cast.analysers.ua.Extension):

    def start_analysis(self):
        cast.analysers.log.debug('Hello World!!')

    def start_file(self,file):
        #cast.analysers.ua.Extension.start_file(self,file)
        filename = file.get_path()
        #cast.analysers.log.debug(filename)
        TC.cast_parser(filename)
        
        
if __name__ == '__main__':
    pass
    