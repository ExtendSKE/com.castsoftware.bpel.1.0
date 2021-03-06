import xml.etree.ElementTree as ET
import file_search as FS
import re
import cast.analysers.log
#import cast.analysers.log
def predefine_tags():
    #cast.analysers.log.debug(path+'')
    tags = ["receive","reply","variables","assign","invoke","partnerLinks"]
    return tags
def finding_tags(root,tags,list_found_tag):  #finding all tags which are present in source-code
    if root is None:
        return list_found_tag
    for i in root:
        #print(i.tag)
        for j in tags:
            index = i.tag.find(j)
            #print(index)
            if index!=-1:
                try:
                    index = list_found_tag.index(j)
                except ValueError:
                    index = -1
                #print(index)
                if index == -1:
                    list_found_tag.append(j)
        list_found_tag=finding_tags(i,tags,list_found_tag)
    return list_found_tag
def finding_tags_info(dict,data,list_found_tag,path):
    line_no = 0
    index1 = 0   #used for temporary storgae
    tmp_index =0
    for j in list_found_tag:
        tmp_list = []
        line_no =0
        #print(j)
        #tmp_list.append(path)
        for i in data:
            i=i[:-1]
            #print(i)
            if len(i)!=0:
                line_no = line_no +1
                index = i.find(j)
                if index!=-1:
                    if i.find('<'+j)!=-1:
                        if i.find('>')==-1:
                            #print(j)
                            try :
                                index1 = data.index(i+"\n")
                                tmp_index = index1
                            except ValueError:
                                index1 =-1
                            flag =0
                            while index1!=len(data):
                                if data[index1].find('>')!=-1:
                                    if data[index1].find('/>')!=-1:
                                        flag =1
                                    break
                                else:
                                    index1 = index1+1;
                            #print(index1)
                            if flag == 1:
                                tmp_list.append("begin_line:"+str(line_no)+",begin_column:"+str(index)+",end_line:"+str(line_no+index1-tmp_index)+",end_column:"+str(data[index1].find('>')))
                                #tmp_list.append(str(line_no)+" begin_column:"+str(index)+", end_line:"+str(line_no+index1-tmp_index)+" end_column:"+str(data[index1].find('>')))
                            else:
                                tmp_list.append("begin_line:"+str(line_no)+",begin_column:"+str(index))
                        else:
                            if(i.find('/>')!=-1):
                                tmp_list.append("begin_line:"+str(line_no)+",begin_column:"+str(index)+",end_line:"+str(line_no)+",end_column:"+str(i.find('>')))
                            else:
                                tmp_list.append("begin_line:"+str(line_no)+",begin_column:"+str(index))
                    else:
                        if i.find('</'+j+'>')!=-1:
                            tmp_list.append("end_line:"+str(line_no)+",end_column:"+str(index))
        dict[j]=tmp_list
    return dict
def find_tag_properties(root,tag_name,list_data):
    if root is None:
        return list_data
    for i in root:
        index1 = str(i.tag)
        index1 =re.sub('{.*?}', '', index1)
        if tag_name == index1:
            data =str(i.attrib)
            data = re.sub('{','',data)
            data = re.sub('}','',data)
            #print(i.attrib)
            if len(data)!=0:
                data = re.sub('[\s+]','',data)
                data= re.sub("'","",data)
                list_data.append(data)
        list_data = find_tag_properties(i,tag_name,list_data)
    return list_data
def cast_parser(filename):
    #cast.analysers.log.debug(path+'\n'+filename)
    tags = predefine_tags()
    list_found_tag = []
    tree = ET.parse(filename)
    root = tree.getroot()
    #cast.analysers.log.debug(str(root))
    list_found_tag=finding_tags(root,tags,list_found_tag)
    dict_tag = {}
    for i in list_found_tag:
        list_data = []
        if i=="partnerLinks":
            dict_tag[i] = find_tag_properties(root,"partnerLink",list_data)
        elif i=="variables":
            dict_tag[i] = find_tag_properties(root,"variable",list_data)
        else:
            dict_tag[i] = find_tag_properties(root,i,list_data)
    #for i in list_found_tag:
    #    cast.analysers.log.debug(i)
    source_code_file = open(filename,'r')
    data = []
    for j in source_code_file:
        data.append(j)
    source_code_file.close()
    dict= {}
    dict=finding_tags_info(dict,data,list_found_tag,filename)
    filename = filename.replace('.bpel','.txt')
    indexx = filename.rfind('\\')
    filename = filename[:indexx]+'/'+filename[indexx+1:]
    return dict_tag,dict,list_found_tag
    '''
    for i in list_found_tag:
        cast.analysers.log.debug(i+ " -> ")
        for j in dict[i]:
            cast.analysers.log.debug(j+" ")
    #cast.analysers.log.debug(filename)

    dict_out=open(filename.replace('.bpel','.txt'),'w')
    for i in list_found_tag:
        dict_out.write(i+": "+str(dict[i])+"\n")
    dict_out.close()
    '''
if __name__ == "__main__":
    #tags = tag_finder()
    cast_parser("C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.bpel.1.0\\tests\BPEL_Sample\Oracle_Samples\TravelProcess\Travel.bpel")
    '''
    tags=predefine_tags()
    path = os.getcwd()
    file_list = FS.directory_search(path,'*.bpel')
    for i in file_list:
        list_found_tag = []
        tree=ET.parse(i[0])
        root =tree.getroot()
        list_found_tag=finding_tags(root,tags,list_found_tag)
        #print(list_found_tag)
        source_code_file = open(i[0],'r') ##Reading SOurce-code Finding Starting & ending Line no. and column no.
        data = []
        for j in source_code_file:
            data.append(j)
        source_code_file.close()
        dict= {}
        dict=finding_tags_info(dict,data,list_found_tag,i[0])
        dict_out=open(i[0].replace('.bpel','.txt'),'w')     ##Writing dictionary in output file
        #dict_out.write("File_Path : "+i[0]+"\n")  #path of file
        for i in list_found_tag:
            dict_out.write(i+": "+str(dict[i])+"\n")
        dict_out.close()
    #print(found_tags)
    '''
