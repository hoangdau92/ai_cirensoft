from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_bytes
import io
import pytesseract
import os
import numpy as np
from PIL import Image
from xulytiengviet import xulyVIE
import caculate_keywords as ck
from detect_blank_image import check_blank_image
import img_preprocess as im_process

def pdf_processing(fileName, xoay180):
    pdf_document = "tempfiles\\" + fileName
    pdf = PdfFileReader(pdf_document)


    numpages = pdf.getNumPages()
    PAGES = np.arange(0, numpages)

    data = {}
    i = -1
    for x in PAGES:
        pdf_writer = PdfFileWriter()
        current_page = pdf.getPage(x)
        print("Page " + str(x) + "/" + str(numpages - 1) + ": ========================================")

        sizePDF = current_page.mediaBox
        pwidth = sizePDF[2]
        pheight = sizePDF[3]
        pdf_writer.addPage(current_page)
        r = io.BytesIO()
        pdf_writer.write(r)
        img = convert_from_bytes(r.getvalue(), fmt="jpeg")
        imgName = "images\i" + str(x) + ".png"
        img[0].save(imgName)
        im = Image.open(imgName)
        if check_blank_image(im):
            im.close()
            os.remove(imgName)
            continue
        i += 1
        data[i] = {}
        #im = normalize(im)
        imgwidth, imgheight = im.size

        #print(pwidth * pheight)
        if pwidth > pheight:#giay chung nhan
            boxTitle = (1200, 480, 2300, 1250)
            if pwidth * pheight > 600000:
                boxTitle = (1550, 700, 2950, 1500)
            imCropTitle = im.crop(boxTitle)
            imCropTitle_Y = im_process.filter_color(imCropTitle, mask=im_process.YELLOW_MASK)
            imCropTitle_R = im_process.filter_color(imCropTitle, mask=im_process.RED_MASK)
            #imCropTitle_R.save("images\R" + fileName + str(i) + ".png")
            #imCropTitle_Y.save("images\Y" + fileName + str(i) + ".png")
            textTitle1 = pytesseract.image_to_string(imCropTitle_R, lang='vie')
            textTitle1 = xulyVIE(textTitle1)

            textTitle2 = pytesseract.image_to_string(imCropTitle_Y, lang='vie')
            textTitle2 = xulyVIE(textTitle2)

            textTitle3 = pytesseract.image_to_string(imCropTitle, lang='vie')
            textTitle3 = xulyVIE(textTitle3)

            textTitle = textTitle1 + " " + textTitle2 + " " + textTitle3
            data[i]["textTitle"] = textTitle
            data[i]["loai"] = ""
            data[i]["order"] = 1
            data[i]["wid"] = pwidth
            data[i]["hei"] = pheight
            data[i]["index"] = x
        else:
            boxTitle = (0, 50, imgwidth, 520)
            imCropTitle = im.crop(boxTitle)
            #imCropTitle.save("images\T" + fileName + str(i) + ".png")

            textTitle = pytesseract.image_to_string(imCropTitle, lang='vie')
            textTitle = xulyVIE(textTitle)

            if xoay180:
                im180 = im.rotate(180)
                imCropTitle = im180.crop(boxTitle)
                #imCropTitle.save("images\T" + fileName + str(i) + "X.png")
                #imCropTitle.save("images\is" + str(i) + ".png")


                t = pytesseract.image_to_string(imCropTitle, lang='vie')
                textTitle += xulyVIE(t)

            data[i]["textTitle"] = textTitle
            data[i]["loai"] = ""
            data[i]["order"] = 1
            data[i]["wid"] = pwidth
            data[i]["hei"] = pheight
            data[i]["index"] = x

        im.close()
        os.remove(imgName)

    findTail = False
    currentType = ""
    currentOrder = 0
    i = -1
    while i < len(data) - 1:
        i = i + 1
        item = data[i]
        if item["loai"] == "":
            if not findTail:
                isGCN, order, sl = ck.caculate_similar(item["textTitle"], "gcn")
                if isGCN > 65 and item["wid"] > item["hei"]:
                    item["loai"] = "gcn"
                    item["order"] = order
                    if sl > 1:
                        for j in range(1, sl):
                            data[i + j]["loai"] = "gcn"
                            data[i + j]["order"] = order
                    continue

                isDONDK, order, sl = ck.caculate_similar(item["textTitle"], "dondk")
                if isDONDK > 60:
                    item["loai"] = "dondk"
                    item["order"] = order
                    if sl > 1:
                        for j in range(1, sl):
                            data[i + j]["loai"] = "dondk"
                            data[i + j]["order"] = order
                    continue

                isCHUNGTU, order, sl = ck.caculate_similar(item["textTitle"], "chungtu")
                if isCHUNGTU > 50:
                    item["loai"] = "chungtu"
                    item["order"] = order
                    if sl > 1:
                        for j in range(1, sl):
                            data[i + j]["loai"] = "chungtu"
                            data[i + j]["order"] = order
                    elif sl == -1:
                        findTail = True
                        currentType = "chungtu"
                        currentOrder = order
                    continue

                item["loai"] = "khac"
                item["order"] = 1
            else:
                item["loai"] = currentType
                item["order"] = currentOrder
                isPageMoi = ck.caculate_PageMoi(item["textTitle"])
                if isPageMoi > 75:
                    findTail = False
                    item["loai"] = ""
                    item["order"] = 1
                    i = i - 1


    print("DONE!!!!!!")
    r = []
    for i in data:
        objR = {}
        objR['index'] = data[i]["index"]
        objR['type'] = data[i]['loai']
        objR['order'] = data[i]['order']
        r.append(objR)

    return r

