import cast.analysers.ua
import cast.analysers.log
from cast.analysers import CustomObject , Bookmark
import tag_checker as TC

class MyExtension(cast.analysers.ua.Extension):

    def start_analysis(self):
        cast.analysers.log.debug('Hello World!!')

    def start_file(self,file):
        #cast.analysers.ua.Extension.start_file(self,file)
        filename = file.get_path()
        cast.analysers.log.debug(filename)
        dict = {}
        list_found_tag = []
        dict, list_found_tag = TC.cast_parser(filename)
        for i in list_found_tag:
            cast.analysers.log.debug(i+ " -> ")
            for j in dict[i]:
                cast.analysers.log.debug(j+" ")
        first_obj = CustomObject()
        #sample_bookmark
        bookmark = Bookmark(file,1,1,1,1)
        #cast.analysers.log.debug(str(bookmark.get_begin_line()))
        first_obj.set_name("partnerLinks")
        first_obj.set_fullname("bpel_partnerlinks")
        first_obj.set_type("BPEL partnerLinks")
        first_obj.set_parent(file)
        first_obj.save()
        first_obj.save_position(bookmark)
        #cast.analysers.log.debug(first_obj.bookmark)
        #cast.analysers.log.debug(filename)
        #TC.cast_parser(filename)
    def end_file(self,file):
        cast.analysers.log.debug('....')       
    def end_analysis(self):
        cast.analysers.log.debug('End..!!')  
if __name__ == '__main__':
    pass
    