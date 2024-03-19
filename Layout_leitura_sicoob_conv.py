import tabula
import pandas as pd
from PyPDF2 import PdfReader
import regex as rg
import math as mat

class Layout_leitura_sicoob_conv:

    def __init__(self):
      self.lista_dfs_layout_sicoob_conv = []

    def leitura_pdfs_layout_sicoob_conv(self, pdf):

      reader = PdfReader(pdf)

      pages_pdf = len(reader.pages)

      i = 1

      while i <= pages_pdf:

        retorno_leitura_layout_conv_sicoob_1 = tabula.read_pdf_with_template(pdf, template_path = "./modelos/layout_sicoob_conv.json", pages = f"{i}")  

        modelo_df_conv = pd.DataFrame(columns=["Conta", "Convenio", "Data pagamento", "Valor documento", "Valor juros", "Valor multa", "Outros encargos", "Valor desconto", "Outras deducoes", "Valor pago", "Operacao"]) 

        modelo_df_conv_2 = pd.DataFrame(columns=["Conta", "Convenio", "Data pagamento", "Valor documento", "Valor juros", "Valor multa", "Outros encargos", "Valor desconto", "Outras deducoes", "Valor pago", "Operacao"])

        valor_conta = ''
        valor_convenio = ''
        valor_data_pag = ''
        valor_doc = ''
        valor_juros = ''
        valor_multa = ''
        valor_outros_encargos = ''
        valor_desconto = ''
        valor_outras_deducoes = ''
        valor_pago = ''
        valor_operacao = ''

        def verifica_qual_conv():
          for item in retorno_leitura_layout_conv_sicoob_1[0].itertuples():

            verifica_limite_df = []

            tamanho_tupla = len(item)

            item_str = str(item[1])

            if(tamanho_tupla >=3):
              tipo_df = str(item[2])
            else:  
              tipo_df = str(item[1])

            if(int(item[0]) > 6):
              verifica_limite_df = rg.findall("COMPROVANTE DE PAGAMENTO DE CONVÊNIO", tipo_df) or rg.findall("SISBR – SISTEMA DE INFORMÁTICA DO SICOOB", tipo_df)

            verifica_conv = rg.findall("Valor da multa:", item_str)

            if(len(verifica_conv) > 0):
              return verifica_conv

            if(len(verifica_limite_df) > 0):
              break 

        def verifica_qual_limite():
          for item in retorno_leitura_layout_conv_sicoob_1[0].itertuples():

            if(int(item[0]) > 6):

              tamanho_tupla = len(item)

              if(tamanho_tupla >=3):
                tipo_df = str(item[2])
              else:  
                tipo_df = str(item[1])
              
              verifica_limite_df = rg.findall("COMPROVANTE DE PAGAMENTO DE CONVÊNIO", tipo_df) or rg.findall("SISBR", tipo_df)        

              if(len(verifica_limite_df) > 0):
                return item[0]

        def verifica_qual_conv_2(limite):
            for item in retorno_leitura_layout_conv_sicoob_1[0].itertuples():

              if(int(item[0]) > int(limite)):

                item_str = str(item[1])

                verifica_conv = rg.findall("Valor da multa:", item_str)

                if(len(verifica_conv) > 0):
                  return verifica_conv

        conv = verifica_qual_conv()
        
        limite = verifica_qual_limite()

        for item_conv in retorno_leitura_layout_conv_sicoob_1[0].itertuples():
           
          verifica_limite_df = []

          tamanho_tupla = len(item_conv)

          item_conv_str = str(item_conv[1])

          if(tamanho_tupla >=3):
            limite_df = str(item_conv[2])
          else:
            limite_df = str(item_conv[1])  

          if(int(item_conv[0]) >6):
            verifica_limite_df = rg.findall("COMPROVANTE DE PAGAMENTO DE CONVÊNIO", limite_df) or rg.findall("SISBR", limite_df)

          if(conv != None):

            valor_operacao = "CONV"

            valor_conta = rg.findall("Conta:", item_conv_str)
            valor_convenio = rg.findall("Convênio:", item_conv_str)
            valor_data_pag = rg.findall("Data Pagamento:", item_conv_str)
            valor_doc = rg.findall("Valor do documento:", item_conv_str)
            valor_juros = rg.findall("Valor dos juros:", item_conv_str)
            valor_multa = rg.findall("Valor da multa:", item_conv_str)
            valor_outros_encargos = rg.findall("Outros encargos:", item_conv_str)
            valor_desconto = rg.findall("Valor do desconto:", item_conv_str)
            valor_outras_deducoes = rg.findall("Outras deduções:", item_conv_str)
            valor_pago = rg.findall("Valor total:", item_conv_str)     

            if(len(valor_conta) > 0):
              modelo_df_conv.at[0,"Conta"] = item_conv[2]
            if(len(valor_convenio) > 0):
              modelo_df_conv.at[0,"Convenio"] = item_conv[2]
            if(len(valor_data_pag) > 0):
              modelo_df_conv.at[0,"Data pagamento"] = item_conv[2]
            if(len(valor_doc) > 0):
              modelo_df_conv.at[0,"Valor documento"] = item_conv[2]
            if(len(valor_juros) > 0):
              modelo_df_conv.at[0,"Valor juros"] = item_conv[2]
            if(len(valor_multa) > 0):
              modelo_df_conv.at[0,"Valor multa"] = item_conv[2]
            if(len(valor_outros_encargos) > 0):
              modelo_df_conv.at[0,"Outros encargos"] = item_conv[2]
            if(len(valor_desconto) > 0):
              modelo_df_conv.at[0,"Valor desconto"] = item_conv[2]              
            if(len(valor_outras_deducoes) > 0):
              modelo_df_conv.at[0,"Outras deducoes"] = item_conv[2]
            if(len(valor_pago) > 0):
              modelo_df_conv.at[0,"Valor pago"] = item_conv[2] 

            modelo_df_conv.at[0,"Operacao"] = valor_operacao

          elif(conv == None):

            valor_operacao = "SISBR"

            valor_conta = rg.findall("CONTA DEBITADA:", item_conv_str)
            valor_pago = rg.findall("VALOR RECOLHIDO:", item_conv_str)
            valor_convenio = rg.findall("DESCRIÇÃO DO PAGAMENTO:", item_conv_str)
            valor_data_pag = rg.findall("PAGAMENTO EFETUADO EM :", item_conv_str)

            if(len(valor_conta) > 0):
              if(tamanho_tupla >=3):
                modelo_df_conv.at[0,"Conta"] = item_conv[2]
              else:
                modelo_df_conv.at[0,"Conta"] = item_conv[1]

            if(len(valor_convenio) > 0):
              if(tamanho_tupla >=3):
                modelo_df_conv.at[0,"Convenio"] = item_conv[2]
              else:
                modelo_df_conv.at[0,"Convenio"] = item_conv[1]

            if(len(valor_data_pag) > 0):
              if(tamanho_tupla >=3):
                modelo_df_conv.at[0,"Data pagamento"] = item_conv[2]
              else:  
                modelo_df_conv.at[0,"Data pagamento"] = item_conv[1]

            if(len(valor_pago) > 0):
              if(tamanho_tupla >=3):
                modelo_df_conv.at[0,"Valor pago"] = item_conv[2]
              else:
                modelo_df_conv.at[0,"Valor pago"] = item_conv[1] 

            modelo_df_conv.at[0,"Operacao"] = valor_operacao

          if(len(verifica_limite_df) > 0):
            break

        self.lista_dfs_layout_sicoob_conv.append(modelo_df_conv)  

        if(limite):

          conv_2 = verifica_qual_conv_2(limite=limite)

          for item_conv in retorno_leitura_layout_conv_sicoob_1[0].itertuples():

            if(int(item_conv[0]) > int(limite)):

              tamanho_tupla_df_2 = len(item_conv)

              item_conv_str = str(item_conv[1])

              if(conv_2 != None):

                valor_operacao = "CONV"

                valor_conta = rg.findall("Conta:", item_conv_str)
                valor_convenio = rg.findall("Convênio:", item_conv_str)
                valor_data_pag = rg.findall("Data Pagamento:", item_conv_str)
                valor_doc = rg.findall("Valor do documento:", item_conv_str)
                valor_juros = rg.findall("Valor dos juros:", item_conv_str)
                valor_multa = rg.findall("Valor da multa:", item_conv_str)
                valor_outros_encargos = rg.findall("Outros encargos:", item_conv_str)
                valor_desconto = rg.findall("Valor do desconto:", item_conv_str)
                valor_outras_deducoes = rg.findall("Outras deduções:", item_conv_str)
                valor_pago = rg.findall("Valor total:", item_conv_str)     

                if(len(valor_conta) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Conta"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Conta"] = item_conv[2]  
                  else:
                    modelo_df_conv_2.at[0,"Conta"] = item_conv[1]

                if(len(valor_convenio) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Convenio"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Convenio"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Convenio"] = item_conv[1]

                if(len(valor_data_pag) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Data pagamento"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Data pagamento"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Data pagamento"] = item_conv[1]

                if(len(valor_doc) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Valor documento"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Valor documento"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Valor documento"] = item_conv[1]

                if(len(valor_juros) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Valor juros"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Valor juros"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Valor juros"] = item_conv[1]

                if(len(valor_multa) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Valor multa"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Valor multa"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Valor multa"] = item_conv[1]

                if(len(valor_outros_encargos) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Outros encargos"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Outros encargos"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Outros encargos"] = item_conv[1]

                if(len(valor_desconto) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Valor desconto"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Valor desconto"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Valor desconto"] = item_conv[1]

                if(len(valor_outras_deducoes) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Outras deducoes"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Outras deducoes"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Outras deducoes"] = item_conv[1]

                if(len(valor_pago) > 0):
                  if(tamanho_tupla_df_2 >=3):
                    if(type(item_conv[2]) == float):
                      if(mat.isnan(item_conv[2])):
                        modelo_df_conv_2.at[0,"Valor pago"] = item_conv[1]
                    else:
                      modelo_df_conv_2.at[0,"Valor pago"] = item_conv[2]
                  else:  
                    modelo_df_conv_2.at[0,"Valor pago"] = item_conv[1]

                modelo_df_conv_2.at[0,"Operacao"] = valor_operacao

              elif(conv_2 == None):

                valor_operacao = "SISBR"

                valor_conta = rg.findall("CONTA DEBITADA:", item_conv_str)
                valor_pago = rg.findall("VALOR RECOLHIDO:", item_conv_str)
                valor_convenio = rg.findall("DESCRIÇÃO DO PAGAMENTO:", item_conv_str)
                valor_data_pag = rg.findall("PAGAMENTO EFETUADO EM :", item_conv_str)

                if(len(valor_conta) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_conv_2.at[0,"Conta"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Conta"] = item_conv[1]

                if(len(valor_convenio) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_conv_2.at[0,"Convenio"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Convenio"] = item_conv[1]

                if(len(valor_data_pag) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_conv_2.at[0,"Data pagamento"] = item_conv[2]
                  else:  
                    modelo_df_conv_2.at[0,"Data pagamento"] = item_conv[1]

                if(len(valor_pago) > 0):
                  if(tamanho_tupla >=3):
                    modelo_df_conv_2.at[0,"Valor pago"] = item_conv[2]
                  else:
                    modelo_df_conv_2.at[0,"Valor pago"] = item_conv[1]

                modelo_df_conv_2.at[0,"Operacao"] = valor_operacao  

          self.lista_dfs_layout_sicoob_conv.append(modelo_df_conv_2)
        
        i+=1

    def criacao_plan_layout_sicoob_conv(self, banco, operacao):

      modelo_df = pd.DataFrame(columns=["Conta", "Convenio", "Data pagamento", "Valor documento", "Valor juros", "Valor multa", "Outros encargos", "Valor desconto", "Outras deducoes", "Valor pago", "Operacao"])

      tamanho_lista_dfs = len(self.lista_dfs_layout_sicoob_conv) - 1

      f = 0

      while f <= tamanho_lista_dfs:

        for item in self.lista_dfs_layout_sicoob_conv[f].itertuples():

          modelo_df.at[f,"Conta"] = item[1]
          modelo_df.at[f,"Convenio"] = item[2]
          modelo_df.at[f,"Data pagamento"] = item[3]
          modelo_df.at[f,"Valor documento"] = item[4] 
          modelo_df.at[f,"Valor juros"] = item[5] 
          modelo_df.at[f,"Valor multa"] = item[6] 
          modelo_df.at[f,"Outros encargos"] = item[7] 
          modelo_df.at[f,"Valor desconto"] = item[8] 
          modelo_df.at[f,"Outras deducoes"] = item[9] 
          modelo_df.at[f,"Valor pago"] = item[10]
          modelo_df.at[f,"Operacao"] = item[11]    

        f += 1  

      modelo_df.to_excel(f'Planilhas/{banco}-{operacao}.xlsx')    
