import tabula
import pandas as pd
from PyPDF2 import PdfReader
import regex as rg
from utils import formata_cnpj
import math as mat

class Layout_leitura_sicoob_pix:

    def __init__(self):
      self.lista_dfs_layout_sicoob_pix = []

    def leitura_pdfs_layout_sicoob_pix(self, pdf):

      reader = PdfReader(pdf)

      pages_pdf = len(reader.pages)

      i = 1

      while i <= pages_pdf:

        lista_retornos_leitura_pdf_sicoob_pix = tabula.read_pdf_with_template(pdf, template_path = "./modelos/layout_sicoob_pix.json", pages = f"{i}")

        tamanho_array_retorno = len(lista_retornos_leitura_pdf_sicoob_pix) - 1

        t = 0

        while t <= tamanho_array_retorno:

          self.lista_dfs_layout_sicoob_pix.append(lista_retornos_leitura_pdf_sicoob_pix[t])
          t+=1  
         
        i+=1


    def criacao_plan_layout_sicoob_pix(self, banco, operacao):

      modelo_df = pd.DataFrame(columns = ['Conta', 'Beneficiário', 'CNPJ_CPF', 'Valor pago', "Operação", "Data", "Observacao"])

      tamanho_lista_dfs = len(self.lista_dfs_layout_sicoob_pix) - 1

      f = 0

      while f <= tamanho_lista_dfs:

        for item in self.lista_dfs_layout_sicoob_pix[f].itertuples():

          item_str = str(item[1])

          value_df_razao_social = rg.findall("Nome:", item_str)
          value_df_conta = rg.findall("Conta", item_str)
          value_df_cnpj_cpf = rg.findall("CPF/CNPJ:", item_str)
          value_df_valor_pago = rg.findall("Valor do Pagamento:", item_str)
          value_df_data = rg.findall("Data do Pagamento:", item_str)
          value_observacao = rg.findall("Observação:", item_str)

          if(not type(item[1]) is str):
            if(mat.isnan(item[1]) and int(item[0]) == 19 and item[2] != "OUVIDORIA SICOOB: 08007250996"):
              modelo_df.at[f,"Data"] = item[2]

          if(not type(item[1]) is str):
            if(mat.isnan(item[1]) and int(item[0]) == 22):
              modelo_df.at[f,"Valor pago"] = item[2]  
          
          if(len(value_df_razao_social) > 0):
            modelo_df.at[f,"Beneficiário"] = item[2]
          if(len(value_df_conta) > 0):
            modelo_df.at[f,"Conta"] = item[2]
          if(len(value_df_cnpj_cpf) > 0):
            modelo_df.at[f,"CNPJ_CPF"] = item[2]
          
          if(len(value_df_valor_pago) > 0):
            if(type(item[1]) is str):
              modelo_df.at[f,"Valor pago"] = item[2]
          
          if(len(value_df_data) > 0):
            if(type(item[1]) is str):  
                modelo_df.at[f,"Data"] = item[2]

          if(len(value_observacao) > 0):
            modelo_df.at[f,"Observacao"] = item[2]

          modelo_df.at[f,"Operação"] = "PIX"  

        f += 1

      modelo_df.to_excel(f'Planilhas/{banco}-{operacao}.xlsx')    
