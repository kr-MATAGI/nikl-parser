from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class POS_TEXT_DATA:
    id: int = -1
    src_pkl: str = ""
    text: str = ""
    word_pos_pair_list: List[Tuple[str, int]] = field(default_factory=list)