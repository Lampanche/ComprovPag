
def formata_cnpj(value_cnpj):
  cnpj_format_carac = str(value_cnpj).replace(".", "").replace("-", "").replace("/", "").replace(",", "")
  cnpj_com_zero = cnpj_format_carac.zfill(14)
  return cnpj_com_zero

