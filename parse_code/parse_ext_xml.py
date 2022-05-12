import pickle
import os
import xml.etree.ElementTree as ET

'''
    @NOTE:
        XML 종류별 key order
        1. 국립국어원 비출판물 말뭉치(버전 1.1)
            - sjml 확장자이지만 xml 형식
            : <SJML> - <text> - <p>
        
        2. 국립국어원 의미역 기술 모형(버전 1.0)
            : <frameFile> - <frameset> - <frame> - <example> - <text>
'''

class Ext_XML_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Ext_XML_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Ext_XML_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store") # mac
        print(f"[Ext_XML_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Ext_XML_Parser][__init__] {self.child_dir_list} !")

    def parse_ext_sjml_files(self):
        print(f"[Ext_XML_Parser][parse_ext_sjml_files] Called !")
        if not self.is_ok_status:
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path+"/"+child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Ext_XML_Parser][parse_ext_sjml_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            tsv_file_list = [x for x in os.listdir(child_path) if ".sjml" in x]
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] Target Dir Path : {child_path}")
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] Json File Size: {len(tsv_file_list)} !")

            for sjml_file_idx, sjml_file_name in enumerate(tsv_file_list):
                print(f"[Ext_XML_Parser][parse_ext_sjml_files] Parse - {sjml_file_idx}, {sjml_file_name}")

                extracted_form_list = []
                sjml_file_path = child_path + "/" + sjml_file_name
                try:
                    tree = ET.parse(sjml_file_path)
                except Exception as err:
                    print(f"[Ext_XML_Parser][parse_ext_sjml_files] ERR - {sjml_file_path}, maybe included &")
                root = tree.getroot()
                all_text_tag = root.find("text")
                all_p_tag = all_text_tag.findall("p")
                for p_item in all_p_tag:
                    extracted_form_list.append(p_item.text)
                total_form_list.extend(extracted_form_list)
                print(f"[Ext_XML_Parser][parse_ext_sjml_files] END - {sjml_file_idx}, {sjml_file_name}, "
                      f"size: {len(extracted_form_list)}")
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] total_form_list.size : {len(total_form_list)}")
        # end, child_path_list loop

        # save
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/ext_sjml.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")

    def parse_ext_xml_files(self):
        print(f"[Ext_XML_Parser][parse_ext_xml_files] Called !")
        if not self.is_ok_status:
            print(f"[Ext_XML_Parser][parse_ext_xml_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path+"/"+child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Ext_XML_Parser][parse_ext_xml_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            xml_file_list = [x for x in os.listdir(child_path) if ".xml" in x]
            print(f"[Ext_XML_Parser][parse_ext_xml_files] Target Dir Path : {child_path}")
            print(f"[Ext_XML_Parser][parse_ext_xml_files] XML File Size: {len(xml_file_list)} !")

            for xml_file_idx, xml_file_name in enumerate(xml_file_list):
                extracted_form_list = []
                sjml_file_path = child_path + "/" + xml_file_name

                try:
                    tree = ET.parse(sjml_file_path)
                except Exception as err:
                    print(f"[Ext_XML_Parser][parse_ext_xml_files] ERR - {sjml_file_path}, Plz check file !")
                root = tree.getroot()
                all_example_tag = root.find("predicate").find("frameset").find("frame").find("example")
                all_text_tag = all_example_tag.findall("text")
                for text_item in all_text_tag:
                    extracted_form_list.append(text_item.text)
                total_form_list.extend(extracted_form_list)
                print(f"[Ext_XML_Parser][parse_ext_sjml_files] END - {xml_file_idx}, {xml_file_name}, "
                      f"size: {len(extracted_form_list)}")
            print(f"[Ext_XML_Parser][parse_ext_sjml_files] total_form_list.size : {len(total_form_list)}")
        # end, child_path_list loop

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/ext_xml.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")

### MAIN ###
if "__main__" == __name__:
    print(f"[parse_key_sent.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/ext_xml"
    parser = Ext_XML_Parser(root_dir_path)
    # parser.parse_ext_sjml_files()
    parser.parse_ext_xml_files()