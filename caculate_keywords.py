from xulytiengviet import xulyVIE
import json

def caculate_similar(text, type):
    if type == "dondk":
        if "DON" not in text:
            return 0, 0, 0
        elif "BIEN BAN" in text:
            return 0, 0, 0
    with open('config\config.json') as json_file:
        data = json.load(json_file)
    # ==============================================
    rate = 0
    order = 0
    sl = 1
    for item in data[type]:
        key = xulyVIE(item['key'])
        sent1 = key.split(' ')
        sent2 = text.split(' ')
        temp = set(sent1) & set(sent2)
        x = len(temp) / len(sent1) * 100
        if rate < x:
            rate = round(x, 2)
            order = item['order']
            sl = item["sl"]
    # ===============================================
    json_file.close()
    s1 = caculate_PageMoi(text)
    s2 = caculate_special(text)
    if type == "gcn":
        return rate, order, sl
    else:
        if s2 < 60:
            if s1 > 65:
                return rate, order, sl
            else:
                return 0, 0, 0
        else:
            return rate, order, sl



def caculate_PageMoi(text):
    # =====================DONDK=====================
    labels = [
        'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM. Độc lập Tự do Hạnh phúc'
    ]
    similar = 0
    for item in labels:
        item = xulyVIE(item)
        sent1 = item.split(' ')
        sent2 = text.split(' ')
        temp = set(sent1) & set(sent2)
        x = len(temp) / len(sent1) * 100
        if similar < x:
            similar = round(x, 2)

    # ===============================================
    return similar

def caculate_special(text):
    # =====================DONDK=====================
    labels = [
        'GIẤY NỘP TIỀN VÀO NGÂN SÁCH NHÀ NƯỚC'
    ]
    similar = 0
    for item in labels:
        item = xulyVIE(item)
        sent1 = item.split(' ')
        sent2 = text.split(' ')
        temp = set(sent1) & set(sent2)
        x = len(temp) / len(sent1) * 100
        if similar < x:
            similar = round(x, 2)

    # ===============================================
    return similar
