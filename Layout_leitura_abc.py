import tabula
import pandas as pd
from PyPDF2 import PdfReader
import regex as rg
from utils import formata_cnpj


class Layout_leitura_abc:

    def __init__(self):
      self.lista_dfs_layout_abc_bo = []

    def leitura_pdfs_layout_abc_bo(self, pdf):

      reader = PdfReader(pdf)

      pages_pdf = len(reader.pages)

      i = 1

      while i <= pages_pdf:

        self.lista_dfs_layout_abc_bo.append(tabula.read_pdf_with_template(pdf, template_path = "./modelos/layout_abc_bo.json", pages = f"{i}")) 

        i+=1
      
    def criacao_plan_layout_abc_bo(self, banco, operacao):

      modelo_df = pd.DataFrame(columns = ['Conta', 'Beneficiário', 'CNPJ', 'Valor orginal', 'Valor pago', 'Juros', 'Descontos', "Operação", "Data"])

      tamanho_lista_dfs = len(self.lista_dfs_layout_abc_bo) - 1

      f = 0

      while f <= tamanho_lista_dfs:

        value_df_1_tipo = self.lista_dfs_layout_abc_bo[f][0].columns.values[0]

        value_df_2_conta = self.lista_dfs_layout_abc_bo[f][1].iloc[0,0]

        value_df_3 = self.lista_dfs_layout_abc_bo[f][2]

        value_df_3_cnpj = value_df_3.iloc[0,0]
        value_df_3_razao_social = value_df_3.iloc[0,1]

        value_df_4 = self.lista_dfs_layout_abc_bo[f][3]

        value_df_4_valor_pago = value_df_4.iloc[0,0]
        value_df_4_valor_original = value_df_4.iloc[0,1]
        value_df_4_valor_juros = value_df_4.iloc[0,2]
        value_df_4_valor_desconto = value_df_4.iloc[0,3]
          
        modelo_df.at[f,"Conta"] = value_df_2_conta
        modelo_df.at[f,"CNPJ"] = formata_cnpj(value_df_3_cnpj)
        modelo_df.at[f,"Beneficiário"] = value_df_3_razao_social
        modelo_df.at[f,"Valor orginal"] = value_df_4_valor_original
        modelo_df.at[f,"Valor pago"] = value_df_4_valor_pago
        modelo_df.at[f,"Juros"] = value_df_4_valor_juros
        modelo_df.at[f,"Descontos"] = value_df_4_valor_desconto

        f += 1

      modelo_df.to_excel(f'./Planilhas/{banco}-{operacao}.xlsx')    


