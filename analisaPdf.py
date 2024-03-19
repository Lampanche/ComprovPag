from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from leitura_pdf_criacao_plan import verifica_operacao_e_banco_criacao_plan, verifica_operacao_e_banco_leitura_pdf

#listaPdfNLido = []

def remove_itens_array(array):
  i = 0
  while i <= 19:
    del(array[0])
    i += 1
  return len(array) - 1

def escrita_pdf_erro(listaPdfNLido):

  tamanhoArrayErros = len(listaPdfNLido) - 1

  if(tamanhoArrayErros == 0):
    return

  errosLeituraPdf = Canvas("Erros de Leitura.pdf")

  i = 0

  y = 800

  x = 70
 
  while i <= tamanhoArrayErros:

    if(i == 19):
      errosLeituraPdf.drawString(x = x, y = y, text = listaPdfNLido[i])
      errosLeituraPdf.showPage()
      y = 800
      att_tamanho_array = remove_itens_array(array = listaPdfNLido)
      tamanhoArrayErros = att_tamanho_array
      i = 0
    else:
      errosLeituraPdf.drawString(x = x, y = y, text = listaPdfNLido[i])
      y -= 25
      i += 1
    
  errosLeituraPdf.save()

def acessar_pastas_e_ler_pdfs(path_inicial):

  for x in path_inicial.iterdir():
    nome_path_bancos = x.name
    path_bancos = Path(x)

    if(nome_path_bancos != "EXTRATOS COMPLETOS"):

      for pbc in path_bancos.iterdir():
        nome_path_conta_bancaria = pbc.name
        path_conta_bancaria = Path(pbc)

        for pdcomprov in path_conta_bancaria.iterdir():
          nome_path_dia_comprovante = Path(pdcomprov).name
          path_dia_comprovante = Path(pdcomprov)

          existe_pdf = sorted(Path(path_dia_comprovante).glob('*.pdf'))

          if(len(existe_pdf) > 0):

            for pdf in existe_pdf:

              operacoes_realizadas = verifica_operacao_e_banco_leitura_pdf(name_banco = nome_path_bancos, name_pdf = pdf)
              
          else:
            continue
      
      verificacao_plan = verifica_operacao_e_banco_criacao_plan(operacoes_realizadas = operacoes_realizadas)

  return verificacao_plan      

def organiza_arquivos(path_inicial_org_arquivos):

  status_organiza = ''

  for x in path_inicial_org_arquivos.iterdir():
    nome_path_bancos = x.name
    path_bancos = Path(x)
    print(nome_path_bancos)

    if(nome_path_bancos != "EXTRATOS COMPLETOS"):

      for pbc in path_bancos.iterdir():
        nome_path_conta_bancaria = pbc.name
        path_conta_bancaria = Path(pbc)
        print(nome_path_conta_bancaria)
        for pdcomprov in path_conta_bancaria.iterdir():
          nome_path_dia_comprovante = Path(pdcomprov).name
          path_dia_comprovante = Path(pdcomprov)
          print(nome_path_dia_comprovante)

          verifica_arquivos = sorted(Path(path_dia_comprovante).glob('*'))

          if(len(verifica_arquivos) > 0):

            print("identifiquei arquivos!!!")

            for files in verifica_arquivos:

              print(files.name)

              if(files.is_dir()):

                for files_2 in files.iterdir():
                  Path.rename(files_2 ,f"Docs organizados - Outros bancos/{nome_path_bancos} - Dia - {nome_path_dia_comprovante} - Conta - {nome_path_conta_bancaria} - {files_2.name}")

              else:
                Path.rename(files ,f"Docs organizados - Outros bancos/{nome_path_bancos} - Dia - {nome_path_dia_comprovante} - Conta - {nome_path_conta_bancaria} - {files.name}")  

  status_organiza = "Organizado!"              
  return status_organiza              