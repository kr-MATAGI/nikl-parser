import json
import pickle
import os
import pandas as pd

'''
    @NOTE:
        JSON 종류별 key order
        1. 국립국어원 문법성 판단 말뭉치(버전 1.1)
            : target - sentence column
        
        2. 국립국어원 어휘 관계 자료 NIKLex(버전 1.0)
            : 내부 데이터가 문장이 아니기에 사용하지 않음
'''


class Ext_TSV_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Ext_TSV_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Ext_TSV_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store")  # mac
        print(f"[Ext_TSV_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Ext_TSV_Parser][__init__] {self.child_dir_list} !")

    def parse_tsv_ext_files(self):
        print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Called !")
        if not self.is_ok_status:
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.froot_dir_path + "/" + child_path for child_path in self.child_dir_list]

        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Ext_TSV_Parser][parse_tsv_ext_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            csv_file_list = [x for x in os.listdir(child_path) if ".tsv" in x]
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Target Dir Path : {child_path}")
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Json File Size: {len(csv_file_list)} !")

            for csv_file_idx, csv_file_name in enumerate(csv_file_list):
                print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Parse - {csv_file_idx}, {csv_file_name}")

                extracted_form_list = []
                tsv_file_path = child_path + "/" + csv_file_name

                tsv_df = pd.read_csv(tsv_file_path, sep="\t", encoding="utf-8")
                target_column = "sentence"
                if not target_column in tsv_df.keys():
                    raise KeyError
                for row_idx, item in tsv_df.iterrows():
                    discourse_item = item.get(target_column, None)
                    if None != discourse_item:
                        discourse_item = str(discourse_item).split(".")
                        discourse_item = [x + "." for x in discourse_item]
                        extracted_form_list.extend(discourse_item)
                print(f"[Ext_TSV_Parser][parse_tsv_ext_files] END - {csv_file_idx}, {csv_file_name}, "
                      f"size: {len(extracted_form_list)}")
                total_form_list.extend(extracted_form_list)
            # end, csv_file_list loop
            print(f"[Ext_TSV_Parser][parse_csv_ext_files] total_form_list.size : {len(total_form_list)}")

        # end, child_path_list loop
        print(f"[Ext_TSV_Parser][parse_csv_ext_files] All Complete - total_form_list.size : {len(total_form_list)}, "
              f"read_file_count: {read_file_count}")

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/ext_tsv.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Ext_TSV_Parser][parse_tsv_ext_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")

### MAIN ###
if "__main__" == __name__:
    print(f"[parse_tsv.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/ext_tsv"
    parser = Ext_TSV_Parser(root_dir_path)
    parser.parse_tsv_ext_files()