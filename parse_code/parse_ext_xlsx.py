import pickle
import os
import pandas as pd

'''
    @NOTE:
        1. 국립국어원 서울말 낭독체 발화 말뭉치(버전 2.0)
            - 5.최초 대본.hwp 라는 한글 파일도 있지만 2.수정 대본을 사용한다. (어차피 xlsx 파일에 다 있음)
            - target column : 수정 대본
'''


class Ext_Xlsx_Parser:
    def __init__(self, root_dir_path: str):
        print(f"[Ext_Xlsx_Parser][__init__] INIT !")
        self.is_ok_status = True
        self.root_dir_path = root_dir_path
        if not os.path.exists(self.root_dir_path):
            print(f"[Ext_Xlsx_Parser][__init__] ERR - Not Exist: {self.root_dir_path} !")
            self.is_ok_status = False
            return
        self.child_dir_list = os.listdir(self.root_dir_path)
        self.child_dir_list.remove(".DS_Store")  # mac
        print(f"[Ext_Xlsx_Parser][__init__] child_dir_list.size: {len(self.child_dir_list)} !")
        print(f"[Ext_Xlsx_Parser][__init__] {self.child_dir_list} !")

    def parse_ext_xlsx_files(self):
        print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Called !")
        if not self.is_ok_status:
            print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] ERR - is_ok_status: {self.is_ok_status} !")
            return

        total_form_list = []
        read_file_count = 0
        child_path_list = [self.root_dir_path + "/" + child_path for child_path in self.child_dir_list]
        for child_path in child_path_list:
            if not os.path.exists(child_path):
                print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] ERR - Not Exist: {child_path} !")
                self.is_ok_status = False
                return

            xlsx_file_list = [x for x in os.listdir(child_path) if ".xlsx" in x]
            print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Target Dir Path : {child_path}")
            print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Json File Size: {len(xlsx_file_list)} !")

            for xlsx_file_idx, xlsx_file_name in enumerate(xlsx_file_list):
                read_file_count += 1
                print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Parse - {xlsx_file_idx}, {xlsx_file_name}")

                extracted_form_list = []
                xlsx_file_path = child_path + "/" + xlsx_file_name

                target_column = "수정 대본"
                xlsx_df = pd.read_excel(xlsx_file_path, sheet_name="음성 파일별 수정 대본")
                for idx, xlsx_item in xlsx_df.iterrows():
                    target_item = xlsx_item.get(target_column, None)
                    if target_item != None:
                        extracted_form_list.append(target_item)
                print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] End - size: {len(extracted_form_list)}")
                total_form_list.extend(extracted_form_list)
            # end, xlsx_file_list loop
        # end, child_path_list loop

        print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Complete - size: {len(total_form_list)}")

        # save pickle file
        pkl_save_path = "../corpus/모두의 말뭉치/result/only_text/ext_xlsx.pkl"
        with open(pkl_save_path, mode="wb") as save_file:
            pickle.dump(total_form_list, save_file)
            print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Save -  {pkl_save_path}")
        # check load
        with open(pkl_save_path, mode="rb") as load_file:
            load_pkl_list = pickle.load(load_file)
            print(f"[Ext_Xlsx_Parser][parse_ext_xlsx_files] Check Load -  {pkl_save_path}, size: {len(load_pkl_list)}")


### MAIN ###
if "__main__" == __name__:
    print(f"[parse_ext_xlsx.py][__main__] START !")
    root_dir_path = "../corpus/모두의 말뭉치/ext_xlsx"
    parser = Ext_Xlsx_Parser(root_dir_path)
    parser.parse_ext_xlsx_files()