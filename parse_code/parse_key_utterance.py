import json
import pickle
import os

'''
    @NOTE:
        JSON 종류별 key order
        1. 구국립국어원 구어 말뭉치(버전 1.2).pdf
            : root - document - utterance(arr) - form
        
        2. 국립국어원 일상 대화 말뭉치 2020(버전 1.2)
            : root - document - utterance(arr) - form
        
        3. 국립국어원 일상 대화 음성 말뭉치 2020(버전 1.2) part 1,2,3,4
            : root - document - utterance(arr) - form
'''

class Utterance_Key_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Utterance_Key_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Utterance_Key_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store") # mac
        print(f"[Utterance_Key_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Utterance_Key_Parser][__init__] {self.child_dir_list} !")

    def parse_key_utterance_files(self):
        print(f"[Utterance_Key_Parser][parse_key_utterance_files] Called !")
        if not self.is_ok_status:
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path+"/"+child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Utterance_Key_Parser][parse_key_utterance_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            json_file_list = [x for x in os.listdir(child_path) if ".json" in x]
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] Target Dir Path : {child_path}")
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] Json File Size: {len(json_file_list)} !")

            for js_file_idx, json_file_name in enumerate(json_file_list):
                print(f"[Utterance_Key_Parser][parse_key_utterance_files] Parse - {js_file_idx}, {json_file_name}")

                extracted_form_list = []
                json_file_path = child_path + "/" + json_file_name
                with open(json_file_path, mode="r", encoding="utf-8") as target_file:
                    read_file_count += 1
                    target_json = json.load(target_file)

                    doc_arr = target_json["document"]
                    for doc_obj in doc_arr:
                        utterance_arr = doc_obj["utterance"]

                        for sent_obj in utterance_arr:
                            extracted_form_list.append(sent_obj["form"])
                    # end, doc_arr loop
                print(f"[Utterance_Key_Parser][parse_key_utterance_files] END - {js_file_idx}, {json_file_name}, "
                      f"size: {len(extracted_form_list)}")
                total_form_list.extend(extracted_form_list)
            # end, json_file_list loop
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] total_form_list.size : {len(total_form_list)}")

        # end, child_path_list loop
        print(f"[Utterance_Key_Parser][parse_key_utterance_files] All Complete - "
              f"total_form_list.size : {len(total_form_list)}, "
              f"read_file_count: {read_file_count}")

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/key_utterance.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Utterance_Key_Parser][parse_key_utterance_files] Check Load -  {pkl_save_path}, "
                  f"size: {len(load_pkl_list)}")

### MAIN ###
if "__main__" == __name__:
    print(f"[parse_key_utterance.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/key_utterance"
    parser = Utterance_Key_Parser(root_dir_path)
    parser.parse_key_utterance_files()