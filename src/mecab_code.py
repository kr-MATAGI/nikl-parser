import pickle
import os
from konlpy.tag import Mecab
from data_def import POS_TEXT_DATA

'''
    To. 승렬:
        @TODO : text 필터링(필요가 있으면, 길이 기준?), txt로 사람눈으로 확인할 수 있게, 지금은 쓰는데 편리함에 목적을 둠
'''

### MAIN ###
if "__main__" == __name__:
    print(f"[mecab_code.py][__main__] START !")

    mecab = Mecab()

    src_pkl_dir = "../corpus/모두의 말뭉치/result/only_text"
    src_pkl_list = os.listdir(src_pkl_dir)
    print(f"[mecab_code.py][__main__] src_pkl_list: size - {len(src_pkl_list)}\nlist: {src_pkl_list} !")

    data_id = 1
    total_pos_text_list = []
    for pkl_idx, pkl_name in enumerate(src_pkl_list):
        print(f"[mecab_code.py][__main__] {pkl_idx}, {pkl_name} is Processing ...")
        pkl_path = src_pkl_dir + "/" + pkl_name

        pkl_text_list = []
        with open(pkl_path, mode="rb") as pkl_file:
            pkl_text_list = pickle.load(pkl_file)
            print(f"[mecab_code.py][__main__] LOAD - size: {len(pkl_text_list)} !")
        if 0 >= len(pkl_text_list):
            print(f"[mecab_code.py][__main__] ERR - size: {len(pkl_text_list)} !")
            exit(1)

        for pkl_text_idx, pkl_text in enumerate(pkl_text_list):
            if 0 == (pkl_text_idx % 50000):
                print(f"[mecab_code.py][__main__] {pkl_idx}, {pkl_name}, pkl_text_idx: {pkl_text_idx} is Processing ...")
            # 문장 짧은거 필터링 하는 코드 넣어도 좋음
            text_pos = mecab.pos(pkl_text)
            pos_text_data = POS_TEXT_DATA(id=data_id,
                                          src_pkl=pkl_name,
                                          text=pkl_text,
                                          word_pos_pair_list=text_pos)
            total_pos_text_list.append(pos_text_data)
            data_id += 1
        # end, pkl_text_list loop
    # end, src_pkl_list loop
    print(f"[mecab_code.py][__main__] Complete Mecab task - total_pos_text_list.size : {total_pos_text_list}")

    # save pkl
    save_path = "./text_pos_result.pkl"
    with open(save_path, mode="wb") as save_file:
        pickle.dump(total_pos_text_list, save_file)
        print(f"[mecab_code.py][__main__] Save - path : {save_path}")

    # check pkl
    with open(save_path, mode="rb") as load_file:
        check_list = pickle.load(load_file)
        print(f"[mecab_code.py][__main__] Load - path : {save_path}, size: {len(check_list)}")