import trafilatura
import requests
import logging
from typing import Dict, List
from urllib.parse import urljoin
import time

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.

    Some common website to crawl information from:
    MLB scores: https://www.mlb.com/scores/YYYY-MM-DD
    """
    # Send a request to the website
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text

class NCMScraper:
    """
    Web scraper para obter dados de códigos NCM do portal oficial
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_expanded_ncm_database(self) -> Dict[str, Dict]:
        """
        Retorna base expandida de códigos NCM com milhares de entradas
        """
        return {
            # ELETRÔNICOS E TECNOLOGIA - Expandido
            '85171100': {'description': 'Telefones móveis (celulares) e de outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85171200': {'description': 'Telefones para redes celulares ou outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176200': {'description': 'Aparelhos receptores para radiotelefonia ou radiotelegrafia', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176100': {'description': 'Outros aparelhos para recepção, conversão e transmissão ou regeneração de voz, imagens', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '84713000': {'description': 'Máquinas automáticas para processamento de dados, portáteis, de peso não superior a 10 kg', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714100': {'description': 'Outras máquinas automáticas para processamento de dados', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714900': {'description': 'Outras máquinas automáticas para processamento de dados, apresentadas sob a forma de sistemas', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85258000': {'description': 'Câmeras de televisão, câmeras fotográficas digitais e câmeras de vídeo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85287200': {'description': 'Aparelhos receptores para televisão, mesmo incorporando um aparelho receptor', 'ii_rate': 0.20, 'ipi_rate': 0.20, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85234900': {'description': 'Outros discos, fitas e outros suportes para gravação de som', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84661000': {'description': 'Porta-ferramentas e fieiras de abertura automática para máquinas-ferramentas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85444200': {'description': 'Cabos coaxiais e outros condutores elétricos coaxiais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90182000': {'description': 'Instrumentos e aparelhos para medicina, cirurgia, odontologia ou veterinária', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85232000': {'description': 'Discos magnéticos', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85239000': {'description': 'Outros suportes preparados para gravação de som ou gravações análogas', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # VESTUÁRIO E MODA - Massivamente Expandido
            '61051000': {'description': 'Camisas de malha de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61052000': {'description': 'Camisas de malha de fibras sintéticas ou artificiais, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61091000': {'description': 'T-shirts, camisetas interiores e artigos semelhantes de malha de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61099000': {'description': 'T-shirts, camisetas interiores e artigos semelhantes de malha de outras matérias têxteis', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61101100': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de lã', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61101200': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de pelos finos', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61102000': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61103000': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61112000': {'description': 'Vestuário e seus acessórios, de malha, para bebês, de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61124000': {'description': 'Maiôs e biquínis de malha de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62019200': {'description': 'Sobretudos, impermeáveis, casacos, capas e artigos semelhantes, de algodão, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62033100': {'description': 'Paletós (casacos) de lã ou pelos finos, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62034200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62034300': {'description': 'Calças, jardineiras, bermudas e shorts, de fibras sintéticas, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62046200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62052000': {'description': 'Camisas de fibras sintéticas ou artificiais, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62064000': {'description': 'Blusas, camisas e camisas-blusas, de fibras sintéticas ou artificiais, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62111100': {'description': 'Maiôs e biquínis, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62121000': {'description': 'Soutiens (sutiãs) de qualquer matéria têxtil', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62171000': {'description': 'Outros acessórios confeccionados do vestuário', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '65050000': {'description': 'Chapéus e outros artigos de uso semelhante, de malha ou confeccionados com rendas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # CALÇADOS - Expandido
            '64019200': {'description': 'Outros calçados impermeáveis de borracha que cubram o joelho', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64021900': {'description': 'Outros calçados com sola exterior e parte superior de borracha ou plástico', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64022000': {'description': 'Calçados com sola exterior e parte superior de borracha ou plástico, com parte superior em tiras', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64032000': {'description': 'Outros calçados com sola de couro natural e parte superior que cubra o tornozelo', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64039100': {'description': 'Calçados com sola exterior de couro natural, que cubram o tornozelo', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64039900': {'description': 'Outros calçados com sola de borracha, plástico, couro natural ou reconstituído', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041100': {'description': 'Calçados para esporte; calçados para tênis, basquetebol, ginástica, treinamento e semelhantes', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041900': {'description': 'Outros calçados com sola de borracha ou plástico', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64051000': {'description': 'Outros calçados com parte superior de couro natural', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64052000': {'description': 'Outros calçados com parte superior de matérias têxteis', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64069000': {'description': 'Partes de calçados (incluindo as partes superiores fixadas a solas que não sejam as solas exteriores)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # ARTIGOS DE COURO E BAGAGEM - Expandido
            '42021100': {'description': 'Malas, maletas e artigos semelhantes, com superfície exterior de couro natural, couro reconstituído ou couro envernizado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42021200': {'description': 'Malas, maletas e artigos semelhantes, com superfície exterior de plástico ou matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42022100': {'description': 'Bolsas, mesmo com alça, normalmente carregadas na mão, com superfície exterior de couro natural', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42022200': {'description': 'Bolsas, mesmo com alça, normalmente carregadas na mão, com superfície exterior de folhas de plástico ou matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42023100': {'description': 'Artigos de bolso ou de bolsa de mão, com superfície exterior de couro natural', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42023200': {'description': 'Artigos de bolso ou de bolsa de mão, com superfície exterior de folhas de plástico ou matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42031000': {'description': 'Vestuário de couro natural ou couro reconstituído', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42032100': {'description': 'Luvas, mitenes e semelhantes, especialmente concebidas para esporte', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42032900': {'description': 'Outras luvas, mitenes e semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42033000': {'description': 'Cintos e bandoleiras', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '42034000': {'description': 'Outros acessórios do vestuário', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # COSMÉTICOS E PERFUMARIA - Expandido
            '33030000': {'description': 'Perfumes e águas-de-colônia', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33041000': {'description': 'Produtos de maquiagem para os lábios', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33042000': {'description': 'Produtos de maquiagem para os olhos', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33043000': {'description': 'Preparações para manicuros e pedicuros', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33049100': {'description': 'Pós, incluindo os pós compactos', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33049900': {'description': 'Outros produtos de beleza, maquiagem e cuidados da pele', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33051000': {'description': 'Xampus para o cabelo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33052000': {'description': 'Preparações para ondulação ou alisamento permanentes dos cabelos', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33053000': {'description': 'Lacas para o cabelo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33059000': {'description': 'Outras preparações capilares', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33061000': {'description': 'Dentifrícios (cremes dentais)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33062000': {'description': 'Fio utilizados para limpeza dos espaços interdentais (fio dental)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33069000': {'description': 'Outras preparações para higiene bucal ou dentária', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33071000': {'description': 'Preparações para barbear (antes, durante ou após)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33072000': {'description': 'Desodorantes corporais e antitranspirantes', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33079000': {'description': 'Outras preparações para perfumar e outros produtos de higiene', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # BRINQUEDOS E JOGOS - Expandido
            '95030010': {'description': 'Triciclos, patinetes, carros de pedal e outros brinquedos semelhantes de rodas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95030090': {'description': 'Outros brinquedos de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95031000': {'description': 'Trens elétricos, incluindo os trilhos, sinais e outros acessórios', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95032000': {'description': 'Outros modelos reduzidos e modelos semelhantes, mesmo animados; quebra-cabeças (puzzles)', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034100': {'description': 'Bonecas que representem exclusivamente seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034200': {'description': 'Vestuário e seus acessórios para bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034300': {'description': 'Outras partes e acessórios para bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034900': {'description': 'Outros brinquedos que representem animais ou criaturas não humanas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95035000': {'description': 'Outros brinquedos de construção', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95036000': {'description': 'Quebra-cabeças (puzzles)', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95037000': {'description': 'Outros brinquedos, modelos reduzidos em escala para diversão', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95038000': {'description': 'Outros brinquedos e modelos, incorporando um motor elétrico', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95039000': {'description': 'Outros brinquedos; modelos reduzidos em escala', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95041000': {'description': 'Videojogos dos tipos utilizados com receptor de televisão', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95049000': {'description': 'Outros artigos para jogos de sociedade, incluindo os jogos com motor ou outros mecanismos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95051000': {'description': 'Artigos para festas de Natal', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # ARTIGOS ESPORTIVOS - Expandido
            '95061100': {'description': 'Esquis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95061200': {'description': 'Fixações para esquis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95061900': {'description': 'Outros equipamentos para esqui', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062100': {'description': 'Pranchas à vela', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062200': {'description': 'Esquis aquáticos, pranchas de surf e outros equipamentos para esportes aquáticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062900': {'description': 'Outras bolas infláveis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95063100': {'description': 'Tacos de golfe, completos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95063200': {'description': 'Bolas de golfe', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95063900': {'description': 'Outros equipamentos para golfe', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95064000': {'description': 'Artigos e equipamentos para tênis de mesa', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95065100': {'description': 'Raquetes de tênis, mesmo não encordoadas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95065900': {'description': 'Raquetes de badminton e raquetes semelhantes, mesmo não encordoadas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95066100': {'description': 'Bolas de tênis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95066200': {'description': 'Bolas infláveis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95066900': {'description': 'Outras bolas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95067000': {'description': 'Patins de gelo e patins de rodas, incluindo os patins fixados ao calçado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95069100': {'description': 'Artigos e equipamentos para cultura física, ginástica ou atletismo', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95069900': {'description': 'Outros artigos e equipamentos para esportes e jogos ao ar livre', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # JOIAS E RELÓGIOS - Expandido  
            '71131100': {'description': 'Artigos de joalharia de metais preciosos, de prata', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71131900': {'description': 'Outros artigos de joalharia de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71132000': {'description': 'Artigos de joalharia de metais folheados ou chapeados de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71171100': {'description': 'Abotoaduras e botões semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71171900': {'description': 'Bijuterias de outros metais comuns', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '71179000': {'description': 'Outras bijuterias', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91011100': {'description': 'Relógios de pulso, elétricos, mesmo com contador de tempo incorporado, com caixa de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91011900': {'description': 'Outros relógios de pulso, elétricos, mesmo com contador de tempo incorporado', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91012100': {'description': 'Relógios de pulso, automáticos, com caixa de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91012900': {'description': 'Outros relógios de pulso, automáticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91019100': {'description': 'Relógios de bolso e outros relógios, incluindo os cronômetros, elétricos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91019900': {'description': 'Outros relógios de bolso e outros relógios, incluindo os cronômetros', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # ÓCULOS E ÓTICA - Expandido
            '90031100': {'description': 'Armações para óculos ou artigos semelhantes, de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90031900': {'description': 'Outras armações para óculos ou artigos semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90039000': {'description': 'Partes de armações e de monturas para óculos ou artigos semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90041000': {'description': 'Óculos de sol', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90049000': {'description': 'Outros óculos corretivos, protetores ou outros', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # MÓVEIS - Expandido
            '94017100': {'description': 'Assentos com armação de madeira, estofados', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017900': {'description': 'Outros assentos com armação de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94018000': {'description': 'Outros assentos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94035000': {'description': 'Móveis de madeira dos tipos utilizados em dormitórios', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94036000': {'description': 'Outros móveis de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94037000': {'description': 'Móveis de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94038100': {'description': 'Móveis de bambu', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94038200': {'description': 'Móveis de vime', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94038900': {'description': 'Móveis de outras matérias', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94039000': {'description': 'Partes de móveis', 'ii_rate': 0.14, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94041000': {'description': 'Somiês (estrados)', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94042100': {'description': 'Colchões de borracha alveolar ou de plástico alveolar', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94042900': {'description': 'Colchões de outras matérias', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94043000': {'description': 'Sacos de dormir', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94049000': {'description': 'Outros artigos de cama e artigos semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # LUMINÁRIA E ILUMINAÇÃO - Expandido
            '94051000': {'description': 'Lustres e outros aparelhos elétricos de iluminação, próprios para serem suspensos ou fixados no teto ou na parede', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94052000': {'description': 'Abajures de cabeceira, de escritório e luminárias de interior, elétricos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94053000': {'description': 'Guirlandas elétricas dos tipos utilizados em árvores de Natal', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94054000': {'description': 'Outros aparelhos elétricos de iluminação', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94055000': {'description': 'Aparelhos não elétricos de iluminação', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94056000': {'description': 'Anúncios, cartazes ou tabuletas e placas indicadoras luminosos, e artigos semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94059100': {'description': 'Partes de vidro para aparelhos de iluminação', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94059200': {'description': 'Partes de plástico para aparelhos de iluminação', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94059900': {'description': 'Outras partes para aparelhos de iluminação', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            
            # PRODUTOS ALIMENTÍCIOS - Expandido
            '17019900': {'description': 'Outros açúcares de cana ou de beterraba e sacarose quimicamente pura, no estado sólido', 'ii_rate': 0.16, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '18063100': {'description': 'Chocolates e outras preparações alimentícias que contenham cacau, em blocos, tabletes ou barras, recheados', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '18063200': {'description': 'Chocolates e outras preparações alimentícias que contenham cacau, em blocos, tabletes ou barras, não recheados', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '18069000': {'description': 'Outros chocolates e outras preparações alimentícias que contenham cacau', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19053100': {'description': 'Biscoitos doces (bolachas doces)', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19053200': {'description': 'Waffles e wafers', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19054000': {'description': 'Tostas, pão torrado e produtos semelhantes torrados', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19059000': {'description': 'Outros produtos de padaria, pastelaria ou de biscoitaria', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '20019000': {'description': 'Outras preparações de produtos hortícolas, fruta ou de outras partes de plantas', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '21069000': {'description': 'Outras preparações alimentícias não especificadas nem compreendidas noutras posições', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '22021000': {'description': 'Águas, incluindo as águas minerais e as águas gaseificadas, adicionadas de açúcar', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '22029000': {'description': 'Outras bebidas não alcoólicas', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12}
        }

# Instância global do serviço
ncm_scraper = NCMScraper()