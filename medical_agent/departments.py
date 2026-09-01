"""Small transparent department vocabulary used by the course demo."""

import jieba


DEPARTMENTS = {
    "心血管科", "内分泌科", "消化科", "神经科", "呼吸科", "肝病科", "肾内科", "感染科",
    "血液科", "风湿免疫科", "普通内科", "肛肠科", "男科", "神经内科", "皮肤科",
    "耳鼻喉科", "肿瘤科", "口腔科", "眼科", "营养科", "肝胆科", "血管科",
    "新生儿科", "妇产科", "脊柱外科", "普通外科", "整形科", "关节科", "骨科",
    "心外科", "精神心理科", "乳腺科", "传染病科", "颌面外科", "美容科", "结核病科",
    "内科", "产科", "老年科", "职业病科", "康复科", "疼痛科", "麻醉科", "急诊科",
    "重症医学科", "医学影像科", "核医学科", "超声科", "病理科", "中医科",
    "中西医结合科", "针灸科", "推拿科", "理疗科", "心理咨询科", "口腔正畸科",
    "口腔修复科", "口腔颌面外科", "口腔种植科", "口腔预防科", "放射科", "检验科",
    "输血科", "药剂科", "临床药学科", "预防保健科",
}

for department in DEPARTMENTS:
    jieba.add_word(department)


def extract_departments(text):
    """Return unique known department names in first-appearance order."""
    matches = []
    for word in jieba.lcut(text or ""):
        if word in DEPARTMENTS and word not in matches:
            matches.append(word)
    return matches
