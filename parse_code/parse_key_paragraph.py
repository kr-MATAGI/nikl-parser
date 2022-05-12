import json
import pickle
import os

'''
    @NOTE:
        JSON 종류별 key order
        1. 국립국어원 감성 분석 말뭉치 2020(버전 1.0)
            : root - document - paragraph - paragraph_form
        
        2. 국립국어원 문어 말뭉치(버전 1.0)
            : root - document - paragraph - form
            
        3. 국립국어원 신문 말뭉치(버전 2.0)
            : root - document - paragraph - form
        
        4. 국립국어원 유사 문장 말뭉치(버전 1.0)
            : root - data - paraphrases - form
'''

class Paragraph_Key_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Paragraph_Key_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Paragraph_Key_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store") # mac
        print(f"[Paragraph_Key_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Paragraph_Key_Parser][__init__] {self.child_dir_list} !")

    def parse_key_paragraph_files(self):
        print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Called !")
        if not self.is_ok_status:
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path+"/"+child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            json_file_list = [x for x in os.listdir(child_path) if ".json" in x]
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Target Dir Path : {child_path}")
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Json File Size: {len(json_file_list)} !")

            for js_file_idx, json_file_name in enumerate(json_file_list):
                print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Parse - {js_file_idx}, {json_file_name}")

                extracted_form_list = []
                json_file_path = child_path + "/" + json_file_name
                with open(json_file_path, mode="r", encoding="utf-8") as target_file:
                    read_file_count += 1

                    target_json = json.load(target_file)
                    if "document" in target_json.keys():
                        print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Key: 'document' - {js_file_idx}, "
                              f"{json_file_name}")

                        doc_arr = target_json["document"]
                        for doc_obj in doc_arr:
                            paragraph_arr = doc_obj["paragraph"]

                            for paragraph_obj in paragraph_arr:
                                if "paragraph_form" in paragraph_obj.keys():
                                    extracted_form_list.append(paragraph_obj["paragraph_form"])
                                elif "form" in paragraph_obj.keys():
                                    extracted_form_list.append(paragraph_obj["form"])
                                else:
                                    print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] ERR - Check: form key")
                                    raise KeyError
                            # end, paragraph_arr loop

                    elif "data" in target_json.keys():
                        print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Key: 'data' - {js_file_idx}, "
                              f"{json_file_name}")

                        data_arr = target_json["data"]
                        for data_obj in data_arr:
                            paraphrases_arr = data_obj["paraphrases"]
                            for paraphrases_obj in paraphrases_arr:
                                extracted_form_list.append(paraphrases_obj["form"])
                    print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] END - {js_file_idx}, {json_file_name}, "
                          f"size: {len(extracted_form_list)}")
                total_form_list.extend(extracted_form_list)
            # end, json_file_list loop
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] total_form_list.size : {len(total_form_list)}")

        # end, child_path_list loop
        print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] All Complete - total_form_list.size : {len(total_form_list)}, "
              f"read_file_count: {read_file_count}")

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/key_paragraph.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Paragraph_Key_Parser][parse_key_paragraph_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")

### MAIN ###
if "__main__" == __name__:
    print(f"[parse_key_paragraph.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/key_paragraph"
    parser = Paragraph_Key_Parser(root_dir_path)
    parser.parse_key_paragraph_files()