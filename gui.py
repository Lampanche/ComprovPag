import PySimpleGUI as gui
from analisaPdf import acessar_pastas_e_ler_pdfs, organiza_arquivos
from pathlib import Path
import shutil

layout = [
  [gui.Text("Insira o caminho para organizar os documentos", background_color="black")],
  [gui.Input(key="caminho_inicial_or_docs", size=(50,1))],
  [gui.Button("Organizar",button_color='red')],
  [gui.Text("", key="status_organiza", background_color="black",  text_color="#008000")],
  [gui.Text("Insira o caminho para salvar a pasta com os docs organizados", background_color="black")],
  [gui.Input(key="caminho_salvar_docs_org", size=(50,1))],
  [gui.Button("Salvar docs organizados", button_color='red')],
  [gui.Text("", key="status_salvar_docs_organizados", background_color="black",  text_color="#008000")],
  [gui.Text("Insira o caminho com os docs", background_color="black")],
  [gui.Input(key='caminho_inicial', size=(50,1),)],
  [gui.Button(button_text="Ler arquivos", key = "btn_ler" ,enable_events=True, button_color='red')],
  [gui.Text("", key="status", background_color="black",  text_color="#008000")],
  [gui.Text("Escolha o caminho para salvar", background_color="black")],
  [gui.Input(key="caminho_salvar", size=(50,1))],
  [gui.Button("Salvar", key="Baixar", button_color='red')],
  [gui.Text("", key="status_salvar", background_color="black",  text_color="#008000")]
]

janela = gui.Window("Ler PDF", background_color="black" , icon="hc2.ico" ,layout=layout)

while True:
  event, value = janela.read()

  retorno_extracao_dados = str
  status_salvar = str
  caminho_salvar = str
  caminho_incial = str
  status_organiza = str
  status_salvar_docs_org = str

  if event == gui.WIN_CLOSED:
    break

  caminho_inicial_org_docs = Path(rf"{value['caminho_inicial_or_docs']}")
  caminho_incial = Path(rf"{value['caminho_inicial']}")

  if event == 'Organizar':
    janela["status_organiza"].update("")
    status_organiza = organiza_arquivos(path_inicial_org_arquivos=caminho_inicial_org_docs)

  if(status_organiza != ''):
    janela["status_organiza"].update(status_organiza)

  caminho_salvar_docs_organizados = Path(rf"{value['caminho_salvar_docs_org']}")
  caminho_pasta_interna_docs_org = Path(r"Docs organizados - Outros bancos")

  if event == 'Salvar docs organizados':
    janela["status_salvar_docs_organizados"].update("")

    for files in caminho_pasta_interna_docs_org.iterdir():
      shutil.move(f"{files}", f"{caminho_salvar_docs_organizados}/{files.name}")
    
    status_salvar_docs_org = "Salvei!"

  if status_salvar_docs_org != '':
    janela["status_salvar_docs_organizados"].update(status_salvar_docs_org)

  if event == 'btn_ler':
    janela["status"].update("")
    janela["status_salvar"].update("")
    retorno_extracao_dados = acessar_pastas_e_ler_pdfs(path_inicial=caminho_incial)

  if retorno_extracao_dados != '':
    janela["status"].update(retorno_extracao_dados)

  caminho_salvar = Path(rf"{value['caminho_salvar']}")
  caminho_planilhas = Path(r"Planilhas")

  if event == "Baixar":

    janela["status_salvar"].update("")

    for xlsx in caminho_planilhas.iterdir():

      shutil.move(f"{xlsx}", f"{caminho_salvar}/{xlsx.name}")

    janela["status_salvar"].update("Arquivos salvos!")
    
