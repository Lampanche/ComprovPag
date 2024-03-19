import regex as rg
from Layout_leitura_abc import Layout_leitura_abc
from Layout_leitura_sicoob_bo import Layout_leitura_sicoob_bo
from Layout_leitura_sicoob_ted import Layout_leitura_sicoob_ted
from Layout_leitura_sicoob_pix import Layout_leitura_sicoob_pix
from Layout_leitura_sicoob_conv import Layout_leitura_sicoob_conv

layout_abc = Layout_leitura_abc()
layout_sicoob_bo = Layout_leitura_sicoob_bo()
layout_sicoob_ted = Layout_leitura_sicoob_ted()
layout_sicoob_pix = Layout_leitura_sicoob_pix()
layout_sicoob_conv = Layout_leitura_sicoob_conv()


def exclui_banco_array(array, banco):

  tamanho_array = len(array) - 1

  i = 0

  while i <= tamanho_array:

    if(array[i] == banco):
      del(array[i])
      tamanho_array = novo_tamanho_array = len(array) - 1
    i += 1


operacoes_realizadas = {
    "BOLETO": {
      "BANCOS": []
    },
    "TED": {
      "BANCOS": []
    },
    "PIX": {
      "BANCOS": []
    },
    "CONV": {
      "BANCOS": []
    },
  }


def verifica_operacao_e_banco_leitura_pdf(name_banco,name_pdf):

  conf_regex = str(name_pdf)

  conferencia_nome_arquivo = rg.findall("BOLETO", conf_regex) or rg.findall("PIX", conf_regex) or rg.findall("TED", conf_regex) or rg.findall("CONV", conf_regex)

  if(len(conferencia_nome_arquivo) > 0):

    if(name_banco == "ABC" and conferencia_nome_arquivo[0] == "BOLETO"):
      layout_abc.leitura_pdfs_layout_abc_bo(name_pdf)
      operacoes_realizadas[conferencia_nome_arquivo[0]]["BANCOS"].append(name_banco)
      
    if(name_banco == "SICOOB" and conferencia_nome_arquivo[0] == "BOLETO"):
      layout_sicoob_bo.leitura_pdfs_layout_sicoob_bo(name_pdf)
      operacoes_realizadas[conferencia_nome_arquivo[0]]["BANCOS"].append(name_banco)

    if(name_banco == "SICOOB" and conferencia_nome_arquivo[0] == "TED"):
      layout_sicoob_ted.leitura_pdfs_layout_sicoob_ted(name_pdf)
      operacoes_realizadas[conferencia_nome_arquivo[0]]["BANCOS"].append(name_banco)
      
    if(name_banco == "SICOOB" and conferencia_nome_arquivo[0] == "PIX"):
      layout_sicoob_pix.leitura_pdfs_layout_sicoob_pix(name_pdf)
      operacoes_realizadas[conferencia_nome_arquivo[0]]["BANCOS"].append(name_banco)
      
    if(name_banco == "SICOOB" and conferencia_nome_arquivo[0] == "CONV"):
      layout_sicoob_conv.leitura_pdfs_layout_sicoob_conv(name_pdf)
      operacoes_realizadas[conferencia_nome_arquivo[0]]["BANCOS"].append(name_banco)

  
  return operacoes_realizadas

def verifica_operacao_e_banco_criacao_plan(operacoes_realizadas):
  
  criacao_planilhas = ''

  if("ABC" in operacoes_realizadas.get("BOLETO").get("BANCOS")):
    layout_abc.criacao_plan_layout_abc_bo(banco = "ABC", operacao = "BOLETO")
    exclui_banco_array(array = operacoes_realizadas.get("BOLETO").get("BANCOS"), banco = "ABC")


  if("SICOOB" in operacoes_realizadas.get("BOLETO").get("BANCOS")):
    layout_sicoob_bo.criacao_plan_layout_sicoob_bo(banco = "SICOOB", operacao = "BOLETO")
    exclui_banco_array(array = operacoes_realizadas.get("BOLETO").get("BANCOS"), banco = "SICOOB")

  
  if("SICOOB" in operacoes_realizadas.get("TED").get("BANCOS")):
    layout_sicoob_ted.criacao_plan_layout_sicoob_ted(banco = "SICOOB", operacao = "TED")
    exclui_banco_array(array = operacoes_realizadas.get("TED").get("BANCOS"), banco = "SICOOB")


  if("SICOOB" in operacoes_realizadas.get("PIX").get("BANCOS")):
    layout_sicoob_pix.criacao_plan_layout_sicoob_pix(banco = "SICOOB", operacao = "PIX")
    exclui_banco_array(array = operacoes_realizadas.get("PIX").get("BANCOS"), banco = "SICOOB")


  if("SICOOB" in operacoes_realizadas.get("CONV").get("BANCOS")):
    layout_sicoob_conv.criacao_plan_layout_sicoob_conv(banco = "SICOOB", operacao = "CONV")
    exclui_banco_array(array = operacoes_realizadas.get("CONV").get("BANCOS"), banco = "SICOOB")   

  criacao_planilhas = "Terminei a extração dos dados"
  return criacao_planilhas