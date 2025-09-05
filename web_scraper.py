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
        Retorna base massivamente expandida de códigos NCM com foco em eletrônicos, químicos, farmacêuticos e domésticos
        """
        return {
            # ELETRÔNICOS E TECNOLOGIA - MASSIVAMENTE EXPANDIDO
            '85171100': {'description': 'Telefones móveis (celulares) e de outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85171200': {'description': 'Telefones para redes celulares ou outras redes sem fio', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176200': {'description': 'Aparelhos receptores para radiotelefonia ou radiotelegrafia', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '85176100': {'description': 'Outros aparelhos para recepção, conversão e transmissão ou regeneração de voz, imagens', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.25},
            '84713000': {'description': 'Máquinas automáticas para processamento de dados, portáteis, de peso não superior a 10 kg', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714100': {'description': 'Outras máquinas automáticas para processamento de dados', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84714900': {'description': 'Outras máquinas automáticas para processamento de dados, apresentadas sob a forma de sistemas', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85287200': {'description': 'Aparelhos receptores para televisão, mesmo incorporando um aparelho receptor', 'ii_rate': 0.20, 'ipi_rate': 0.20, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85285200': {'description': 'Monitores e projetores, que não incorporem aparelho receptor de televisão', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85258000': {'description': 'Câmeras de televisão, câmeras fotográficas digitais e câmeras de vídeo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85444200': {'description': 'Cabos coaxiais e outros condutores elétricos coaxiais', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85423100': {'description': 'Processadores e controladores, mesmo combinados com memórias', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85423200': {'description': 'Memórias', 'ii_rate': 0.16, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85183000': {'description': 'Fones de ouvido e auscultadores, mesmo combinados com microfone', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85414000': {'description': 'Diodos emissores de luz (LED)', 'ii_rate': 0.16, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS QUÍMICOS - NOVA SEÇÃO EXPANDIDA
            '28011000': {'description': 'Cloro', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28020000': {'description': 'Enxofre sublimado ou precipitado; enxofre coloidal', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28061000': {'description': 'Ácido clorídrico (ácido muriático)', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28070000': {'description': 'Ácido sulfúrico; óleum', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '28080000': {'description': 'Ácido nítrico; ácidos sulfonítricos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32041100': {'description': 'Corantes orgânicos sintéticos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '32061100': {'description': 'Pigmentos e preparações à base de dióxido de titânio', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS FARMACÊUTICOS - NOVA SEÇÃO EXPANDIDA
            '29411000': {'description': 'Penicilinas e seus derivados, com a estrutura do ácido penicilânico', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29412000': {'description': 'Estreptomicinas e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29413000': {'description': 'Tetraciclinas e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30021000': {'description': 'Antissoros e outras frações do sangue', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30031000': {'description': 'Medicamentos contendo penicilinas ou estreptomicinas', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '30033100': {'description': 'Medicamentos contendo insulina', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '29362700': {'description': 'Vitamina C e seus derivados', 'ii_rate': 0.14, 'ipi_rate': 0.00, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # UTENSÍLIOS DOMÉSTICOS - MASSIVAMENTE EXPANDIDO
            '73211100': {'description': 'Aparelhos de cozinhar e aquecedores de pratos, de ferro fundido, ferro ou aço', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '73239300': {'description': 'Outros artigos de mesa, cozinha ou outros utensílios domésticos, de aço inoxidável', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '76151100': {'description': 'Artigos de mesa, cozinha ou outros utensílios domésticos, de alumínio', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82111000': {'description': 'Sortidos de facas de mesa de lâmina cortante ou serrilhada', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82159100': {'description': 'Colheres, garfos, conchas, escumadeiras, pás para tortas, facas especiais para peixe ou manteiga', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34011100': {'description': 'Sabões e produtos orgânicos tensoativos para uso na forma de barras, pães, pedaços moldados', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '34022000': {'description': 'Preparações tensoativas, preparações para lavagem e preparações para limpeza', 'ii_rate': 0.18, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85167100': {'description': 'Aparelhos eletrotérmicos para preparo de café ou chá', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85165000': {'description': 'Fornos de microondas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '70131000': {'description': 'Artigos de vidro dos tipos utilizados para serviço de mesa ou de cozinha', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '69111000': {'description': 'Artigos para serviço de mesa ou de cozinha, de porcelana', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # VESTUÁRIO E MODA
            '61051000': {'description': 'Camisas de malha de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61091000': {'description': 'T-shirts, camisetas interiores e artigos semelhantes de malha de algodão', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '61103000': {'description': 'Suéteres, pulôveres, cardigãs, coletes e artigos semelhantes, de malha, de fibras sintéticas ou artificiais', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62034200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para homens ou rapazes', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '62046200': {'description': 'Calças, jardineiras, bermudas e shorts, de algodão, para mulheres ou meninas', 'ii_rate': 0.35, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # CALÇADOS
            '64039900': {'description': 'Outros calçados com sola de borracha, plástico, couro natural ou reconstituído', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041900': {'description': 'Outros calçados com sola de borracha ou plástico', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '64041100': {'description': 'Calçados para esporte; calçados para tênis, basquetebol, ginástica, treinamento e semelhantes', 'ii_rate': 0.35, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # COSMÉTICOS E PERFUMARIA
            '33030000': {'description': 'Perfumes e águas-de-colônia', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33041000': {'description': 'Produtos de maquiagem para os lábios', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33049900': {'description': 'Outros produtos de beleza, maquiagem e cuidados da pele', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33051000': {'description': 'Xampus para o cabelo', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33061000': {'description': 'Dentifrícios (cremes dentais)', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '33072000': {'description': 'Desodorantes corporais e antitranspirantes', 'ii_rate': 0.18, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # BRINQUEDOS E JOGOS
            '95030010': {'description': 'Triciclos, patinetes, carros de pedal e outros brinquedos semelhantes de rodas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034100': {'description': 'Bonecas que representem exclusivamente seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95036000': {'description': 'Quebra-cabeças (puzzles)', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95041000': {'description': 'Videojogos dos tipos utilizados com receptor de televisão', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # MÓVEIS
            '94035000': {'description': 'Móveis de madeira dos tipos utilizados em dormitórios', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94036000': {'description': 'Outros móveis de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.10, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017100': {'description': 'Assentos com armação de madeira, estofados', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94042900': {'description': 'Colchões de outras matérias', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ILUMINAÇÃO
            '94051000': {'description': 'Lustres e outros aparelhos elétricos de iluminação, próprios para serem suspensos ou fixados no teto ou na parede', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94052000': {'description': 'Abajures de cabeceira, de escritório e luminárias de interior, elétricos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ARTIGOS ESPORTIVOS
            '95069100': {'description': 'Artigos e equipamentos para cultura física, ginástica ou atletismo', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95062200': {'description': 'Esquis aquáticos, pranchas de surf e outros equipamentos para esportes aquáticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95065100': {'description': 'Raquetes de tênis, mesmo não encordoadas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95066100': {'description': 'Bolas de tênis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # JOIAS E RELÓGIOS  
            '71131100': {'description': 'Artigos de joalharia de metais preciosos, de prata', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '91011100': {'description': 'Relógios de pulso, elétricos, mesmo com contador de tempo incorporado, com caixa de metais preciosos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # ÓCULOS
            '90041000': {'description': 'Óculos de sol', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '90031100': {'description': 'Armações para óculos ou artigos semelhantes, de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # PRODUTOS ALIMENTÍCIOS
            '18063100': {'description': 'Chocolates e outras preparações alimentícias que contenham cacau, em blocos, tabletes ou barras, recheados', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '19053100': {'description': 'Biscoitos doces (bolachas doces)', 'ii_rate': 0.18, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},
            '22021000': {'description': 'Águas, incluindo as águas minerais e as águas gaseificadas, adicionadas de açúcar', 'ii_rate': 0.20, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.12},

            # FERRAMENTAS
            '82013000': {'description': 'Picaretas, pás, cavadeiras, enxadas, sachos, forcados, forquilhas, ancinhos e raspadeiras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82032000': {'description': 'Alicates, tenazes, pinças e ferramentas semelhantes', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '82054000': {'description': 'Chaves de fenda', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # SEÇÃO XVI - MÁQUINAS E APARELHOS, MATERIAL ELÉTRICO (SISCOMEX)
            # Capítulo 84 - Reatores nucleares, caldeiras, máquinas, aparelhos e instrumentos mecânicos
            '84011000': {'description': 'Reatores nucleares', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84012000': {'description': 'Máquinas e aparelhos para a separação isotópica', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84021100': {'description': 'Caldeiras aquatubulares com produção de vapor superior a 45 t por hora', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84021200': {'description': 'Caldeiras aquatubulares com produção de vapor não superior a 45 t por hora', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84022000': {'description': 'Caldeiras denominadas "de água superaquecida"', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84031000': {'description': 'Caldeiras para aquecimento central', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84039000': {'description': 'Outras caldeiras de vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84041000': {'description': 'Aparelhos auxiliares para caldeiras', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84042000': {'description': 'Condensadores para máquinas a vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84051000': {'description': 'Geradores de gás de ar (gás pobre) ou de gás de água', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84059000': {'description': 'Outros geradores de gás', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84061000': {'description': 'Turbinas para propulsão de embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84068100': {'description': 'Turbinas a vapor de potência superior a 40 MW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84068200': {'description': 'Turbinas a vapor de potência não superior a 40 MW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84069000': {'description': 'Partes de turbinas a vapor', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84071000': {'description': 'Motores de aviação', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84072100': {'description': 'Motores fora-de-borda, para embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84072900': {'description': 'Outros motores marinos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073100': {'description': 'Motores alternativos de cilindrada não superior a 50 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073200': {'description': 'Motores alternativos de cilindrada superior a 50 cm³ mas não superior a 250 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073300': {'description': 'Motores alternativos de cilindrada superior a 250 cm³ mas não superior a 1000 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84073400': {'description': 'Motores alternativos de cilindrada superior a 1000 cm³', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84081000': {'description': 'Motores de pistão para embarcações', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84082000': {'description': 'Motores de pistão dos tipos utilizados para propulsão de veículos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84089000': {'description': 'Outros motores de pistão', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84091000': {'description': 'Partes para motores de aviação', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84099100': {'description': 'Partes para motores de pistão de ignição por centelha', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '84099900': {'description': 'Outras partes para motores de pistão', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 85 - Máquinas, aparelhos e materiais elétricos
            '85011000': {'description': 'Motores de potência não superior a 37,5 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85012000': {'description': 'Motores universais de potência superior a 37,5 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013100': {'description': 'Motores de corrente contínua de potência não superior a 750 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013200': {'description': 'Motores de corrente contínua de potência superior a 750 W mas não superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013300': {'description': 'Motores de corrente contínua de potência superior a 75 kW mas não superior a 375 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85013400': {'description': 'Motores de corrente contínua de potência superior a 375 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85014000': {'description': 'Motores de corrente alternada, monofásicos', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015100': {'description': 'Motores de corrente alternada, polifásicos, de potência não superior a 750 W', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015200': {'description': 'Motores de corrente alternada, polifásicos, de potência superior a 750 W mas não superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85015300': {'description': 'Motores de corrente alternada, polifásicos, de potência superior a 75 kW', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016100': {'description': 'Geradores de corrente alternada de potência não superior a 75 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016200': {'description': 'Geradores de corrente alternada de potência superior a 75 kVA mas não superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016300': {'description': 'Geradores de corrente alternada de potência superior a 375 kVA mas não superior a 750 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85016400': {'description': 'Geradores de corrente alternada de potência superior a 750 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021100': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência não superior a 75 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021200': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência superior a 75 kVA mas não superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85021300': {'description': 'Grupos eletrogênios com motores de pistão de ignição por compressão, de potência superior a 375 kVA', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85022000': {'description': 'Grupos eletrogênios com motores de pistão de ignição por centelha', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85023100': {'description': 'Grupos eletrogênios com energia eólica', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '85023900': {'description': 'Outros grupos eletrogênios', 'ii_rate': 0.14, 'ipi_rate': 0.05, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # SEÇÃO XX - MERCADORIAS E PRODUTOS DIVERSOS (SISCOMEX)
            # Capítulo 94 - Móveis; mobiliário médico-cirúrgico; colchões, almofadas e semelhantes
            '94011000': {'description': 'Assentos dos tipos utilizados em veículos aéreos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94012000': {'description': 'Assentos dos tipos utilizados em veículos automóveis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94013000': {'description': 'Assentos giratórios, de altura ajustável', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94014000': {'description': 'Assentos transformáveis em camas, exceto o material de acampamento ou de jardim', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94015000': {'description': 'Assentos de vime, vime entrançado, bambu ou matérias semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94016100': {'description': 'Outros assentos, com armação de madeira, estofados', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94016900': {'description': 'Outros assentos, com armação de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94017900': {'description': 'Outros assentos, com armação de metal', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94018000': {'description': 'Outros assentos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '94019000': {'description': 'Partes de assentos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 95 - Brinquedos, jogos, artigos para divertimento ou para esporte
            '95011000': {'description': 'Carrinhos para bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95019000': {'description': 'Outros brinquedos de rodas concebidos para serem montados pelas crianças', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95021000': {'description': 'Bonecas que representem exclusivamente seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95029100': {'description': 'Partes e acessórios de bonecas que representem seres humanos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95029900': {'description': 'Outras bonecas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95031000': {'description': 'Conjuntos de construção e brinquedos de construção', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95032000': {'description': 'Outros brinquedos de plástico', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95033000': {'description': 'Outros brinquedos de madeira', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95034000': {'description': 'Outros brinquedos de metal', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95035000': {'description': 'Brinquedos que representem animais ou criaturas não humanas', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95037000': {'description': 'Outros brinquedos, conjuntos e sortidos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '95038000': {'description': 'Outros brinquedos e modelos', 'ii_rate': 0.20, 'ipi_rate': 0.30, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},

            # Capítulo 96 - Obras diversas
            '96031000': {'description': 'Vassouras e escovas de galhos ou de outras matérias vegetais', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96032100': {'description': 'Escovas de dentes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96032900': {'description': 'Outras escovas de barba, para cabelos, para unhas ou para cílios', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96033000': {'description': 'Pincéis e escovas para artistas, pincéis de escrever e pincéis semelhantes para aplicação de produtos cosméticos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96034000': {'description': 'Escovas e pincéis para pintar, caiar, envernizar ou semelhantes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96035000': {'description': 'Outras escovas que constituam partes de máquinas, aparelhos ou veículos', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96039000': {'description': 'Outras vassouras, escovas, esfregões e espanadores', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96040000': {'description': 'Peneiras e crivos, manuais', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96050000': {'description': 'Sortidos de viagem para toucador de pessoas, para costura ou para limpeza de calçado ou de roupas', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96061000': {'description': 'Botões de pressão e suas partes', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062100': {'description': 'Botões de plástico, não recobertos de matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062200': {'description': 'Botões de metais comuns, não recobertos de matérias têxteis', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96062900': {'description': 'Outros botões', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18},
            '96063000': {'description': 'Formas e outras partes de botões; esboços de botões', 'ii_rate': 0.20, 'ipi_rate': 0.15, 'pis_rate': 0.0165, 'cofins_rate': 0.076, 'icms_rate': 0.18}
        }

# Instância global do serviço
ncm_scraper = NCMScraper()