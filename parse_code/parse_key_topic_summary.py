import json
import pickle
import os

'''
    @NOTE:
        JSON 종류별 key order
        1. 국립국어원 문서 요약 말뭉치(버전 1.0)
            : root - data(arr) - topic_sentences(arr)
'''

class Summary_Key_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Summary_Key_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Summary_Key_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store") # mac
        print(f"[Summary_Key_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Summary_Key_Parser][__init__] {self.child_dir_list} !")

    def parse_key_summary_files(self):
        print(f"[Summary_Key_Parser][parse_key_summary_files] Called !")
        if not self.is_ok_status:
            print(f"[Sent_Key_Parser][parse_key_summary_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path+"/"+child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Summary_Key_Parser][parse_key_summary_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            json_file_list = [x for x in os.listdir(child_path) if ".json" in x]
            print(f"[Summary_Key_Parser][parse_key_summary_files] Target Dir Path : {child_path}")
            print(f"[Summary_Key_Parser][parse_key_summary_files] Json File Size: {len(json_file_list)} !")

            for js_file_idx, json_file_name in enumerate(json_file_list):
                print(f"[Summary_Key_Parser][parse_key_summary_files] Parse - {js_file_idx}, {json_file_name}")

                extracted_form_list = []
                json_file_path = child_path + "/" + json_file_name
                with open(json_file_path, mode="r", encoding="utf-8") as target_file:
                    read_file_count += 1
                    target_json = json.load(target_file)

                    data_arr = target_json["data"]
                    for data_obj in data_arr:
                        topic_sent_arr = data_obj["topic_sentences"]

                        for topic_sent_obj in topic_sent_arr:
                            extracted_form_list.append(topic_sent_obj)
                print(f"[Summary_Key_Parser][parse_key_summary_files] END - {js_file_idx}, {json_file_name}, "
                      f"size: {len(extracted_form_list)}")
                total_form_list.extend(extracted_form_list)
            # end, json_file_list loop
            print(f"[Summary_Key_Parser][parse_key_summary_files] total_form_list.size : {len(total_form_list)}")

        # end, child_path_list loop
        print(f"[Summary_Key_Parser][parse_key_summary_files] All Complete - "
              f"total_form_list.size : {len(total_form_list)}, "
              f"read_file_count: {read_file_count}")

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/key_topic_summary.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Summary_Key_Parser][parse_key_sent_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Summary_Key_Parser][parse_key_sent_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")

### MAIN ###
if "__main__" == __name__:
    print(f"[parse_topic_summary.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/key_topic_summary"
    parser = Summary_Key_Parser(root_dir_path)
    parser.parse_key_summary_files()