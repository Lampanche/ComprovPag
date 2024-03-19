import tabula
import pandas as pd
from PyPDF2 import PdfReader
import regex as rg
from utils import formata_cnpj
import psutil

class Layout_leitura_sicoob_bo:

    def __init__(self):
      self.lista_dfs_layout_sicoob_bo = []

    def leitura_pdfs_layout_sicoob_bo(self, pdf):

      reader = PdfReader(pdf)

      pages_pdf = len(reader.pages)

      i = 1

      while i <= pages_pdf:

        retorno_leitura_layout_bo_sicoob = tabula.read_pdf_with_template(pdf, template_path = "./modelos/layout_sicoob_bo.json", pages = f"{i}")

        tamanho_array_retorno = len(retorno_leitura_layout_bo_sicoob) - 1

        o = 0

        while o <= tamanho_array_retorno:

          if(not retorno_leitura_layout_bo_sicoob[o].empty):
            self.lista_dfs_layout_sicoob_bo.append(retorno_leitura_layout_bo_sicoob[o])
          o+=1
         
        i+=1
      
    def criacao_plan_layout_sicoob_bo(self, banco, operacao):

      modelo_df = pd.DataFrame(columns = ['Conta', "Numero doc" ,'Beneficiário', 'CNPJ', 'Valor orginal', 'Valor pago', 'Juros', 'Descontos', "Operação", "Data"])

      tamanho_lista_dfs = len(self.lista_dfs_layout_sicoob_bo) - 1

      f = 0

      value_df_conta = ''
      value_df_cnpj = ''
      value_df_razao_social = ''
      value_df_valor_original = ''
      value_df_valor_pago = ''
      value_df_valor_juros = ''
      value_df_valor_desconto = ''
      value_df_data = ''
      value_df_numero_doc = ''

      while f <= tamanho_lista_dfs:

        for item in self.lista_dfs_layout_sicoob_bo[f].itertuples():
          
          item_str = str(item[1])

          procura_razao_social = rg.findall("Nome/Razão Social do Beneficiário:", item_str)
          procura_cnpj = rg.findall("CPF/CNPJ Beneficiário:", item_str)
          procura_data_pagamento = rg.findall("Data Pagamento:", item_str)
          procura_valor_original = rg.findall("Valor Documento:", item_str)
          procura_desconto = rg.findall("Desconto / Abatimento:", item_str)
          procura_juros = rg.findall("Outros acréscimos:", item_str)
          procura_valor_pago = rg.findall("Valor Pago:", item_str)
          procura_conta = rg.findall("Conta:", item_str)
          procura_numero_doc = rg.findall("No documento:", item_str)

          if(len(procura_razao_social) > 0):
            value_df_razao_social = item[2]
          if(len(procura_cnpj) > 0):
            value_df_cnpj = item[2]
          if(len(procura_data_pagamento) > 0):
            value_df_data = item[2]
          if(len(procura_valor_original) > 0):
            value_df_valor_original = item[2]
          if(len(procura_desconto) > 0):
            value_df_valor_desconto = item[2]
          if(len(procura_juros) > 0):
            value_df_valor_juros = item[2]
          if(len(procura_valor_pago) > 0):
            value_df_valor_pago = item[2]
          if(len(procura_conta) > 0):
            value_df_conta = item[1]
          if(len(procura_numero_doc) > 0):
            value_df_numero_doc = item[2]  
            
        modelo_df.at[f,"Conta"] = value_df_conta
        modelo_df.at[f,"CNPJ"] = formata_cnpj(value_df_cnpj)
        modelo_df.at[f,"Beneficiário"] = value_df_razao_social
        modelo_df.at[f,"Valor orginal"] = value_df_valor_original
        modelo_df.at[f,"Valor pago"] = value_df_valor_pago
        modelo_df.at[f,"Juros"] = value_df_valor_juros
        modelo_df.at[f,"Descontos"] = value_df_valor_desconto
        modelo_df.at[f,"Data"] = value_df_data
        modelo_df.at[f,"Numero doc"] = value_df_numero_doc

        f += 1

      modelo_df.to_excel(f'Planilhas/{banco}-{operacao}.xlsx')    
