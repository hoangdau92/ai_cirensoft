import re
import sys

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def removeMark(text):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def removeSpecialChar(text):
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('.', '')
    text = re.sub('[^a-zA-Z.\d\s]', '', text)
    text = re.sub(' +',' ',text)
    return text

def xulyVIE(text):
    return removeSpecialChar(removeMark(text))

if __name__ == '__main__':
    print(removeMark(sys.argv[1]))