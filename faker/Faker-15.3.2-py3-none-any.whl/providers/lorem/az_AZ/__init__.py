from typing import Dict

from .. import Provider as LoremProvider


class Provider(LoremProvider):
    """Implement lorem provider for ``az_AZ`` locale.

    Word list is based on the source(s) below with some filtering.

    Sources:

    - https://1000mostcommonwords.com/1000-most-common-azerbaijani-words/
    """

    word_list = (
        "kimi",
        "mən",
        "olmaq",
        "at",
        "bir",
        "var",
        "bu",
        "dən",
        "tərəfindən",
        "isti",
        "bilərsiniz",
        "həyata",
        "digər",
        "etmək",
        "onların",
        "vaxt",
        "əgər",
        "olacaq",
        "necə",
        "bildirib",
        "bir",
        "hər",
        "demək",
        "yoxdur",
        "dəst",
        "üç",
        "istəyirəm",
        "hava",
        "quyu",
        "oynamaq",
        "kiçik",
        "son",
        "qoymaq",
        "ev",
        "oxumaq",
        "əl",
        "port",
        "böyük",
        "sehr",
        "əlavə",
        "etmək",
        "hətta",
        "torpaq",
        "burada",
        "lazımdır",
        "böyük",
        "yüksək",
        "belə",
        "izləmək",
        "akt",
        "niyə",
        "soruşmaq",
        "oxumaq",
        "dəyişiklik",
        "getdi",
        "yüngül",
        "cür",
        "müstəqil",
        "ehtiyac",
        "ev",
        "şəkil",
        "çalışmaq",
        "azad",
        "yenidən",
        "heyvan",
        "nöqtə",
        "ana",
        "dünya",
        "yaxın",
        "qurmaq",
        "özü",
        "torpaq",
        "ata",
        "hər",
        "hansı",
        "bir",
        "yeni",
        "iş",
        "hissə",
        "almaq",
        "yer",
        "etdi",
        "yaşamaq",
        "harada",
        "sonra",
        "cümlə",
        "böyük",
    )

    parts_of_speech: Dict[str, tuple] = {}
