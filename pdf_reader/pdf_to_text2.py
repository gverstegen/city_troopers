import tempfile, subprocess

def pdf_to_string(file_object):
    pdfData = file_object.read()
    tf = tempfile.NamedTemporaryFile()
    tf.write(pdfData)
    tf.seek(0)
    outputTf = tempfile.NamedTemporaryFile()

    if (len(pdfData) > 0) :
        out, err = subprocess.Popen(["pdftotext", "-layout", tf.name, outputTf.name ]).communicate()
        return outputTf.read()
    else :
        return None

pdfFileObj = open('C:/Users/gjave/Desktop/Biergarten2018-BASISMENU-DRIELUIK-JUNI-FOOD.pdf', 'rb')
print(pdf_to_string(pdfFileObj))


pdfFileObj = open('C:/Users/gjave/Desktop/Biergarten2018-BASISMENU-DRIELUIK-JUNI-FOOD.pdf', 'rb')
pdfData = pdfFileObj.read()
tf = tempfile.NamedTemporaryFile()
tf.write(pdfData)
tf.seek(0)
outputTf = tempfile.NamedTemporaryFile()
out, err = subprocess.Popen(["pdftotext", pdfFileObj, "-layout", tf.name, outputTf.name], shell=True).communicate()
