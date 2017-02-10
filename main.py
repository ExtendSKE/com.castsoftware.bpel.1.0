import cast.analysers.ua
import cast.analysers.log
import os
from cast.analysers import CustomObject , Bookmark,create_link
import tag_checker as TC
obj_ref_invoke = {}
obj_ref_receive = {}
obj_data_patnerlink ={}
obj_bookmark = {}
class MyExtension(cast.analysers.ua.Extension):
    def __init__ (self):
        self.dict = {}
        self.tag_data = {}
        self.list_tag_data = []
        self.list_data = []
        self.list_found_tag = []
        self.list_bookmark = []
        self.begin_line = ""
        self.begin_column = ""
        self.end_line = ""
        self.end_column = ""
        self.bookmark_index = -1
        self.count_tag = 0
        self.flag = 0
    def start_analysis(self):
        cast.analysers.log.debug('H')
        #cast.analysers.log.debug(os.getcwd())
    def start_file(self,file):
        #cast.analysers.ua.Extension.start_file(self,file)
        filename = file.get_path()
        cast.analysers.log.debug(filename)
        self.tag_data,self.dict, self.list_found_tag = TC.cast_parser(filename)
        for i in self.list_found_tag:
            cast.analysers.log.debug(i+ " -> ")
            self.list_bookmark = []
            for j in self.dict[i]:
                #cast.analysers.log.debug(j)
                self.list_bookmark.extend(j.split(','))
            self.count_tag = 0
            #del tmp_list.index[tmp_list.index()]
            while len(self.list_bookmark)!=0:
                self.begin_line = ""
                self.begin_column = ""
                self.end_line = ""
                self.end_column = ""
                for k in self.list_bookmark:
                    if k.find("begin_line")!=-1:
                        self.bookmark_index = k.find(':')
                        self.begin_line = k[self.bookmark_index+1:]
                        del self.list_bookmark[self.list_bookmark.index(k)]
                        break
                for k in self.list_bookmark:
                    if k.find("begin_column")!=-1:
                        self.bookmark_index = k.find(':')
                        self.begin_column = k[self.bookmark_index+1:]
                        del self.list_bookmark[self.list_bookmark.index(k)]
                        break
                for k in self.list_bookmark:
                    if k.find("end_line")!=-1:
                        self.bookmark_index = k.find(':')
                        self.end_line = k[self.bookmark_index+1:]
                        del self.list_bookmark[self.list_bookmark.index(k)]
                        break
                for k in self.list_bookmark:
                    if k.find("end_column")!=-1:
                        self.bookmark_index = k.find(':')
                        self.end_column = k[self.bookmark_index+1:]
                        del self.list_bookmark[self.list_bookmark.index(k)]
                        break
                self.count_tag =self.count_tag+1
                if i =="partnerLinks" or i =="invoke" or i=="receive":
                    #cast.analysers.log.debug(self.begin_line)
                    tag_obj = CustomObject()
                    bookmark = Bookmark(file,int(self.begin_line),int(self.begin_column),int(self.end_line),int(self.end_column))
                    tag_obj.set_name(i)
                    #cast.analysers.log.debug(str(self.tag_data[i]))
                    for val in self.tag_data[i]:
                        self.flag = 0
                        self.list_data = val.split(',')
                        for val_1 in self.list_data:
                            if i != "partnerLinks" and val_1.find("partnerLink") !=-1:
                                tag_obj.set_name(val_1[val_1.find(':')+1:])
                                self.flag = 1
                                break
                        if self.flag == 1:
                            if i=="invoke":
                                obj_ref_invoke[tag_obj] = val
                            else:
                                obj_ref_receive[tag_obj] = val
                            obj_bookmark[tag_obj] = bookmark
                            del self.tag_data[i][self.tag_data[i].index(val)]
                            break
                    if i =="partnerLinks":
                        obj_data_patnerlink[file] = self.tag_data[i]
                        #cast.analysers.log.debug(str(self.tag_data[i]))
                    tag_obj.set_fullname(filename+"bpel_"+i+str(self.count_tag))
                    tag_obj.set_type("BPEL_"+i)
                    tag_obj.set_parent(file)
                    tag_obj.set_guid(filename+"bpel_"+i+str(self.count_tag))
                    tag_obj.save()
                    tag_obj.save_position(bookmark)
                    tag_obj.save_property("BPEL_Sample.processWidth",5)
                    tag_obj.save_violation("BPEL_Sample.processWidth", bookmark, additional_bookmarks=None)
        '''
        cast.analysers.log.debug(str(len(tmp_list)))
        cast.analysers.log.debug(str_val)
        cast.analysers.log.debug(str_val_1)
        cast.analysers.log.debug(str_val_2)
        cast.analysers.log.debug(str_val_3)
        first_obj = CustomObject()
        second_obj = CustomObject()
        third_obj = CustomObject()
        #sample_bookmark
        bookmark = Bookmark(file,1,1,1,1)
        bookmark_1 = Bookmark(file,2,2,2,2)

        #cast.analysers.log.debug(str(bookmark.get_begin_line()))
        first_obj.set_name("partnerLinks")
        first_obj.set_fullname(filename+"bpel_partnerlinks")
        first_obj.set_type("BPEL partnerLinks")
        first_obj.set_parent(file)
        first_obj.set_guid(filename+"bpel_partnerlinks")
        first_obj.save()
        first_obj.save_position(bookmark)
        second_obj.set_name("invoke")
        second_obj.set_fullname(filename+"bpel_invoke")
        second_obj.set_type("BPEL_invoke")
        second_obj.set_parent(file)
        second_obj.set_guid(filename+"bpel_invoke")
        second_obj.save()
        second_obj.save_position(bookmark_1)
        third_obj.set_name("recieve")
        third_obj.set_fullname(filename+"bpel_recieve")
        third_obj.set_type("BPEL_recieve")
        third_obj.set_parent(file)
        third_obj.set_guid(filename+"bpel_recieve")
        third_obj.save()
        third_obj.save_position(bookmark_1)
        create_link('callLink',file,second_obj,bookmark_1)
        #Error
        #cast.analysers.log.debug(second_obj._bookmark)
        # it doesn't
        # cast.analysers.log.debug(first_obj.get_positions())
        #first_obj.save_property("BPEL_Sample.processWidth",5)
        #cast.analysers.log.debug(Object.get_name(self))
        #cast.analysers.log.debug(filename)
        #TC.cast_parser(filename)
        '''
    def end_file(self,file):
        pass
    def end_analysis(self):
        #cast.analysers.log.debug(str(len(obj_bookmark)))
        count = 0
        for i in obj_ref_invoke:
            tmp_list = []
            tmp_list = obj_ref_invoke[i].split(',')
            op_type = ""
            port_type = ""
            partner_link_type = ""
            partner_link_name = ""
            for j in tmp_list:
                if j.find('operation')!=-1:
                    op_type = j[j.find(':')+1:]
                    break;
            for j in tmp_list:
                if j.find('portType')!=-1:
                    port_type = j[j.find(':')+1:]
                    break;
            for j in tmp_list:
                if j.find('partnerLink')!=-1:
                    partner_link_name = j[j.find(':')+1:]
                    break;
            for j in obj_ref_receive:
                tmp_list_1 = []
                op_type_1 = ""
                port_type_1 = ""
                tmp_list_1 = obj_ref_receive[j].split(',')
                for k in tmp_list_1:
                    if k.find('operation')!=-1:
                        op_type_1 = k[k.find(':')+1:]
                        break;
                for k in tmp_list:
                    if k.find('portType')!=-1:
                        port_type_1 = k[k.find(':')+1:]
                        break;
                if op_type == op_type_1 and port_type == port_type_1:
                    #cast.analysers.log.debug(str(obj_ref_invoke[i]))
                    flag =0
                    filename =i.parent.get_path()
                    for child in obj_data_patnerlink[i.parent]:
                        #cast.analysers.log.debug(child)
                        if child.find('name:'+partner_link_name)!=-1:
                            tmp_list_2 = []
                            tmp_list_2 = child.split(',')
                            for child_1 in tmp_list_2:
                                if child_1.find('partnerLinkType')!=-1:
                                    partner_link_type = child_1[child_1.find(':')+1:]
                                    flag = 1
                                    break;
                            if flag == 1:
                                break;
                    count = count+1
                    tag_obj = CustomObject()
                    tag_obj.set_name(partner_link_name)
                    tag_obj.set_parent(i.parent)
                    tag_obj.set_fullname(filename+'bpel_'+partner_link_name+str(count))
                    tag_obj.set_type('BPEL_Partnerlink_Name')
                    tag_obj.set_guid(filename+'bpel_'+partner_link_name+str(count))
                    tag_obj.save()
                    create_link('callLink',i,tag_obj,obj_bookmark[i])
                    tag_obj_1 = CustomObject()
                    tag_obj_1.set_name(partner_link_type)
                    tag_obj_1.set_parent(i.parent)
                    tag_obj_1.set_fullname(filename+'bpel_'+partner_link_type+str(count))
                    tag_obj_1.set_type('BPEL_Partnerlink_Type')
                    tag_obj_1.set_guid(filename+'bpel_'+partner_link_type+str(count))
                    tag_obj_1.save()
                    create_link('callLink',tag_obj,tag_obj_1,obj_bookmark[i])
                    tag_obj_2 = CustomObject()
                    tag_obj_2.set_name(port_type)
                    tag_obj_2.set_parent(i.parent)
                    tag_obj_2.set_fullname(filename+'bpel_'+port_type+str(count))
                    tag_obj_2.set_type('BPEL_Port')
                    tag_obj_2.set_guid(filename+'bpel_'+port_type+str(count))
                    tag_obj_2.save()
                    create_link('callLink',tag_obj_1,tag_obj_2,obj_bookmark[i])
                    tag_obj_3 = CustomObject()
                    tag_obj_3.set_name(op_type)
                    tag_obj_3.set_parent(i.parent)
                    tag_obj_3.set_fullname(filename+'bpel_'+op_type+str(count))
                    tag_obj_3.set_type('BPEL_Operation')
                    tag_obj_3.set_guid(filename+'bpel_'+op_type+str(count))
                    tag_obj_3.save()
                    create_link('callLink',tag_obj_2,tag_obj_3,obj_bookmark[i])
                    create_link('callLink',tag_obj_3,j,obj_bookmark[i])

            #cast.analysers.log.debug(list_obj_ref[i])
    #    cast.analysers.log.debug(str(list_obj_ref[0].name))
    #    cast.analysers.log.debug(str(list_obj_ref[len(list_obj_ref)-2].name))
    #    create_link('callLink',list_obj_ref[0],list_obj_ref[len(list_obj_ref)-2],list_obj_ref[len(list_obj_ref)-1])
        pass
if __name__ == '__main__':
    pass
