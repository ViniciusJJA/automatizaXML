import os
import shutil
import xml.etree.ElementTree as ET

pasta = "caminho/para/sua/pasta/xmls"

cds = {
    "CNPJ_DO_CD_1": "CD 1",
    "CNPJ_DO_CD_2": "CD 2",
    "CNPJ_DO_CD_3": "CD 3",
    "CNPJ_DO_CD_4": "CD 4",
    "CNPJ_DO_CD_5": "CD 5"
}

empresas = {
    "CNPJ_EMPRESA_1": "EMPRESA 1",
    "CNPJ_EMPRESA_2": "EMPRESA 2"
}

ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

backup = os.path.join(pasta, "BACKUP")
os.makedirs(backup, exist_ok=True)

total_xml = 0

erros = 0

for arq in os.listdir(pasta):

    if not arq.endswith(".xml"):
        continue

    total_xml +=1

    caminho = os.path.join(pasta, arq)

    try:
        root = ET.parse(caminho).getroot()

        dest = root.find(".//nfe:dest/nfe:CNPJ", ns)
        emit = root.find(".//nfe:emit/nfe:CNPJ", ns)

        dest = dest.text.strip() if dest is not None and dest.text else ""
        emit = emit.text.strip() if emit is not None and emit.text else ""

        cd = cds.get(dest, "OUTROS")
        emp = empresas.get(emit, "OUTROS")

        pasta_final = os.path.join(pasta, cd, emp)
        os.makedirs(pasta_final, exist_ok=True)

        destino = os.path.join(pasta_final, arq)
    
        if os.path.exists(destino):
            nome, ext = os.path.splitext(arq)
            destino = os.path.join(pasta_final, nome + "_2" + ext)

        shutil.copy2(caminho, destino)

        shutil.move(caminho, os.path.join(backup, arq))

        print(arq, "->", cd, "/", emp)

    except Exception as e:
        erros += 1
        print("erro:", arq, "-", e)
        
        
        
print(f"Total de arquivos XML: {total_xml} \nTotal de erros: {erros}")
    
    