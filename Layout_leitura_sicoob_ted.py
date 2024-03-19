import tabula
import pandas as pd
from PyPDF2 import PdfReader
import regex as rg
from utils import formata_cnpj
import math as mat

class Layout_leitura_sicoob_ted:

  def __init__(self):
    self.lista_dfs_layout_sicoob_ted = []

  def leitura_pdfs_layout_sicoob_ted(self, pdf):

      reader = PdfReader(pdf)

      pages_pdf = len(reader.pages)

      i = 1

      while i <= pages_pdf:

        retorno_leitura_layout_ted_sicoob_1 = tabula.read_pdf_with_template(pdf, template_path = "./modelos/layout_sicoob_ted.json", pages = f"{i}")  

        modelo_df_ted = pd.DataFrame(columns=["Conta", "Data pagamento", "Valor Transferencia", "Destinatário", "CNPJ/CPF", "Operacao"]) 

        modelo_df_ted_2 = pd.DataFrame(columns=["Conta", "Data pagamento", "Valor Transferencia", "Destinatário", "CNPJ/CPF", "Operacao"])

        valor_conta = ''
        valor_data_pag = ''
        valor_transferencia = ''
        valor_destinatario = ''
        valor_cnpj_cpf = ''
        valor_operacao = ''
        valor_cooperativa = ''

        def verifica_qual_conv():
          for item in retorno_leitura_layout_ted_sicoob_1[0].itertuples():

            verifica_limite_df = []

            tamanho_tupla = len(item)

            item_str = str(item[1])

            if(tamanho_tupla >=3):
              tipo_df = str(item[2])
            else:  
              tipo_df = str(item[1])

            if(int(item[0]) > 6):
              verifica_limite_df = rg.findall("COMPROVANTE DE TED", tipo_df) or rg.findall("CONTAS CORRENTES", tipo_df)

            verifica_conv = rg.findall("CPF/CNPJ:", item_str)

            if(len(verifica_conv) > 0):
              return verifica_conv

            if(len(verifica_limite_df) > 0):
              break 

        def verifica_qual_limite():
          for item in retorno_leitura_layout_ted_sicoob_1[0].itertuples():

            if(int(item[0]) > 6):

              tamanho_tupla = len(item)

              if(tamanho_tupla >=3):
                tipo_df = str(item[2])
              else:  
                tipo_df = str(item[1])
              
              verifica_limite_df = rg.findall("COMPROVANTE DE TED", tipo_df) or rg.findall("CONTAS CORRENTES", tipo_df)        

              if(len(verifica_limite_df) > 0):
                return item[0]

        def verifica_qual_conv_2(limite):
            for item in retorno_leitura_layout_ted_sicoob_1[0].itertuples():

              if(int(item[0]) > int(limite)):

                item_str = str(item[1])

                verifica_conv = rg.findall("CPF/CNPJ:", item_str)

                if(len(verifica_conv) > 0):
                  return verifica_conv

        conv = verifica_qual_conv()
        
        limite = verifica_qual_limite()

        for item_conv in retorno_leitura_layout_ted_sicoob_1[0].itertuples():
           
          verifica_limite_df = []

          tamanho_tupla = len(item_conv)

          item_conv_str = str(item_conv[1])

          if(tamanho_tupla >=3):
            limite_df = str(item_conv[2])
          else:
            limite_df = str(item_conv[1])  

          if(int(item_conv[0]) > 6):
            verifica_limite_df = rg.findall("COMPROVANTE DE TED", limite_df) or rg.findall("CONTAS CORRENTES", limite_df)

          if(conv != None):

            valor_operacao = "TED-1"

            valor_conta = rg.findall("Conta:", item_conv_str)
            valor_transferencia = rg.findall("Valor:", item_conv_str)
            valor_data_pag = rg.findall("Agendado para:", item_conv_str)
            valor_destinatario = rg.findall("Nome:", item_conv_str)
            valor_cnpj_cpf = rg.findall("CPF/CNPJ:", item_conv_str)
            valor_cooperativa = rg.findall("Cooperativa:", item_conv_str)

            if(len(valor_cooperativa) > 0):
              index_cooperativa = item_conv[0]

            if(len(valor_conta) > 0):
              index_valor_conta = item_conv[0]

              if(int(index_valor_conta) == int(index_cooperativa) + 1):
                if(tamanho_tupla >=3):
                  if(type(item_conv[2]) == float):
                    if(mat.isnan(item_conv[2])):
                      modelo_df_ted.at[0,"Conta"] = item_conv[1]
                  else:
                    modelo_df_ted.at[0,"Conta"] = item_conv[2]
                else:
                  modelo_df_ted.at[0,"Conta"] = item_conv[1]     

            if(len(valor_transferencia) > 0):
              modelo_df_ted.at[0,"Valor Transferencia"] = item_conv[2]

            if(len(valor_data_pag) > 0):
              modelo_df_ted.at[0,"Data pagamento"] = item_conv[2]

            if(len(valor_destinatario) > 0):
              modelo_df_ted.at[0,"Destinatário"] = item_conv[2]

            if(len(valor_cnpj_cpf) > 0):
              modelo_df_ted.at[0,"CNPJ/CPF"] = item_conv[2]

            modelo_df_ted.at[0,"Operacao"] = valor_operacao

          elif(conv == None):

            valor_operacao = "TED-2"

            valor_conta = rg.findall("RGL ENGENHARIA E CONSULTORIA LTDA",limite_df)
            valor_transferencia = rg.findall("Valor:", item_conv_str)
            valor_data_pag = rg.findall("Data da Transferência:", item_conv_str)
            valor_destinatario = rg.findall("Conta:", item_conv_str)

            if(len(valor_conta) > 0):
              if(tamanho_tupla >=3):
                modelo_df_ted.at[0,"Conta"] = item_conv[2]
              else:
                modelo_df_ted.at[0,"Conta"] = item_conv[1]

            if(len(valor_transferencia) > 0):
              if(tamanho_tupla >=3):
                modelo_df_ted.at[0,"Valor Transferencia"] = item_conv[2]
              else:
                modelo_df_ted.at[0,"Valor Transferencia"] = item_conv[1]

            if(len(valor_data_pag) > 0):
              if(tamanho_tupla >=3):
                modelo_df_ted.at[0,"Data pagamento"] = item_conv[2]
              else:  
                modelo_df_ted.at[0,"Data pagamento"] = item_conv[1]

            if(len(valor_destinatario) > 0):
              if(tamanho_tupla >=3):
                modelo_df_ted.at[0,"Destinatário"] = item_conv[2]
              else:
                modelo_df_ted.at[0,"Destinatário"] = item_conv[1] 

            modelo_df_ted.at[0,"Operacao"] = valor_operacao

          if(len(verifica_limite_df) > 0):
            break

        self.lista_dfs_layout_sicoob_ted.append(modelo_df_ted)  

        if(limite):

          conv_2 = verifica_qual_conv_2(limite=limite)

          for item_conv in retorno_leitura_layout_ted_sicoob_1[0].itertuples():

            if(int(item_conv[0]) > int(limite)):

              tamanho_tupla_df_2 = len(item_conv)

              item_conv_str = str(item_conv[1])

              if(tamanho_tupla_df_2 >=3):
                item_conv_str_2 = str(item_conv[2])
              else:
                item_conv_str_2 = str(item_conv[1])  

              if(conv_2 != None):

                valor_operacao = "TED-1"

                valor_conta = rg.findall("Conta:", item_conv_str)
                valor_transferencia = rg.findall("Valor:", item_conv_str)
                valor_data_pag = rg.findall("Agendado para:", item_conv_str)
                valor_destinatario = rg.findall("Nome:", item_conv_str)
                valor_cnpj_cpf = rg.findall("CPF/CNPJ:", item_conv_str)
                valor_cooperativa = rg.findall("Cooperativa:", item_conv_str)

                if(len(valor_cooperativa) > 0):
                  index_cooperativa = item_conv[0]

                if(len(valor_conta) > 0):
                  index_valor_conta = item_conv[0]

                  if(int(index_valor_conta) == int(index_cooperativa) + 1):
                    if(tamanho_tupla_df_2 >=3):
                      if(type(item_conv[2]) == float):
                        if(mat.isnan(item_conv[2])):
                          modelo_df_ted_2.at[0,"Conta"] = item_conv[1]
                      else:
                        modelo_df_ted_2.at[0,"Conta"] = item_conv[2]
                    else:
                      modelo_df_ted_2.at[0,"Conta"] = item_conv[1]

                if(len(valor_data_pag) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_ted_2.at[0,"Data pagamento"] = item_conv[1]
                    else:
                      modelo_df_ted_2.at[0,"Data pagamento"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Data pagamento"] = item_conv[1]

                if(len(valor_transferencia) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_ted_2.at[0,"Valor Transferencia"] = item_conv[1]
                    else:
                      modelo_df_ted_2.at[0,"Valor Transferencia"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Valor Transferencia"] = item_conv[1]

                if(len(valor_destinatario) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_ted_2.at[0,"Destinatário"] = item_conv[1]
                    else:
                      modelo_df_ted_2.at[0,"Destinatário"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Destinatário"] = item_conv[1]

                if(len(valor_cnpj_cpf) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_ted_2.at[0,"CNPJ/CPF"] = item_conv[1]
                    else:
                      modelo_df_ted_2.at[0,"CNPJ/CPF"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"CNPJ/CPF"] = item_conv[1]              

                modelo_df_ted_2.at[0,"Operacao"] = valor_operacao

              elif(conv_2 == None):

                valor_operacao = "TED-2"

                valor_conta = rg.findall("RGL ENGENHARIA E CONSULTORIA LTDA", item_conv_str_2)
                valor_transferencia = rg.findall("Valor:", item_conv_str)
                valor_data_pag = rg.findall("Data da Transferência:", item_conv_str)
                valor_destinatario = rg.findall("Conta:", item_conv_str)

                if(len(valor_conta) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_ted_2.at[0,"Conta"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Conta"] = item_conv[1]

                if(len(valor_transferencia) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_ted_2.at[0,"Valor Transferencia"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Valor Transferencia"] = item_conv[1]

                if(len(valor_data_pag) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_ted_2.at[0,"Data pagamento"] = item_conv[2]
                  else:  
                    modelo_df_ted_2.at[0,"Data pagamento"] = item_conv[1]

                if(len(valor_destinatario) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_ted_2.at[0,"Destinatário"] = item_conv[2]
                  else:
                    modelo_df_ted_2.at[0,"Destinatário"] = item_conv[1] 

                modelo_df_ted_2.at[0,"Operacao"] = valor_operacao

          self.lista_dfs_layout_sicoob_ted.append(modelo_df_ted_2)
        
        i+=1

  def criacao_plan_layout_sicoob_ted(self, banco, operacao):

      modelo_df = pd.DataFrame(columns=["Conta", "Data pagamento", "Valor Transferencia", "Destinatário", "CNPJ/CPF", "Operacao"])

      tamanho_lista_dfs = len(self.lista_dfs_layout_sicoob_ted) - 1

      f = 0

      while f <= tamanho_lista_dfs:

        for item in self.lista_dfs_layout_sicoob_ted[f].itertuples():

          modelo_df.at[f,"Conta"] = item[1]
          modelo_df.at[f,"Data pagamento"] = item[2]
          modelo_df.at[f,"Valor Transferencia"] = item[3]
          modelo_df.at[f,"Destinatário"] = item[4] 
          modelo_df.at[f,"CNPJ/CPF"] = item[5] 
          modelo_df.at[f,"Operacao"] = item[6]    

        f += 1  

      modelo_df.to_excel(f'Planilhas/{banco}-{operacao}.xlsx')   

